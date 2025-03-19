"""
Fill out the auto-generated sections in our experiment description pages
"""

from __future__ import annotations

from pathlib import Path

import cmipld
from attrs import define

DOCS_DIR = Path(__file__).parents[1] / "docs"


@define
class ExperimentDescriptionFile:
    """Experiment description file"""

    experiment_name: str
    """Name of the experiment"""

    experiment_one_line_description: str
    """One-line description of the experiment"""

    experiment_longer_description: str
    """Longer (than one line) description of the experiment"""

    @classmethod
    def from_raw_lines(cls, raw_lines: list[str]) -> ExperimentDescriptionFile:
        """
        Initialise from raw file lines
        """
        # breakpoint()

    def to_markdown(self) -> str:
        """
        Convert the information held by self to a markdown representation

        Returns
        -------
        :
            Markdown representation of the information in self
        """
        out_l = [
            "<!--- This file contains a number of sections -->",
            "<!--- They are bounded by comments like this -->",
            "<!--- Do not edit these sections by hand -->",
            "<!--- Start title -->",
            f"# {self.experiment_name}",
            "",
            "<!--- End title -->",
            "<!--- Start one-line-description -->",
            "## One-line description",
            self.experiment_one_line_description,
            "",
            "<!--- End one-line-description -->",
            "<!--- Start longer-description -->",
            "## Longer description",
            self.experiment_longer_description,
            "",
            "<!--- End longer-description -->",
        ]

        return "\n".join(out_l)


def main() -> None:
    """
    Run the script
    """
    GRAPH_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/graph.jsonld"
    CONTEXT_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/_context_"

    data = cmipld.jsonld.frame(GRAPH_URL, CONTEXT_URL)

    for entry in data["@graph"]:
        experiment_name = entry["label"]
        if experiment_name != "abrupt-2xCO2":
            continue

        doc_file = DOCS_DIR / f"{experiment_name}.md"

        # with open(doc_file) as fh:
        #     start = fh.readlines()
        # breakpoint()
        experiment_description = ExperimentDescriptionFile(
            experiment_name=experiment_name,
            experiment_one_line_description=entry["long-label"],
            experiment_longer_description=entry["description"],
        )
        with open(doc_file, "w") as fh:
            fh.write(experiment_description.to_markdown())


if __name__ == "__main__":
    main()
