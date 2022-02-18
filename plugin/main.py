import json
import os
import pathlib
import re

from mkdocs.plugins import BasePlugin

from .backends import render_backend
from .contracts import render_contract


backends_pat = re.compile(r"\n[\s]*!!!\sbackend:(.*)\n")
contracts_pat = re.compile(r"\n[\s]*!!!\scontract:(.*)\n")

DATA_FILE = os.environ.get("BACKEND_DOCS_FILE", "public_docs.json")


class DataBuilderPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        """
        Replace backend/contract markers with appropriate templates

        on_page_* methods are called for each Page in a mkdocs site (in this
        case, the OpenSAFELY documentation site) and can modify the markdown
        they are given as input.  We're using this method to look for the
        backend and contract markers, defined in the *_pat variables above, and
        lookup the defined classes in the JSON file generated by the
        databuilder.

        For example:

            !!! backend:cohortextractor2.concepts.Patients

        looks up the `cohortextractor2.concepts.Patients` class in the backends
        section of the data file.

        The appropriate template above is then used to render the information
        from the databuilder file into markdown for mkdocs to continue
        processing.
        """
        path = pathlib.Path(DATA_FILE)
        if not path.exists():
            raise FileNotFoundError(f"Expected to find {DATA_FILE} in root directory")

        # load all data from JSON file
        with path.open() as f:
            data = json.load(f)

        for match in backends_pat.findall(markdown):
            backend = render_backend(data, match)
            markdown = markdown.replace(f"!!! backend:{match}", backend)

        # find each matching `!!! dotted.path.Class` string in the markdown
        for match in contracts_pat.findall(markdown):
            contract = render_contract(data, match)
            markdown = markdown.replace(f"!!! contract:{match}", contract)

        return markdown