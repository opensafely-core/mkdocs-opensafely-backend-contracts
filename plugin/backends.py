from first import first

from .exceptions import UnknownClassException


backend_template = """
Tables implemented:

{contracts}
"""


def render_backend(data, match):
    # get backend details from data file
    backend_data = first(data["backends"], key=lambda c: c["name"] == match)
    if backend_data is None:
        raise UnknownClassException(f"Unknown class: {match}")

    contracts = "\n".join(f"* `{c}`" for c in sorted(backend_data["tables"]))

    return backend_template.format(
        name=backend_data["name"],
        contracts=contracts,
    ).strip()
