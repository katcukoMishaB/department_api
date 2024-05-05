from app import app, api
from Controllers.PageController import PageConroller
from Controllers.DepartmentController import DepartmentController
from Controllers.EmployeeController import EmployeeController


api.add_resource(PageConroller)
api.add_resource(DepartmentController)
api.add_resource(EmployeeController)


if __name__ == '__main__':

    app.run(debug=True, port=3000, host ="127.0.0.1")