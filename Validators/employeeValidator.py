import json
from jsonschema import validate

class EmployeeValidator:
    """Класс для проверки json файлов добавляемых работников."""
    def get_schema(self):
        with open('Schemes/employee.schema.json', 'r') as file:
            schema = json.load(file)
        return schema
    
    def validate_employee(self, jsonData):
        schema = self.get_schema()
        validate(instance=jsonData, schema=schema)