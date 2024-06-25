from app import db
from .departmentModel import Department

class Employee(db.Model):
    """Инициализация таблицы работников"""
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(128), index=True)
    first_name = db.Column(db.String(128), index=True)
    patronimic = db.Column(db.String(128), index=True)
    salary = db.Column(db.Integer, index=True)
    work_status = db.Column(db.Boolean, index=True)
    
    work_where = db.relationship('DepartmentEmployee', back_populates='employee_work')
