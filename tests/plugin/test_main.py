import pytest

import plugin
from plugin.exceptions import UnknownClassException
from plugin.main import DataBuilderPlugin


def test_nothing_to_change(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    output = DataBuilderPlugin().on_page_markdown("", None, None, None)

    assert output == ""


def test_no_data_file(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/non-existent-data.json")

    with pytest.raises(FileNotFoundError):
        DataBuilderPlugin().on_page_markdown("", None, None, None)


def test_success(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contracts

!!! backend:DummyBackend1
    """

    output = DataBuilderPlugin().on_page_markdown(markdown, None, None, None)

    expected = """
# this is a page title


## Some/Path/DummyClass

Dummy docstring

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |
| patient_id | a column description | PseudoPatientId | Must have a value, must be unique. |






## Some/Path/DummyClass2

Dummy docstring2.

Second line.

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |







Contracts implemented:

* [`Some/Path/DummyClass`](contracts-reference.md#somepathdummyclass)
* [`Some/Path/DummyClass2`](contracts-reference.md#somepathdummyclass2)
    """

    assert output == expected


def test_unknown_class(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    with pytest.raises(UnknownClassException):
        DataBuilderPlugin().on_page_markdown(
            "\n!!! backend:UnknownBackend\n", None, None, None
        )
