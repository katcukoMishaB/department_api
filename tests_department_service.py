import unittest
from app import app, db
from Services.departmentService import DepartmentService
from Models.departmentModel import Department
from Models.employeeModel import Employee
from Exceptions.classes import DepartmentNotFoundException, UniqueNameException

class TestDepartmentService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
        self.app_context = app.app_context()
        self.app_context.push()  
        db.create_all()

    def tearDown(self):
        db.session.rollback()  
        db.session.query(Department).delete() 
        db.session.query(Employee).delete() 
        db.session.commit()  
        self.app_context.pop()  

    def test_findAllDepartmentsTrue(self):
        department1 = Department(department_name="Department 1")
        department2 = Department(department_name="Department 2")
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()

        service = DepartmentService()
        departments = service.findAllDepartments()

        self.assertEqual(len(departments), 2)

    def test_findAllDepartmentsFalse(self):
        department1 = Department(department_name="Department 1")
        department2 = Department(department_name="Department 2")
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()

        service = DepartmentService()
        departments = service.findAllDepartments()

        self.assertEqual(len(departments), 0)

    def test_findDepartmentTrue(self):
        
        department = Department(department_name="DepartmentTest")
        db.session.add(department)
        db.session.commit()

        service = DepartmentService()
        result = service.findDepartment(department.id)

        self.assertEqual(result['id'], department.id)
        self.assertEqual(result['department_name'], department.department_name)

    def test_findDepartmentFalse(self):
        
        department = Department(department_name="DepartmentTest")
        db.session.add(department)
        db.session.commit()

        service = DepartmentService()
        result = service.findDepartment(department.id)

        self.assertNotEqual(result['id'], department.id)
        self.assertNotEqual(result['department_name'], department.department_name)
    def test_UniqueNameException(self):
        service = DepartmentService()
        request_data = {'department_name': 'NewDepartment1'}
        service.addDepartment(request_data)

        department = Department.query.filter_by(department_name='NewDepartment1').first()
        self.assertIsNotNone(department)

        with self.assertRaises(UniqueNameException):
            request_data = {'department_name': 'NewDepartment1'}
            service.addDepartment(request_data)

    def test_DepartmentNotFoundException(self):
        department = Department(department_name="DepartmentTest")
        db.session.add(department)
        db.session.commit()
        service = DepartmentService()
        with self.assertRaises(DepartmentNotFoundException):
            service.findDepartment(2)  

    def test_addDepartment(self):
        service = DepartmentService()
        request_data = {'department_name': 'NewDepartment'}
        service.addDepartment(request_data)

        department = Department.query.filter_by(department_name='NewDepartment').first()
        self.assertIsNotNone(department)

    def test_deleteDepartment(self):
        department = Department(department_name="DepartmentTest")
        db.session.add(department)
        db.session.commit()

        service = DepartmentService()
        result = service.deleteDepartment(department.id)

   
        self.assertIsNone(Department.query.filter_by(id=department.id).first())

    def test_deleteDepartmentNotFoundException(self):
        service = DepartmentService()
        with self.assertRaises(DepartmentNotFoundException):
            service.deleteDepartment(999)  

    def test_updateDepartment(self):
        department = Department(department_name="DepartmentTest")
        db.session.add(department)
        db.session.commit()

        service = DepartmentService()
        request_data = {'department_name': 'UpdatedDepartment'}
        service.updateDepartment(department.id, request_data)


        updated_department = Department.query.filter_by(id=department.id).first()
        self.assertEqual(updated_department.department_name, 'UpdatedDepartment')

    def test_updateDepartmentNotFoundException(self):
        service = DepartmentService()
        with self.assertRaises(DepartmentNotFoundException):
            service.updateDepartment(999, {'department_name': 'UpdatedDepartment'})

if __name__ == '__main__':
    unittest.main()
