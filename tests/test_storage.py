import json

import pytest

from src.catalog import AircraftCatalog
from src.exceptions import DamagedFileError, UnsupportedVersionError
from src.models import AircraftPart
from src.storage import FORMAT_VERSION, CatalogStorage


def create_part(part_id, name):
    return AircraftPart(
        id=part_id,
        name=name,
        category="Конструкция",
        year=2020,
        manufacturer="МАИ",
        material="Алюминий",
    )


def test_save_and_load(tmp_path):
    catalog = AircraftCatalog()
    part = create_part("A001", "Крыло")
    catalog.add(part)

    storage = CatalogStorage()
    path = tmp_path / "catalog.json"

    storage.save(catalog, path)

    new_catalog = AircraftCatalog()
    storage.load(new_catalog, path)

    assert len(new_catalog) == 1
    assert new_catalog.get("A001") == part


def test_load_empty_catalog(tmp_path):
    path = tmp_path / "catalog.json"
    data = {"format_version": FORMAT_VERSION, "items": []}
    path.write_text(json.dumps(data), encoding="utf-8")

    catalog = AircraftCatalog()
    catalog.add(create_part("A001", "Крыло"))

    storage = CatalogStorage()
    storage.load(catalog, path)

    assert len(catalog) == 0


def test_load_wrong_json(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text("{неправильный json", encoding="utf-8")

    catalog = AircraftCatalog()
    storage = CatalogStorage()

    with pytest.raises(DamagedFileError):
        storage.load(catalog, path)


def test_load_wrong_version(tmp_path):
    path = tmp_path / "catalog.json"
    data = {"format_version": FORMAT_VERSION + 1, "items": []}
    path.write_text(json.dumps(data), encoding="utf-8")

    catalog = AircraftCatalog()
    storage = CatalogStorage()

    with pytest.raises(UnsupportedVersionError):
        storage.load(catalog, path)


def test_load_missing_file(tmp_path):
    catalog = AircraftCatalog()
    storage = CatalogStorage()
    path = tmp_path / "missing.json"

    with pytest.raises(DamagedFileError):
        storage.load(catalog, path)


def test_load_does_not_change_catalog_if_data_is_wrong(tmp_path):
    catalog = AircraftCatalog()
    old_part = create_part("A001", "Старое крыло")
    catalog.add(old_part)

    path = tmp_path / "catalog.json"
    data = {
        "format_version": FORMAT_VERSION,
        "items": [{"id": "A002", "name": "Новое крыло"}]
    }
    path.write_text(json.dumps(data), encoding="utf-8")

    storage = CatalogStorage()

    with pytest.raises(DamagedFileError):
        storage.load(catalog, path)

    assert len(catalog) == 1
    assert catalog.get("A001") == old_part
    assert "A002" not in catalog


def test_load_duplicate_id(tmp_path):
    catalog = AircraftCatalog()
    old_part = create_part("A001", "Старое крыло")
    catalog.add(old_part)

    path = tmp_path / "catalog.json"
    data = {
        "format_version": FORMAT_VERSION,
        "items": [
            {
                "id": "A002",
                "name": "Крыло",
                "category": "Конструкция",
                "year": 2020,
                "manufacturer": "МАИ",
                "material": "Алюминий",
            },
            {
                "id": "A002",
                "name": "Двигатель",
                "category": "Конструкция",
                "year": 2020,
                "manufacturer": "МАИ",
                "material": "Алюминий",
            },
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")

    storage = CatalogStorage()

    with pytest.raises(DamagedFileError):
        storage.load(catalog, path)

    assert len(catalog) == 1
    assert catalog.get("A001") == old_part
    assert "A002" not in catalog
