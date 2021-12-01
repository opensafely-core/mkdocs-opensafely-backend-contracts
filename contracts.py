import json
import os
import pathlib
import re

from first import first
from mkdocs.plugins import BasePlugin


backends_pat = re.compile(r"\n[\s]*!!!\sbackend:(.*)\n")
contracts_pat = re.compile(r"\n[\s]*!!!\scontract:(.*)\n")

backend_template = """
## {name}

{contracts}
"""
contract_template = """
## {name}

{docstring}

{columns}

{backend_support}
"""

DATA_FILE = os.environ.get("BACKEND_DOCS_FILE", "public_docs.json")


class UnknownClassException(Exception):
    pass


class BackendContractsPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        path = pathlib.Path(DATA_FILE)
        if not path.exists():
            raise FileNotFoundError(f"Expected to find {DATA_FILE} in root directory")

        # load all data from JSON file
        with path.open() as f:
            data = json.load(f)

        for match in backends_pat.findall(markdown):
            # get backend details from data file
            backend_data = first(data["backends"], key=lambda c: c["name"] == match)
            if backend_data is None:
                raise UnknownClassException(f"Unknown class: {match}")

            contracts = ", ".join(f"`{c}`" for c in backend_data["tables"])

            output = backend_template.format(
                name=backend_data["name"],
                contracts=contracts,
            ).strip()

            markdown = markdown.replace(f"!!! backend:{match}", output)

        # find each matching `!!! dotted.path.Class` string in the markdown
        for match in contracts_pat.findall(markdown):
            # get contract details from data file
            contract_data = first(
                data["contracts"], key=lambda c: c["dotted_path"] == match
            )
            if contract_data is None:
                raise UnknownClassException(f"Unknown class: {match}")

            output = contract_template.format(
                name=contract_data["name"],
                docstring=contract_data["docstring"],
                columns="",
                backend_support="",
            ).strip()

            markdown = markdown.replace(f"!!! contract:{match}", output)

        return markdown
