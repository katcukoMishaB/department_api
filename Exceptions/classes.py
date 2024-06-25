class UniqueNameException(Exception):
    """Возникает, если в БД есть запись подразделения/работники с таким именем"""
    def __init__(self, message):
        self.message = message

class DepartmentNotFoundException(Exception):
    """Возникает, если в запросах указывается id подразделения, которого нет в базе"""
    def __init__(self, message):
        self.message = message

class EmployeeNotFoundException(Exception):
    """Возникает, если в запросах указывается id работника,  которого нет в базе"""
    def __init__(self, message):
        self.message = message

class DepartmentEmployeeNotFoundException(Exception):
    """Возникает, если в запросах указывается id работника и id подразделения,  которого нет в базе"""
    def __init__(self, message):
        self.message = message

class SalaryLowException(Exception):
    """Возникает, если зарплата меньше 1"""
    def __init__(self, message):
        self.message = message

class WrongIdTypeException(Exception):
    """Возникает, если id не нужного типа"""
    def __init__(self, message):
        self.message = message
