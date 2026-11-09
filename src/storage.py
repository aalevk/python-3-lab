from json import JSONDecodeError, dump, load

from src.catalog import AircraftCatalog
from src.exceptions import CatalogError, DamagedFileError, UnsupportedVersionError
from src.models import AircraftPart


class CatalogStorage:
    def to_dict(self, part):
        return {
            "id": part.id,
            "name": part.name,
            "category": part.category,
            "manufacturer": part.manufacturer,
            "material": part.material,
            "year": part.year,
        }

    def save(self, catalog, path):
        result = []
        for detal in catalog:
            result.append(self.to_dict(detal))
        json_doc = {"format_version": 1, "items": result}
        try:
            with open(path, "w", encoding="utf-8") as file:
                dump(json_doc, file, ensure_ascii=False, indent=4)
        except OSError as error:
            raise DamagedFileError("Не удалось сохранить файл") from error

    def load(self, catalog, path):
        try:
            with open(path, encoding="utf-8") as file:
                data = load(file)
        except OSError as error:
            raise DamagedFileError("Не удалось прочитать файл") from error
        except JSONDecodeError as error:
            raise DamagedFileError("Некорректный формат JSON") from error

        if not isinstance(data, dict):
            raise DamagedFileError("Корень JSON должен быть объектом")

        if "format_version" not in data or "items" not in data:
            raise DamagedFileError("Отсутствуют обязательные поля")

        if data["format_version"] != 1:
            raise UnsupportedVersionError("Неподдерживаемая версия")

        if not isinstance(data["items"], list):
            raise DamagedFileError("Поле items должно быть списком")

        try:
            transit_catalog = AircraftCatalog()

            for detal in data["items"]:
                if not isinstance(detal, dict):
                    raise DamagedFileError("Некорректная запись детали")

                part = AircraftPart(**detal)
                transit_catalog.add(part)

        except (TypeError, CatalogError) as error:
            raise DamagedFileError("Некорректные данные каталога") from error

        catalog._items = transit_catalog._items
        catalog._items_by_id = transit_catalog._items_by_id
