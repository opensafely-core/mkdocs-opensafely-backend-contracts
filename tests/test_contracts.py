import pytest

import contracts
from contracts import BackendContractsPlugin, UnknownClassException


def test_multiple_paths_to_change(monkeypatch):
    monkeypatch.setattr(contracts, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contract:dummy_module.DummyClass

!!! contract:dummy_module2.DummyClass2

!!! backend:DummyBackend1

!!! backend:DummyBackend2
    """

    output = BackendContractsPlugin().on_page_markdown(markdown, None, None, None)

    expected = """
# this is a page title

## DummyClass

Dummy docstring

## DummyClass2

Dummy docstring2.

Second line.

## DummyBackend1

`DummyClass`, `DummyClass2`

## DummyBackend2

`DummyClass`
    """

    assert output == expected


def test_no_paths_to_change(monkeypatch):
    monkeypatch.setattr(contracts, "DATA_FILE", "tests/data.json")

    output = BackendContractsPlugin().on_page_markdown("", None, None, None)

    assert output == ""


def test_one_path_to_change(monkeypatch):
    monkeypatch.setattr(contracts, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contract:dummy_module.DummyClass

!!! backend:DummyBackend1
    """

    output = BackendContractsPlugin().on_page_markdown(markdown, None, None, None)

    expected = """
# this is a page title

## DummyClass

Dummy docstring

## DummyBackend1

`DummyClass`, `DummyClass2`
    """

    assert output == expected


def test_no_data_file(monkeypatch):
    monkeypatch.setattr(contracts, "DATA_FILE", "tests/non-existent-data.json")

    with pytest.raises(FileNotFoundError):
        BackendContractsPlugin().on_page_markdown("", None, None, None)


def test_unknown_class(monkeypatch):
    monkeypatch.setattr(contracts, "DATA_FILE", "tests/data.json")

    with pytest.raises(UnknownClassException):
        BackendContractsPlugin().on_page_markdown(
            "\n!!! backend:UnknownBackend\n", None, None, None
        )

    with pytest.raises(UnknownClassException):
        BackendContractsPlugin().on_page_markdown(
            "\n!!! contract:unknown_module.UnknownClass\n", None, None, None
        )
