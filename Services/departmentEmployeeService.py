from app import db
from Models.departmentModel import Department
from Models.employeeModel import Employee
from Models.departmentEmployeeModel import DepartmentEmployee
from Exceptions.classes import DepartmentNotFoundException
from Exceptions.classes import EmployeeNotFoundException
from Exceptions.classes import UniqueNameException
from Exceptions.classes import WrongIdTypeException
from Exceptions.classes import DepartmentEmployeeNotFoundException
from Loggers.serviceLogger import serviceLogger

"""Класс сервиса подразделений. Выполняет операции поиска (всех и по id), создания, изменения, удаления."""
class DepartmentEmployeeService:
    def findAllDepartmentEmployees(self, department_id):
        """Возвращает все подразделения."""
        try:
            department_id = int(department_id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{department_id}")
            raise err
        department_employee = DepartmentEmployee.query.filter_by(
                department_id=department_id
                ).all()
        if not department_employee:
                    err = DepartmentNotFoundException("У Подразделения нет работников или его не существует")
                    serviceLogger.error(f"{err.message} — id:{department_id}")
                    raise err
        departments_dict = []
        for department in department_employee:
            department_dict = {
                "id": department.id,
                "department_id": department.department_id,
                "employee_id": department.employee_id,
            }
            departments_dict.append(department_dict)
        serviceLogger.info(f"Выполнен вывод всех подразделений и работников.")
        return departments_dict
        
        
    
    def findDepartmentEmployee(self, department_id, employee_id):
                """Возвращает подразделение с заданным id."""
                try:
                    department_id = int(department_id)
                except ValueError:
                    err = WrongIdTypeException("Неверный айди")
                    serviceLogger.error(f"{err.message} — id:{department_id}")
                    raise err
                try:
                    employee_id = int(employee_id)
                except ValueError:
                    err = WrongIdTypeException("Неверный айди")
                    serviceLogger.error(f"{err.message} — id:{employee_id}")
                    raise err

                department_employee_dep = DepartmentEmployee.query.filter_by(
                department_id=department_id
                ).first()
                
                if not department_employee_dep:
                    err = DepartmentNotFoundException("Подразделения нет")
                    serviceLogger.error(f"{err.message} — id:{department_id}")
                    raise err
                department_employee_emp = DepartmentEmployee.query.filter_by(
                employee_id=employee_id
                ).first()

                if not department_employee_emp:
                    err = EmployeeNotFoundException("Работника нет")
                    serviceLogger.error(f"{err.message} — id:{employee_id}")
                    raise err
                
                department_dict = {
                        "id": department_employee_emp.id,
                        "department_id": department_employee_emp.department_id,
                        "employee_id": department_employee_emp.employee_id,
                    }
            
                serviceLogger.info(f"Выполнен вывод подразделения.")
                return department_dict
    
    def addDepartmentEmployee(self, department_id, request_data):
        """Добавляет подразделение в БД."""
        try:
            department_id = int(department_id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{department_id}")
            raise err

        employee_id = request_data.get('employee_id')
        existing_department = Department.query.filter_by(id=department_id).first()
        if not existing_department:
            err = DepartmentNotFoundException("Такого подразделения нет")
            serviceLogger.error(f"{err.message} — id:{department_id}")
            raise err
        existing_employee = Employee.query.filter_by(id=employee_id).first()

        if not existing_employee:
                    err = EmployeeNotFoundException("Работника нет")
                    serviceLogger.error(f"{err.message} — id:{department_id}")
                    raise err
        
        existing_department_employee = DepartmentEmployee.query.filter_by(department_id=department_id, employee_id=employee_id).first()
        if existing_department_employee:
                err = UniqueNameException("Такое  уже есть")
                serviceLogger.error(f"{err.message} — :{existing_department.id}")
                raise err
        
        new_department = DepartmentEmployee(
                department_id = department_id,
                employee_id = employee_id
            )
        existing_employee.work_status = True
        db.session.add(new_department)
        db.session.commit()
        serviceLogger.info(f"Добавлено подразделение {str(new_department)}")

    def deleteDepartmentEmployee(self, department_id, employee_id):
        """Удаление подразделения по id."""
     
        try:
            department_id = int(department_id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{department_id}")
            raise err
        try:
            employee_id = int(employee_id)
        except ValueError:
            err = WrongIdTypeException("Неверный айди")
            serviceLogger.error(f"{err.message} — id:{employee_id}")
            raise err

        department_employee_dep = DepartmentEmployee.query.filter_by(
        department_id=department_id, employee_id=employee_id
        ).first()
        
        if not department_employee_dep:
            err = DepartmentEmployeeNotFoundException("Такой Работника с таким Подразделением нет")
            serviceLogger.error(f"{err.message}")
            raise err
        department_employee_emp = DepartmentEmployee.query.filter_by(
        employee_id=employee_id
        ).count()
        print(department_employee_emp)
        if department_employee_emp < 2:

            fire_employee_status = Employee.query.filter_by(id=employee_id).first()
            fire_employee_status.work_status = False

        DepartmentEmployee.query.filter_by(department_id=department_id,employee_id=employee_id).delete()
        
        db.session.commit()
        serviceLogger.info(f"Удалено подразделение {department_employee_dep.id}")
        return f"Удалено подразделение {department_employee_dep.id}"
    
