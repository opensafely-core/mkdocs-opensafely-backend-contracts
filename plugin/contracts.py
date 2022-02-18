from first import first

from .exceptions import UnknownClassException


contract_template = """
## {name}

{docstring}

| Column name | Description | Type | Constraints |
| ----------- | ----------- | ---- | ----------- |
{columns}


{backend_support}
"""


def render_contract(data, match):
    # get contract details from data file
    contract_data = first(data["contracts"], key=lambda c: c["dotted_path"] == match)
    if contract_data is None:
        raise UnknownClassException(f"Unknown class: {match}")

    docstring = "\n".join(contract_data["docstring"])
    columns = "\n".join(
        f"| {c['name']} | {c['description']} | {c['type']} | {', '.join(c['constraints'])}. |"
        for c in contract_data["columns"]
    )

    return contract_template.format(
        name=contract_data["name"],
        docstring=docstring,
        columns=columns,
        backend_support="",
    ).strip()
