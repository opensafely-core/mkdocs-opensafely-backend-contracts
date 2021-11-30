import json
import pathlib
import re

from first import first
from mkdocs.plugins import BasePlugin


class_path_pat = re.compile(r"\n[\s]*!!!\s(.*)\n")

template = """
# {name}

{docstring}

{columns}

{backend_support}
"""

DATA_FILE = "public_docs.json"


class UnknownClassException(Exception):
    pass


class BackendContractsPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        path = pathlib.Path(DATA_FILE)
        if not path.exists():
            raise FileNotFoundError("Expected backends data file in root directory")

        # load all data from JSON file
        with path.open() as f:
            data = json.load(f)

        # find each matching `!!! dotted.path.Class` string in the markdown
        for match in class_path_pat.findall(markdown):
            # get class details from data file
            class_data = first(data, key=lambda c: c["dotted_path"] == match)
            if class_data is None:
                raise UnknownClassException(f"Unknown class: {match}")

            output = template.format(
                name=class_data["name"],
                docstring=class_data["docstring"],
                columns="",
                backend_support="",
            )

            markdown = markdown.replace(f"!!! {match}", output)

        return markdown
