from app import db
from Models.departmentModel import Department
from Models.employeeModel import Employee
from Models.departmentEmployeeModel import DepartmentEmployee
from Exceptions.classes import DepartmentNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import WrongIdTypeException

from Services.departmentEmployeeService import DepartmentEmployeeService

from Loggers.serviceLogger import serviceLogger

"""Класс сервиса подразделений. Выполняет операции поиска (всех и по id), создания, изменения, удаления."""
class DepartmentService:
    def findAllDepartments(self):
        """Возвращает все подразделения."""
        departments = Department.query.all()
        departments_dict = []
        for department in departments:
            department_dict = {
                "id": department.id,
                "department_name": department.department_name,
            }
            departments_dict.append(department_dict)
        serviceLogger.info(f"Выполнен вывод всех подразделений.")
        return departments_dict
        
        
    
    def findDepartment(self, id):
                """Возвращает подразделение с заданным id."""
                try:
                    id = int(id)
                except ValueError:
                    err = WrongIdTypeException("Неверный айди")
                    serviceLogger.error(f"{err.message} — id:{id}")
                    raise err


                department = Department.query.filter_by(
                id=id
                ).first()
                
                if not department:
                    err = DepartmentNotFoundException("Подразделения нет")
                    serviceLogger.error(f"{err.message} — id:{id}")
                    raise err
                
                department_dict = {
                        "id": department.id,
                        "department_name": department.department_name,
                    }
            
                serviceLogger.info(f"Выполнен вывод подразделения.")
                return department_dict
    
    def addDepartment(self, request_data):
        """Добавляет подразделение в БД."""
        department_name = request_data.get('department_name')
        existing_department = Department.query.filter_by(department_name=department_name).first()
        if existing_department:
                err = UniqueNameException("Такое подразделение уже есть")
                serviceLogger.error(f"{err.message} — название:{department_name}")
                raise err
        new_department = Department(
                department_name = department_name
            )
        db.session.add(new_department)
        db.session.commit()
        serviceLogger.info(f"Добавлено подразделение {str(new_department)}")

    def deleteDepartment(self, id):
        """Удаление подразделения по id."""
        try:
            id = int(id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err

        department = Department.query.filter_by(id=id).first()
        if not department:
            err = DepartmentNotFoundException("Такого подразделения нет")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
            
        delete_employees = DepartmentEmployee.query.filter_by(department_id=id).all()
        for dep in delete_employees:  
            delete_employee = dep.employee_id
            DepartmentEmployeeService.deleteDepartmentEmployee(self, id, delete_employee)

        db.session.delete(department)
        db.session.commit()
        serviceLogger.info(f"Удалено подразделение {id}")
        return f"Удалено подразделение {id}"
    
    def updateDepartment(self, id, request_data):
        """Изменяет данные о подразделение в БД."""
        try:
            id = int(id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err

        department_name = request_data.get('department_name')
        new_data_department = Department.query.filter_by(id=id).first()
        if not new_data_department:
            err = DepartmentNotFoundException("Подразделения нет")
            serviceLogger.error(f"{err.message} — id:{id}")
            raise err
        existing_department = Department.query.filter_by(department_name=department_name).first()
        if existing_department:
                err = UniqueNameException("Такое подразделение уже есть")
                serviceLogger.error(f"{err.message} — название:{department_name}")
                raise err
        new_data_department.department_name = department_name
        db.session.commit()
        serviceLogger.info(f"Изменено подразделение {new_data_department.department_name}  c id {id} на {str(department_name)}")
