from app import db

class Department(db.Model):
    """Инициализация таблицы подразделений"""
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(64), index=True, unique=True)

    work_who = db.relationship('DepartmentEmployee', back_populates='department_work')
