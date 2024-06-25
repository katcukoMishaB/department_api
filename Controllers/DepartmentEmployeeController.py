from app import app, db
from flask import jsonify
from flask_restful import Resource, request

from Services.departmentEmployeeService import DepartmentEmployeeService
from Validators.departmentEmployeeValidator import DepartmentEmployeeValidator

from Exceptions.problemDetails import ProblemDetails
from Exceptions.classes import DepartmentNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import WrongIdTypeException
from Exceptions.classes import EmployeeNotFoundException
from Exceptions.classes import DepartmentEmployeeNotFoundException

from jsonschema.exceptions import ValidationError

from Loggers.controllerLogger import controllerLogger

_departmentEmplyeeService = DepartmentEmployeeService()
_departmentEmployeeValidator = DepartmentEmployeeValidator()


class DepartmentEmployeeController(Resource):
    """Класс контроллера подразделений и работников. Обрабатывает запросы"""
    @staticmethod
    @app.route('/v1/departments/<department_id>/employees', methods=['GET'])
    def get_departments_employee(department_id):
        """Возвращает весь список подразделений и работников."""
        try: 
            return jsonify({"Department": _departmentEmplyeeService.findAllDepartmentEmployees(department_id)})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employees"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415

        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employees"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404

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
    @app.route('/v1/departments/<department_id>/employee/<employee_id>', methods=['GET'])
    def get_department_employee(department_id, employee_id):
        try: 
            """Возвращает подразделение по id."""
            return jsonify({"Department": _departmentEmplyeeService.findDepartmentEmployee(department_id, employee_id)})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employee/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415

        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employee/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
        except EmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employee/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))

            return jsonify(problemDetails), 404
    @staticmethod
    @app.route('/v1/departments/<department_id>/add_employee', methods=['POST'])
    def add_department_employee(department_id):
        """Создает объект подразделения по полученному JSON. Перед созданием проверяет его на соответствие нужной схеме"""
        try:
            request_data = request.get_json()
        except Exception as err:
            problemDetails = ProblemDetails(
            type="Ошибка коректности в DepartmentEmployee",
            title="JSON некоректнет",
            status=400,
            detail="Отправленные данные некоректные",
            instance="http://127.0.0.1:3000/v1/departments/<department_id>/add_employee"
            )
            controllerLogger.error("Ошибка разбора JSON: " + str(err))
            return jsonify(problemDetails), 400
        try:
            _departmentEmployeeValidator.validate_department_employee(request_data) 
            _departmentEmplyeeService.addDepartmentEmployee(department_id, request_data)
            return jsonify({"Department": _departmentEmplyeeService.findAllDepartmentEmployees(department_id)})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/employee/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415
        except ValidationError as err:
            problemDetails = ProblemDetails(
            type = "Ошибка валидации в DepartmentEmployee",
            title = err.message,
            status = 400,
            detail = "Отпрвленный JSON не соответствует схеме.",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/add_employee"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except UniqueNameException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания DepartmentEmployee",
            title = err.message,
            status = 400,
            detail = "Отпрвленная сущность уже существует.",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/add_employee"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/add_employee"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
        except EmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/<int:id>"
            )
            controllerLogger.error(str(problemDetails))

            return jsonify(problemDetails), 404
        

    @staticmethod
    @app.route('/v1/departments/<department_id>/delete/<employee_id>', methods=['DELETE'])
    def delete_department_employee(department_id, employee_id):
        """Удаляет подразделение, возвращает id удалённой записи."""
        try:
            response = _departmentEmplyeeService.deleteDepartmentEmployee(department_id, employee_id)
            return jsonify(f"{response}" )
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/delete/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415
        except DepartmentEmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска DepartmentEmployee",
            title = err.message,
            status = 404,
            detail = "Неправильно указаны id (его нет)",
            instance = "http://127.0.0.1:3000/v1/departments/<department_id>/delete/<employee_id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
        