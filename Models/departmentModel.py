from app import db

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(64), index=True, unique=True)

    employees = db.relationship('Employee', back_populates='departments') 