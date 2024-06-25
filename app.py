from flask import Flask
from flask_restful import Api
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.json.ensure_ascii = False
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

from Models.departmentModel import Department
from Models.employeeModel import Employee
from Models.departmentEmployeeModel import DepartmentEmployee