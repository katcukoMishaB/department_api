from app import app, db
from flask import jsonify
from flask_restful import Resource, request

from Services.employeeService import EmployeeService
from Validators.employeeValidator import EmployeeValidator

from Exceptions.problemDetails import ProblemDetails
from Exceptions.classes import EmployeeNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import SalaryLowException
from Exceptions.classes import WrongIdTypeException
from Exceptions.classes import DepartmentNotFoundException


from jsonschema.exceptions import ValidationError

from Loggers.controllerLogger import controllerLogger

_employeeService = EmployeeService()
_employeeValidator = EmployeeValidator()


class EmployeeController(Resource):
    """Класс контроллера работников. Обрабатывает запросы"""
    @staticmethod
    @app.route('/v1/employees', methods=['GET'])
    def get_employees():
        """Возвращает весь список подразделений."""
        return jsonify({"Employees": _employeeService.findAllEmployees()})
        
    @staticmethod
    @app.route('/v1/employees/<id>', methods=['GET'])
    def get_employee(id):
        try: 
            """Возвращает работника по id."""
            return jsonify({"Employee": _employeeService.findEmployee(id)})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска  Employee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/employees/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415
        except EmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Employee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
    
    @staticmethod
    @app.route('/v1/employees/add', methods=['POST'])
    def add_employee():
        """Создает объект работника по полученному JSON. Перед созданием проверяет его на соответствие нужной схеме"""
        try:
            request_data = request.get_json()
            print(request_data)
        except Exception as err:
            problemDetails = ProblemDetails(
            type="Ошибка коректности в Employee",
            title="JSON некоректнет",
            status=400,
            detail="Отправленные данные некоректные",
            instance="http://127.0.0.1:3000/v1/employees/add"
            )
            controllerLogger.error("Ошибка разбора JSON: " + str(err))
            return jsonify(problemDetails), 400
        try:
            _employeeValidator.validate_employee(request_data) 
            _employeeService.addEmployee(request_data)
            return jsonify({"Employees": _employeeService.findAllEmployees()})
        except ValidationError as err:
            problemDetails = ProblemDetails(
            type = "Ошибка валидации в Employee",
            title = err.message,
            status = 400,
            detail = "Отпрвленный JSON не соответствует схеме.",
            instance = "http://127.0.0.1:3000/v1/employees/add"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except UniqueNameException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания Employee",
            title = err.message,
            status = 400,
            detail = "Отпрвленная сущность уже существует.",
            instance = "http://127.0.0.1:3000/v1/employees/add"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
    
        except SalaryLowException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания Employee",
            title = err.message,
            status = 400,
            detail = "Зарплата не может быть такой маленькой (<1).",
            instance = "http://127.0.0.1:3000/v1/employees/add"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        
    
    @staticmethod
    @app.route('/v1/employees/update/<id>', methods=['PUT'])
    def update_employee(id):
        """Обновляет запись о подразделении."""
        try:
            request_data = request.get_json()
        except Exception as err:
            problemDetails = ProblemDetails(
            type="Ошибка коректности в Employee",
            title="JSON некоректнет",
            status=400,
            detail="Отправленные данные некоректные",
            instance="http://127.0.0.1:3000/v1/employees/update/<int:id>"
            )
            controllerLogger.error("Ошибка разбора JSON: " + str(err))
            return jsonify(problemDetails), 400
        try:
            _employeeValidator.validate_employee(request_data) 
            _employeeService.updateEmployee(id, request_data)
            return jsonify({"Employees": _employeeService.findAllEmployees()})
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска  Employee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/employees/update/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415

        except UniqueNameException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка создания Employee",
            title = err.message,
            status = 400,
            detail = "Отпрвленная сущность уже существует.",
            instance = "http://127.0.0.1:3000/v1/employees/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except ValidationError as err:
            problemDetails = ProblemDetails(
            type = "Ошибка валидации в Employee",
            title = err.message,
            status = 400,
            detail = "Отпрвленный JSON не соответствует схеме.",
            instance = "http://127.0.0.1:3000/v1/employees/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 400
        except EmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Employee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
        except DepartmentNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Department",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/update/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404

    @staticmethod
    @app.route('/v1/employees/delete/<id>', methods=['DELETE'])
    def delete_employee(id):
        """Удаляет подразделение, возвращает id удалённой записи."""
        try:
            response = _employeeService.deleteEmployee(id)
            return jsonify(f"{response}" )
        except WrongIdTypeException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска  Employee",
            title = err.message,
            status = 415,
            detail = "Неправильно указан id (его тип не правильный)",
            instance = "http://127.0.0.1:3000/v1/employees/delete/<id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 415

        except EmployeeNotFoundException as err:
            problemDetails = ProblemDetails(
            type = "Ошибка поиска Employee",
            title = err.message,
            status = 404,
            detail = "Неправильно указан id (его нет)",
            instance = "http://127.0.0.1:3000/v1/employees/delete/<int:id>"
            )
            controllerLogger.error(str(problemDetails))
            return jsonify(problemDetails), 404
        
