import json
from jsonschema import validate

class DepartmentValidator:
    """Класс для проверки json файлов при создании подразделений."""
    def get_schema(self):
        with open('Schemes/department.schema.json', 'r') as file:
            schema = json.load(file)
        return schema
    
    def validate_department(self, jsonData):
        schema = self.get_schema()
        validate(instance=jsonData, schema=schema)