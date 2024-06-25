import unittest
from app import app, db
from Services.departmentEmployeeService import DepartmentEmployeeService
from Models.departmentModel import Department
from Models.employeeModel import Employee
from Models.departmentEmployeeModel import DepartmentEmployee
from Exceptions.classes import DepartmentNotFoundException, EmployeeNotFoundException, UniqueNameException, WrongIdTypeException, DepartmentEmployeeNotFoundException

class TestDepartmentEmployeeService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.session.query(DepartmentEmployee).delete()
        db.session.query(Department).delete()
        db.session.query(Employee).delete()
        db.session.commit()
        self.app_context.pop()

    

    def test_findAllDepartmentEmployeesFalse(self):
        department = Department(department_name="Dep 1")
        db.session.add(department)
        db.session.commit()

        service = DepartmentEmployeeService()
        with self.assertRaises(DepartmentNotFoundException):
            service.findAllDepartmentEmployees(department.id)


    def test_findDepartmentEmployeeFalse(self):
        service = DepartmentEmployeeService()
        with self.assertRaises(DepartmentNotFoundException):
            service.findDepartmentEmployee(1, 1)

    
    
    

    

if __name__ == '__main__':
    unittest.main()