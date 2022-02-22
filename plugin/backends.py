from first import first

from .exceptions import UnknownClassException


backend_template = """
Contracts implemented:

{contracts}
"""


def render_backend(data, match):
    # get backend details from data file
    backend_data = first(data["backends"], key=lambda c: c["name"] == match)
    if backend_data is None:
        raise UnknownClassException(f"Unknown class: {match}")

    contracts = [
        (c, c.lower().replace("/", "")) for c in sorted(backend_data["contracts"])
    ]
    contracts = "\n".join(
        f"* [`{name}`](contracts-reference.md#{link})" for name, link in contracts
    )

    return backend_template.format(
        name=backend_data["name"],
        contracts=contracts,
    ).strip()
