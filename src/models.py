from dataclasses import dataclass

from src.exceptions import IncorrectEntityError


@dataclass
class AircraftPart:
    id: str
    name: str
    category: str
    year: int
    manufacturer: str
    material: str

    def __post_init__(self):
        if not (isinstance(self.id, str)):
            raise IncorrectEntityError("Некорректный ID")
        if not (isinstance(self.name, str)):
            raise IncorrectEntityError("Некорректный name")
        if not (isinstance(self.category, str)):
            raise IncorrectEntityError("Некорректный category")
        if not (isinstance(self.manufacturer, str)):
            raise IncorrectEntityError("Некорректный manufacturer")
        if not (isinstance(self.material, str)):
            raise IncorrectEntityError("Некорректный material")
        if type(self.year) is not int:
            raise IncorrectEntityError("Нечисловое значение year")

        if not self.id.strip():
            raise IncorrectEntityError("Поле id не может быть пустым")
        if not self.name.strip():
            raise IncorrectEntityError("Поле name не может быть пустым")
        if not self.category.strip():
            raise IncorrectEntityError("Поле category не может быть пустым")
        if not self.manufacturer.strip():
            raise IncorrectEntityError("Поле manufacturer не может быть пустым")
        if not self.material.strip():
            raise IncorrectEntityError("Поле material не может быть пустым")

        if not (1910 <= self.year <= 2026):
            raise IncorrectEntityError("Некорректный год производства детали")
