from dataclasses import dataclass

@dataclass
class ProblemDetails:
    """Класс для подробного описания ошибки"""
    type: str = None
    title: str = None
    status: int = None
    detail: str = None
    instance: str = None