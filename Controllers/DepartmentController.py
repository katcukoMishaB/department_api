from app import app, db
from flask import jsonify
from flask_restful import Resource, request

from Services.departmentService import DepartmentService
from Validators.departmentValidator import DepartmentValidator

from Exceptions.problemDetails import ProblemDetails
from Exceptions.classes import DepartmentNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import WrongIdTypeException

from jsonschema.exceptions import ValidationError

from Loggers.controllerLogger import controllerLogger

_departmentService = DepartmentService()
_departmentValidator = DepartmentValidator()


class DepartmentController(Resource):
    """Класс контроллера подразделений. Обрабатывает запросы"""
    @staticmethod
    @app.route('/v1/departments', methods=['GET'])
    def get_departments():
        """Возвращает весь список подразделений."""
        return jsonify({"Departments": _departmentService.findAllDepartments()})


    @staticmethod
    @app.errorhandler(404)
    def pageNotFount(error):
        problemDetails = ProblemDetails(
            type = "Ошибка неправильный ввод рута",
            title ="404",
            status = 404,
            detail = "Неправильно указан юрл (его нет)",
            instance = "http://127.0.0.1:3000"
            )
        controllerLogger.error(str(problemDetails))
        return jsonify(problemDetails), 404

        
    @staticmethod
    @app.route('/v1/departments/<id>', methods=['GET'])
    def get_department(id):
        try: 
            """Возвращает подразделение по id."""
            return jsonify({"Department": _departmentService.findDepartment(id)})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415

        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
    
    @staticmethod
    @app.route('/v1/departments/add', methods=['POST'])
    def add_department():
        """Создает объект подразделения по полученному JSON. Перед созданием проверяет его на соответствие нужной схеме"""
        try:
            request_data = request.get_json()
        except Exception as err:
            problemDetails = ProblemDetails(
            type="Ошибка коректности в Department",
            title="JSON некоректнет",
            status=400,
            detail="Отправленные данные некоректные",
            instance="http://127.0.0.1:3000/v1/departments/add"
            )
            controllerLogger.error("Ошибка разбора JSON: " + str(err))
            return jsonify(problemDetails), 400
        try:
            _departmentValidator.validate_department(request_data) 
            _departmentService.addDepartment(request_data)
            return jsonify({"Departments": _departmentService.findAllDepartments()})

        except ValidationError as err:
            problemDetails = ProblemDetails(
            type = "Ошибка валидации в Department",
            title = err.message,
            status = 400,
            detail = "Отпрвленный JSON не соответствует схеме.",
            instance = "http://127.0.0.1:3000/v1/departments/add"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except UniqueNameException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания Department",
            title = err.message,
            status = 400,
            detail = "Отпрвленная сущность уже существует.",
            instance = "http://127.0.0.1:3000/v1/departments/add"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        
    
    @staticmethod
    @app.route('/v1/departments/update/<id>', methods=['PUT'])
    def update_department(id):
        """Обновляет запись о подразделении."""
        try:
            request_data = request.get_json()
        except Exception as err:
            problemDetails = ProblemDetails(
            type="Ошибка коректности в Department",
            title="JSON некоректнет",
            status=400,
            detail="Отправленные данные некоректные",
            instance="http://127.0.0.1:3000/v1/departments/update/<int:id>"
            )
            controllerLogger.error("Ошибка разбора JSON: " + str(err))
            return jsonify(problemDetails), 400
        try:
            _departmentValidator.validate_department(request_data) 
            _departmentService.updateDepartment(id, request_data)
            return jsonify({"Departments": _departmentService.findAllDepartments()})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/update/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415
        except UniqueNameException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания Department",
            title = err.message,
            status = 400,
            detail = "Отпрвленная сущность уже существует.",
            instance = "http://127.0.0.1:3000/v1/departments/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except ValidationError as err:
            problemDetails = ProblemDetails(
            type = "Ошибка валидации в Department",
            title = err.message,
            status = 400,
            detail = "Отпрвленный JSON не соответствует схеме.",
            instance = "http://127.0.0.1:3000/v1/departments/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404

    @staticmethod
    @app.route('/v1/departments/delete/<id>', methods=['DELETE'])
    def delete_department(id):
        """Удаляет подразделение, возвращает id удалённой записи."""
        try:
            response = _departmentService.deleteDepartment(id)
            return jsonify(f"{response}" )
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/delete/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415
        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/delete/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
