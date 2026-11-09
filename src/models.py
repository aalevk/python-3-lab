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
        if (
            isinstance(self.id, str)
            + isinstance(self.name, str)
            + isinstance(self.category, str)
            + isinstance(self.manufacturer, str)
            + isinstance(self.material, str)
            + (type(self.year) is int)
            != 6
        ):
            raise IncorrectEntityError("Некорректный тип данных")

        if (
            not self.id.strip()
            or not self.name.strip()
            or not self.category.strip()
            or not self.manufacturer.strip()
            or not self.material.strip()
        ):
            raise IncorrectEntityError("Значение не может быть пустым")

        if not (1910 <= self.year <= 2026):
            raise IncorrectEntityError("Некорректный год производства детали")
