"""
Fill out the auto-generated sections in our experiment description pages
"""

from __future__ import annotations

from pathlib import Path

import cmipld
from attrs import asdict, define

DOCS_DIR = Path(__file__).parents[1] / "docs"


def read_until(raw_lines: list[str], line: str, start_position: int) -> int:
    """Read until a specific line is found"""
    for i, file_line in enumerate(raw_lines[start_position:]):
        if file_line == line:
            return i + start_position

    msg = (
        f"Missing expected line: {line}. "
        f"Raw text: {'\n'.join(raw_lines[start_position:])}"
    )
    raise ValueError(msg)


def get_experiment_name(raw_lines: list[str], start_position: int) -> tuple[str, int]:
    """Get the experiment name from the raw lines"""
    exp_end_block = "<!--- End title -->"
    if raw_lines[start_position + 2].strip() != exp_end_block:
        raise AssertionError(raw_lines[start_position + 2])

    line_to_parse = raw_lines[start_position + 1]
    try:
        experiment_name = line_to_parse.lstrip("# ").strip()
    except ValueError:
        print(line_to_parse)
        raise

    return experiment_name, start_position + 3


def get_experiment_one_line_description(
    raw_lines: list[str], start_position: int
) -> tuple[str, int]:
    """Get the experiment one-line description from the raw lines"""
    exp_end_block = "<!--- End one-line-description -->"
    if raw_lines[start_position + 2].strip() != exp_end_block:
        raise AssertionError(raw_lines[start_position + 2])

    line_to_parse = raw_lines[start_position + 1]
    try:
        experiment_one_line = line_to_parse.strip()
    except ValueError:
        print(line_to_parse)
        raise

    return experiment_one_line, start_position + 3


def get_experiment_longer_description(
    raw_lines: list[str], start_position: int
) -> tuple[str, int]:
    """Get the experiment longer-description from the raw lines"""
    exp_end_block = "<!--- End longer-description -->"

    longer_description_l = []
    for i, line in enumerate(raw_lines[start_position + 1 :]):
        if line.strip() == exp_end_block:
            break

        longer_description_l.append(line.strip())

    else:
        msg = (
            f"Missing expected end of block delimiter: {exp_end_block}. "
            f"Raw text: {'\n'.join(raw_lines[start_position:])}"
        )
        raise ValueError(msg)

    return "\n".join(longer_description_l), start_position + i


@define
class OtherExperimentInfo:
    """Other experiment info that may or may not be missing"""

    parent_experiment: str | None = None


def get_other_experiment_info(
    raw_lines: list[str], start_position: int
) -> tuple[OtherExperimentInfo, int]:
    """Get other experiment info from the raw text"""
    exp_end_block = "<!--- End other-experiment-info -->"
    mapping = {"Parent experiment": "parent_experiment"}

    other_experiment_info_d = {}
    for i, line in enumerate(raw_lines[start_position + 1 :]):
        if line.strip() == exp_end_block:
            break

        toks = line.split(": ")
        other_experiment_info_d[mapping[toks[0]]] = toks[1]

    else:
        msg = (
            f"Missing expected end of block delimiter: {exp_end_block}. "
            f"Raw text: {'\n'.join(raw_lines[start_position:])}"
        )
        raise ValueError(msg)

    return OtherExperimentInfo(**other_experiment_info_d), start_position + i


