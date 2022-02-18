from first import first

from .exceptions import UnknownClassException


contract_template = """
## {name}

{docstring}

{columns}


{backend_support}
"""


def render_contract(data, match):
    # get contract details from data file
    contract_data = first(data["contracts"], key=lambda c: c["dotted_path"] == match)
    if contract_data is None:
        raise UnknownClassException(f"Unknown class: {match}")

    docstring = "\n".join(contract_data["docstring"])

    return contract_template.format(
        name=contract_data["name"],
        docstring=docstring,
        columns="",
        backend_support="",
    ).strip()
