import json
from jsonschema import validate

class DepartmentEmployeeValidator:
    """Класс для проверки json файлов при создании работников и подразделений."""
    def get_schema(self):
        with open('Schemes/departmentEmployee.schema.json', 'r') as file:
            schema = json.load(file)
        return schema
    
    def validate_department_employee(self, jsonData):
        schema = self.get_schema()
        validate(instance=jsonData, schema=schema)