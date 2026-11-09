import pytest

from src.catalog import AircraftCatalog
from src.exceptions import DuplicateIDError, NotFoundObjectError
from src.models import AircraftPart


def create_part(part_id, name, category):
    return AircraftPart(
        id=part_id,
        name=name,
        category=category,
        year=2020,
        manufacturer="МАИ",
        material="Алюминий",
    )


def test_add_and_get():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")

    catalog.add(part)

    assert catalog.get("A001") == part
    assert len(catalog) == 1


def test_add_duplicate():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")

    catalog.add(part)

    with pytest.raises(DuplicateIDError):
        catalog.add(part)


def test_add_many_parts():
    catalog = AircraftCatalog()
    part1 = create_part("A001", "Крыло", "Конструкция")
    part2 = create_part("A002", "Двигатель", "Силовая установка")

    catalog.add(part1)
    catalog.add(part2)

    assert len(catalog) == 2
    assert catalog.get("A001") == part1
    assert catalog.get("A002") == part2


def test_get_missing_part():
    catalog = AircraftCatalog()

    with pytest.raises(NotFoundObjectError):
        catalog.get("A999")


def test_remove():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")

    catalog.add(part)
    catalog.remove("A001")

    assert len(catalog) == 0
    assert "A001" not in catalog


def test_remove_one_part():
    catalog = AircraftCatalog()
    part1 = create_part("A001", "Крыло", "Конструкция")
    part2 = create_part("A002", "Двигатель", "Силовая установка")

    catalog.add(part1)
    catalog.add(part2)
    catalog.remove("A001")

    assert len(catalog) == 1
    assert catalog.get("A002") == part2


def test_remove_missing_part():
    catalog = AircraftCatalog()

    with pytest.raises(NotFoundObjectError):
        catalog.remove("A999")


def test_find_by_category():
    catalog = AircraftCatalog()
    part1 = create_part("A001", "Крыло", "Конструкция")
    part2 = create_part("A002", "Двигатель", "Силовая установка")
    part3 = create_part("A003", "Фюзеляж", "Конструкция")

    catalog.add(part1)
    catalog.add(part2)
    catalog.add(part3)

    result = catalog.find_by_category("Конструкция")

    assert len(result) == 2
    assert part1 in result
    assert part3 in result


def test_find_wrong_category():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")
    catalog.add(part)

    result = catalog.find_by_category("Двигатель")

    assert result == []


def test_find_by_name():
    catalog = AircraftCatalog()
    part1 = create_part("A001", "Крыло самолета", "Конструкция")
    part2 = create_part("A002", "Двигатель", "Силовая установка")

    catalog.add(part1)
    catalog.add(part2)

    result = catalog.find_by_name("КРЫЛО")

    assert len(result) == 1
    assert result[0] == part1


def test_find_part_of_name():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло самолета", "Конструкция")
    catalog.add(part)

    result = catalog.find_by_name("самол")

    assert result == [part]


def test_find_wrong_name():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")
    catalog.add(part)

    result = catalog.find_by_name("Двигатель")

    assert result == []


def test_iteration():
    catalog = AircraftCatalog()
    part1 = create_part("A001", "Крыло", "Конструкция")
    part2 = create_part("A002", "Двигатель", "Силовая установка")

    catalog.add(part1)
    catalog.add(part2)

    result = list(catalog)

    assert result == [part1, part2]


def test_contains():
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло", "Конструкция")

    catalog.add(part)

    assert "A001" in catalog
    assert "A999" not in catalog
