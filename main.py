from app import app, api
from Controllers.DepartmentController import DepartmentController
from Controllers.EmployeeController import EmployeeController
from Controllers.DepartmentEmployeeController import DepartmentEmployeeController


api.add_resource(DepartmentController)
api.add_resource(EmployeeController)
api.add_resource(DepartmentEmployeeController)

if __name__ == '__main__':

    app.run(debug=True, port=3000, host ="127.0.0.1")