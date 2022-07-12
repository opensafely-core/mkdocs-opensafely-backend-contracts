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


def test_success_no_additional_text(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    markdown = """
# this is a page title

!!! contracts

!!! backend:DummyBackend1

!!! specs
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


## 1 Filtering an event frame


### 1.1 Including rows


#### 1.1.1 Take with column

This example makes use of an event-level table named `e` containing the following data:

| |i1|b1 |
| - | - | - |
| 1|101|T |
| 2|201|T |
| 2|203|F |
| 3|302|F |

```
e.take(e.b1).i1.sum_for_patient()
```
returns the following patient series:

| patient | value |
| - | - |
| 1|203 |
| 2|201 |
| 3| |

    """

    assert output == expected


def test_success_with_multiline_series(monkeypatch):
    monkeypatch.setattr(
        plugin.main, "DATA_FILE", "tests/data_with_multiline_series.json"
    )

    markdown = """
# this is a page title

!!! contracts

!!! backend:DummyBackend1

!!! specs
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


## 1 Logical case expressions


### 1.1 Logical case expressions


#### 1.1.1 Case with expression

This example makes use of a patient-level table named `p` containing the following data:

| patient|i1 |
| - | - |
| 1|6 |
| 2|7 |
| 3|8 |
| 4|9 |
| 5| |

```
case(
    when(p.i1 < 8).then(p.i1),
    when(p.i1 > 8).then(100),
)
```
returns the following patient series:

| patient | value |
| - | - |
| 1|6 |
| 2|7 |
| 3| |
| 4|100 |
| 5| |

    """
    assert output == expected


def test_success_with_additional_text(monkeypatch):
    monkeypatch.setattr(
        plugin.main, "DATA_FILE", "tests/data_with_additional_text.json"
    )

    markdown = """
# this is a page title

!!! contracts

!!! backend:DummyBackend1

!!! specs
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


## 1 Filtering an event frame
Chapters may have additional descriptive text blocks


### 1.1 Including rows
Additional text can also be added at a section level


#### 1.1.1 Take with column
Further additional text can be provided for a paragraph

This example makes use of an event-level table named `e` containing the following data:

| |i1|b1 |
| - | - | - |
| 1|101|T |
| 2|201|T |
| 2|203|F |
| 3|302|F |

```
e.take(e.b1).i1.sum_for_patient()
```
returns the following patient series:

| patient | value |
| - | - |
| 1|203 |
| 2|201 |
| 3| |

    """

    assert output == expected


def test_unknown_class(monkeypatch):
    monkeypatch.setattr(plugin.main, "DATA_FILE", "tests/data.json")

    with pytest.raises(UnknownClassException):
        DataBuilderPlugin().on_page_markdown(
            "\n!!! backend:UnknownBackend\n", None, None, None
        )
