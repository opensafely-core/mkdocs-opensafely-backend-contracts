import pytest

import plugin
from plugin.exceptions import UnknownClassException
from plugin.main import DataBuilderPlugin


def test_multiple_paths_to_change(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contract:dummy_module.DummyClass

!!! contract:dummy_module2.DummyClass2

!!! backend:DummyBackend1

!!! backend:DummyBackend2
    """

    output = DataBuilderPlugin().on_page_markdown(markdown, None, None, None)

    expected = """
# this is a page title

## DummyClass

Dummy docstring

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |
| patient_id | a column description | PseudoPatientId | Must have a value, Must be unique. |

## DummyClass2

Dummy docstring2.

Second line.

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |

Tables implemented:

* `DummyClass`
* `DummyClass2`

Tables implemented:

* `DummyClass`
    """

    assert output == expected


def test_no_paths_to_change(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    output = DataBuilderPlugin().on_page_markdown("", None, None, None)

    assert output == ""


def test_one_path_to_change(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contract:dummy_module.DummyClass

!!! backend:DummyBackend1
    """

    output = DataBuilderPlugin().on_page_markdown(markdown, None, None, None)

    expected = """
# this is a page title

## DummyClass

Dummy docstring

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |
| patient_id | a column description | PseudoPatientId | Must have a value, Must be unique. |

Tables implemented:

* `DummyClass`
* `DummyClass2`
    """

    assert output == expected


def test_no_data_file(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/non-existent-data.json")

    with pytest.raises(FileNotFoundError):
        DataBuilderPlugin().on_page_markdown("", None, None, None)


def test_unknown_class(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    with pytest.raises(UnknownClassException):
        DataBuilderPlugin().on_page_markdown(
            "\n!!! backend:UnknownBackend\n", None, None, None
        )

    with pytest.raises(UnknownClassException):
        DataBuilderPlugin().on_page_markdown(
            "\n!!! contract:unknown_module.UnknownClass\n", None, None, None
        )
