import pytest

from src.exceptions import IncorrectEntityError
from src.models import AircraftPart


def test_create_aircraft_part():
    part = AircraftPart(
        id="A001",
        name="Крыло",
        category="Конструкция",
        year=2020,
        manufacturer="МАИ",
        material="Алюминий",
    )

    assert part.id == "A001"
    assert part.name == "Крыло"
    assert part.year == 2020


def test_wrong_type():
    with pytest.raises(IncorrectEntityError):
        AircraftPart(
            id=123,
            name="Крыло",
            category="Конструкция",
            year=2020,
            manufacturer="МАИ",
            material="Алюминий",
        )


def test_empty_name():
    with pytest.raises(IncorrectEntityError):
        AircraftPart(
            id="A001",
            name="",
            category="Конструкция",
            year=2020,
            manufacturer="МАИ",
            material="Алюминий",
        )


def test_empty_category():
    with pytest.raises(IncorrectEntityError):
        AircraftPart(
            id="A001",
            name="Крыло",
            category="",
            year=2020,
            manufacturer="МАИ",
            material="Алюминий",
        )


def test_wrong_year():
    with pytest.raises(IncorrectEntityError):
        AircraftPart(
            id="A001",
            name="Крыло",
            category="Конструкция",
            year=1800,
            manufacturer="МАИ",
            material="Алюминий",
        )


def test_year_as_bool():
    with pytest.raises(IncorrectEntityError):
        AircraftPart(
            id="A001",
            name="Крыло",
            category="Конструкция",
            year=True,
            manufacturer="МАИ",
            material="Алюминий",
        )
