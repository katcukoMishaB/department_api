from app import db
from .departmentModel import Department

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer,db.ForeignKey(Department.id, name = 'fk_department_id'), index=True)
    last_name = db.Column(db.String(128), index=True)
    first_name = db.Column(db.String(128), index=True)
    patronimic = db.Column(db.String(128), index=True)
    salary = db.Column(db.Integer, index=True)
    hire_date = db.Column(db.Date, index=True)

    departments = db.relationship('Department', back_populates='employees')