@define
class ExperimentDescriptionFile:
    """Experiment description file"""

    experiment_name: str
    """Name of the experiment"""

    experiment_one_line_description: str
    """One-line description of the experiment"""

    experiment_longer_description: str
    """Longer (than one line) description of the experiment"""

    parent_experiment: str | None
    """Parent experiment of this experiment"""

    forcings_section: str
    """
    Section on forcings

    Placeholder until we generate this section automatically
    """

    @classmethod
    def from_raw_lines(
        cls, raw_lines: list[str], max_exp: int = int(1e4)
    ) -> ExperimentDescriptionFile:
        """
        Initialise from raw file lines
        """
        i = read_until(
            raw_lines=raw_lines, line="<!--- Start title -->", start_position=0
        )
        experiment_name, i = get_experiment_name(raw_lines, i)

        i = read_until(
            raw_lines=raw_lines,
            line="<!--- Start one-line-description -->",
            start_position=i,
        )
        experiment_one_line_description, i = get_experiment_one_line_description(
            raw_lines, i
        )

        i = read_until(
            raw_lines=raw_lines,
            line="<!--- Start longer-description -->",
            start_position=i,
        )
        experiment_longer_description, i = get_experiment_longer_description(
            raw_lines, i
        )

        i = read_until(
            raw_lines=raw_lines,
            line="<!--- Start other-experiment-info -->",
            start_position=i,
        )
        other_experiment_info, i = get_other_experiment_info(raw_lines, i)

        i = read_until(
            raw_lines=raw_lines,
            line="<!--- Start forcings -->",
            start_position=i,
        )
        i_end_forcings_block = read_until(
            raw_lines=raw_lines,
            line="<!--- End forcings -->",
            start_position=i,
        )
        forcings_section = "\n".join(raw_lines[i + 1 : i_end_forcings_block])

        return cls(
            experiment_name=experiment_name,
            experiment_one_line_description=experiment_one_line_description,
            experiment_longer_description=experiment_longer_description,
            forcings_section=forcings_section,
            **asdict(other_experiment_info),
        )

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
            "<!--- End title -->",
            "",
            "## One-line description",
            "",
            "<!--- Start one-line-description -->",
            self.experiment_one_line_description,
            "<!--- End one-line-description -->",
            "",
            "## Longer description",
            "",
            "<!--- Start longer-description -->",
            self.experiment_longer_description,
            "<!--- End longer-description -->",
            "",
            "## Other experiment info",
            "",
            "<!--- Start other-experiment-info -->",
        ]

        if self.parent_experiment is not None:
            out_l.extend(
                [
                    f"Parent experiment: {self.parent_experiment}",
                ]
            )

        out_l.extend(
            [
                "<!--- End other-experiment-info -->",
                "",
                "## Forcings",
                "",
                "<!--- Start forcings -->",
                self.forcings_section,
                "<!--- End forcings -->",
                "",
                "## Generating the data",
                "",
                "<!--- TODO: auto-generate this -->",
            ]
        )

        return "\n".join(out_l)


def main() -> None:
    """
    Run the script
    """
    GRAPH_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/graph.jsonld"
    CONTEXT_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/_context_"

    data = cmipld.jsonld.frame(GRAPH_URL, CONTEXT_URL)

    experiment_files_l = []
    for entry in data["@graph"]:
        experiment_name = entry["label"]
        if (
            not experiment_name.startswith("abrupt")
            and not experiment_name.startswith("historical")
            and not experiment_name.startswith("piControl")
        ):
            continue

        doc_file = DOCS_DIR / "experiment_overviews" / f"{experiment_name}.md"

        if doc_file.exists():
            with open(doc_file) as fh:
                raw_lines = fh.readlines()

            experiment_description = ExperimentDescriptionFile.from_raw_lines(
                [line.strip() for line in raw_lines]
            )
            info = asdict(experiment_description)

        else:
            info = {"forcings_section": "TBD"}

        info["experiment_name"] = experiment_name
        info["experiment_one_line_description"] = entry["long-label"]
        info["experiment_longer_description"] = entry["description"]
        info["parent_experiment"] = entry["parent-experiment"]
        experiment_description = ExperimentDescriptionFile(**info)

        doc_file.parent.mkdir(exist_ok=True, parents=True)
        with open(doc_file, "w") as fh:
            fh.write(experiment_description.to_markdown())

        experiment_files_l.append(doc_file)


if __name__ == "__main__":
    main()
