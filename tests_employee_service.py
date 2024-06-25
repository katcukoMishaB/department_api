import unittest
from app import app, db
from Services.employeeService import EmployeeService
from Services.departmentService import DepartmentService
from Models.employeeModel import Employee
from Models.departmentModel import Department
from Exceptions.classes import EmployeeNotFoundException, UniqueNameException, SalaryLowException

class TestEmployeeService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
        self.app_context = app.app_context()
        self.app_context.push()  
        db.create_all()

    def tearDown(self):
        db.session.rollback()  
        db.session.query(Employee).delete() 
        db.session.query(Department).delete() 
        db.session.commit()  
        self.app_context.pop()  

    def test_findAllEmployees(self):
        employee1 = Employee(last_name="Last1", first_name="First1", patronimic="Patronimic1", salary=1000, department_id=1)
        employee2 = Employee(last_name="Last2", first_name="First2", patronimic="Patronimic2", salary=2000, department_id=2)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

        service = EmployeeService()
        employees = service.findAllEmployees()

        self.assertEqual(len(employees), 2)

    def test_findEmployee(self):
        employee = Employee(last_name="Last", first_name="First", patronimic="Patronimic", salary=1500, department_id=1)
        db.session.add(employee)
        db.session.commit()

        service = EmployeeService()
        result = service.findEmployee(employee.id)

        self.assertEqual(result['id'], employee.id)
        self.assertEqual(result['last_name'], employee.last_name)
        self.assertEqual(result['first_name'], employee.first_name)
        self.assertEqual(result['patronimic'], employee.patronimic)
        self.assertEqual(result['salary'], employee.salary)

    def test_findEmployee_not_found(self):
        service = EmployeeService()
        with self.assertRaises(EmployeeNotFoundException):
            service.findEmployee(999)

    def test_addEmployee(self):
        department = Department(department_name="TestDepartment")
        db.session.add(department)
        db.session.commit()

        service = EmployeeService()
        request_data = {'department_id': department.id, 'last_name': 'NewLast', 'first_name': 'NewFirst', 'patronimic': 'NewPatronimic', 'salary': 3000}
        service.addEmployee(request_data)

        employee = Employee.query.filter_by(last_name='NewLast', first_name='NewFirst', patronimic='NewPatronimic', salary=3000, department_id=department.id).first()
        self.assertIsNotNone(employee)

    def test_addEmployee_unique_name_exception(self):
        department = Department(department_name="TestDepartment")
        db.session.add(department)
        db.session.commit()

        employee = Employee(last_name="UniqueLast", first_name="UniqueFirst", patronimic="UniquePatronimic", salary=2500, department_id=department.id)
        db.session.add(employee)
        db.session.commit()

        service = EmployeeService()
        request_data = {'department_id': department.id, 'last_name': 'UniqueLast', 'first_name': 'UniqueFirst', 'patronimic': 'UniquePatronimic', 'salary': 2500}

        with self.assertRaises(UniqueNameException):
            service.addEmployee(request_data)

    def test_addEmployee_salary_low_exception(self):
        department = Department(department_name="TestDepartment")
        db.session.add(department)
        db.session.commit()

        service = EmployeeService()
        request_data = {'department_id': department.id, 'last_name': 'LowSalary', 'first_name': 'LowSalary', 'patronimic': 'LowSalary', 'salary': 0}

        with self.assertRaises(SalaryLowException):
            service.addEmployee(request_data)

    def test_deleteEmployee(self):
        employee = Employee(last_name="ToDelete", first_name="ToDelete", patronimic="ToDelete", salary=2000, department_id=1)
        db.session.add(employee)
        db.session.commit()

        service = EmployeeService()
        result = service.deleteEmployee(employee.id)

        self.assertIsNone(Employee.query.filter_by(id=employee.id).first())

    def test_deleteEmployee_not_found_exception(self):
        service = EmployeeService()
        with self.assertRaises(EmployeeNotFoundException):
            service.deleteEmployee(999)

    def test_updateEmployee(self):
        department = Department(department_name="TestDepartment")
        db.session.add(department)
        db.session.commit()

        employee = Employee(last_name="ToUpdate", first_name="ToUpdate", patronimic="ToUpdate", salary=2000, department_id=department.id)
        db.session.add(employee)
        db.session.commit()

        service = EmployeeService()
        request_data = {'department_id': department.id, 'last_name': 'UpdatedLast', 'first_name': 'UpdatedFirst', 'patronimic': 'UpdatedPatronimic', 'salary': 3000}
        service.updateEmployee(employee.id, request_data)

        updated_employee = Employee.query.filter_by(id=employee.id).first()
        self.assertEqual(updated_employee.last_name, 'UpdatedLast')
        self.assertEqual(updated_employee.first_name, 'UpdatedFirst')
        self.assertEqual(updated_employee.patronimic, 'UpdatedPatronimic')
        self.assertEqual(updated_employee.salary, 3000)

    def test_updateEmployee_not_found_exception(self):
        service1 = EmployeeService()
        service2 = DepartmentService()
        request_data = {'department_name': 'NewDepartment'}
        service2.addDepartment(request_data)
        with self.assertRaises(EmployeeNotFoundException):
            service1.updateEmployee(999, {'department_id': 1, 'last_name': 'UpdatedLast', 'first_name': 'UpdatedFirst', 'patronimic': 'UpdatedPatronimic', 'salary': 3000})

if __name__ == '__main__':
    unittest.main()
