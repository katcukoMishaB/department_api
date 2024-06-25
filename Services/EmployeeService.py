from app import db
from Models.departmentModel import Department
from Models.employeeModel import Employee
from Models.departmentEmployeeModel import DepartmentEmployee
from Exceptions.classes import EmployeeNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import SalaryLowException
from Exceptions.classes import WrongIdTypeException

from Loggers.serviceLogger import serviceLogger
from Services.departmentService import DepartmentService

_departmentService = DepartmentService()

"""Класс сервиса рвботников. Выполняет операции поиска (всех и по id), создания, изменения, удаления."""
class EmployeeService:
    def findAllEmployees(self):
        """Возвращает всех работников."""
        employee = Employee.query.all()
        employees_dict = []
        for employee in employee:
            employee_dict = {
                "id": employee.id,
                "last_name": employee.last_name,
                "first_name": employee.first_name,
                "patronimic": employee.patronimic,
                "salary": employee.salary,
                "work_status": employee.work_status,
            }
            employees_dict.append(employee_dict)
        serviceLogger.info(f"Выполнен вывод всех работников.")
        return employees_dict
        
        
    
    def findEmployee(self, id):
        """Возвращает работника с заданным id."""
        try:
            id = int(id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err

        employee = Employee.query.filter_by(
        id=id
        
        ).first()
        
        if not employee:
            err = EmployeeNotFoundException("Работника нет")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        
        employee_dict = {
        "id": employee.id,
        "last_name": employee.last_name,
        "first_name": employee.first_name,
        "patronimic": employee.patronimic,
        "salary": employee.salary,
        "work_status": employee.work_status,
        }
    
        serviceLogger.info(f"Выполнен вывод работника.")
        return employee_dict
    
    def addEmployee(self, request_data):
        """Добавляет работника в БД."""
        last_name = request_data.get('last_name')
        first_name = request_data.get('first_name')
        patronimic = request_data.get('patronimic')
        salary = request_data.get('salary')

        if salary < 1:
                err = SalaryLowException("Зарплата не может быть нулевой")
                serviceLogger.error(f"{err.message} — Зарплата была:{salary}")
                raise err
        existing_employee = Employee.query.filter_by(last_name=last_name, first_name=first_name, patronimic=patronimic,salary=salary).first()
        
        if existing_employee:
                err = UniqueNameException("Такой работник уже есть")
                serviceLogger.error(f"{err.message} — Фио:{last_name,first_name,patronimic}")
                raise err
        
        new_employee = Employee(
            last_name = last_name,
            first_name = first_name,
            patronimic = patronimic,
            salary = salary,
            work_status = False
            )
        db.session.add(new_employee)
        db.session.commit()
        serviceLogger.info(f"Добавлен работник {str(new_employee)}")

    def deleteEmployee(self, id):
        """Удаление работника по id."""
        try:
            id = int(id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        employee = Employee.query.filter_by(id=id).first()

        if not employee:
            err = EmployeeNotFoundException("Работника нет")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        
        employee.work_status = False

        DepartmentEmployee.query.filter_by(employee_id=id).delete()

        db.session.commit()
        serviceLogger.info(f"Удален работник {id}")
        return f"Удален работник {id}"
    
    def updateEmployee(self, id, request_data):
        """Изменяет данные о работнике в БД."""
        try:
            id = int(id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        last_name = request_data.get('last_name')
        first_name = request_data.get('first_name')
        patronimic = request_data.get('patronimic')
        salary = request_data.get('salary')

        new_data_employee = Employee.query.filter_by(id=id).first()
        if not new_data_employee:
            err = EmployeeNotFoundException("Работника нет")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        
        existing_employee = Employee.query.filter_by(last_name=last_name, first_name=first_name, patronimic=patronimic,salary=salary).first()
        
        if existing_employee:
                err = UniqueNameException("Такой работник уже есть")
                serviceLogger.error(f"{err.message} — Фио:{last_name,first_name,patronimic}")
                raise err
        
        new_data_employee.last_name = last_name
        new_data_employee.first_name = first_name
        new_data_employee.patronimic = patronimic
        new_data_employee.salary = salary

        db.session.commit()
        serviceLogger.info(f"Изменены данные работника {new_data_employee.last_name}  c id {id} на {request_data}")
        
        