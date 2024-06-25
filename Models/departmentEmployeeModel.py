from app import db
from .departmentModel import Department
from .employeeModel import Employee

class DepartmentEmployee(db.Model):
    """Инициализация таблицы работников и их отделов"""
    __tablename__ = "departmentEmployee"
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer,db.ForeignKey(Department.id, name = 'fk_department_work_id'), index=True)
    employee_id = db.Column(db.Integer,db.ForeignKey(Employee.id, name = 'fk_employee_work_id'), index=True)
    

    department_work = db.relationship('Department', back_populates='work_who')
    employee_work = db.relationship('Employee', back_populates='work_where')
