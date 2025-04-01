"""
Fill out the auto-generated sections in our experiment description pages
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cmipld
from attrs import asdict, define

HERE = Path(__file__).parent
DOCS_DIR = HERE.parents[0] / "docs"


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


def get_info(in_id: str) -> dict[str, Any]:
    """
    Get info from its ID
    """
    # This doesn't feel very portable to me, but maybe it is?
    cv_location, tmp = in_id.split(":")
    facet, label = tmp.split("/")

    url_base = f"{cmipld.locations.mapping[cv_location]}/{facet}"
    GRAPH_URL = f"{url_base}/graph.jsonld"
    CONTEXT_URL = f"{url_base}/_context_"

    data_facet = cmipld.jsonld.frame(GRAPH_URL, CONTEXT_URL)
    # This should not be needed.
    # The issue is that the parent-activity varies by entry.
    # For example, here it uses the ID: https://github.com/WCRP-CMIP/CMIP7-CVs/blob/main/src-data/experiment/esm-scen7-h-ext.json
    # Here it uses the label: https://github.com/WCRP-CMIP/CMIP7-CVs/blob/main/src-data/experiment/esm-scen7-h.json
    in_id_lower = in_id.lower()
    info_l = [v for v in data_facet["@graph"] if v["id"] == in_id_lower]
    if len(info_l) != 1:
        raise AssertionError

    info = info_l[0]

    return info


@define
class OtherExperimentInfo:
    """Other experiment info that may or may not be missing"""

    parent_experiment: str | None = None
    """Parent experiment"""

    parent_experiment_activity: str | None = None
    """Parent experiment activity"""


def get_other_experiment_info(
    raw_lines: list[str], start_position: int
) -> tuple[OtherExperimentInfo, int]:
    """Get other experiment info from the raw text"""
    exp_end_block = "<!--- End other-experiment-info -->"
    mapping = {
        "Parent experiment": "parent_experiment",
        "Parent experiment activity": "parent_experiment_activity",
    }

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


def get_wrapped_esgf_url_for_source_id(source_ids: list[str]) -> str:
    """
    Get a wrapped ESGF URL for a given source ID
    """
    source_id_str = ", ".join(source_ids)
    source_id_search = "%22%2C%22".join(source_ids)

    return (
        f"[{source_id_str}](https://aims2.llnl.gov/search?project=input4MIPs&versionType=all&&"
        f"activeFacets=%7B%22source_id%22%3A%5B%22{source_id_search}%22%5D%7D)"
    )


@define
class ForcingInfo:
    """Forcing information for use in these docs"""

    shorthand: str
    """Short-hand used to refer to the forcing"""

    source_ids: list[str]
    """Source ID(s) of the forcing"""

    further_information: str | None = None
    """Further details/information"""


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

    parent_experiment_activity: str | None
    """Parent experiment activity"""

    forcings_info: tuple[ForcingInfo, ...] | None
    """
    Forcings info

    Keys should be the short-hand for the forcing,
    values should be the source IDs from which those forcings should be retrieved.
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

        # i = read_until(
        #     raw_lines=raw_lines,
        #     line="<!--- Start forcings -->",
        #     start_position=i,
        # )
        # i_end_forcings_block = read_until(
        #     raw_lines=raw_lines,
        #     line="<!--- End forcings -->",
        #     start_position=i,
        # )
        # forcings_section = "\n".join(raw_lines[i + 1 : i_end_forcings_block])

        return cls(
            experiment_name=experiment_name,
            experiment_one_line_description=experiment_one_line_description,
            experiment_longer_description=experiment_longer_description,
            forcings_info=None,
            # forcings_section=forcings_section,
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
            out_l.append(f"Parent experiment: {self.parent_experiment}")
        if self.parent_experiment_activity is not None:
            out_l.append(
                f"Parent experiment activity: {self.parent_experiment_activity}"
            )

        forcings_lines = [
            "## Forcings",
            "",
            "The forcings required for this experiment are listed below.",
            "For each forcing, we provide a short-hand/common name,",
            "followed by the source ID from which this forcing should be retrieved.",
            "Where relevant, we also provide further information.",
            "",
            "<!--- Start forcings -->",
        ]
        for forcing_info in self.forcings_info:
            if forcing_info.shorthand == "aerosol-optical-properties":
                source_id_url = "Available outside ESGF"

            elif forcing_info.source_ids is None:
                source_id_url = "Not available yet"

            else:
                source_id_url = get_wrapped_esgf_url_for_source_id(
                    forcing_info.source_ids
                )

            fi_l = [
                f"- {forcing_info.shorthand}: {source_id_url}",
            ]
            if forcing_info.further_information is not None:
                fi_l.append(
                    f"    - Further information: {forcing_info.further_information}"
                )

            forcings_lines.extend(fi_l)

        forcings_lines.append(
            "<!--- End forcings -->",
        )

        source_ids = []
        for fi in self.forcings_info:
            if fi.shorthand == "aerosol-optical-properties":
                continue

            if fi.source_ids is not None:
                source_ids.extend(fi.source_ids)

        esgpull_download_lines = [
            "## Getting the data",
            "",
            "If you install [esgpull](https://esgf.github.io/esgf-download/),",
            "you can download all the data associated with the source IDs above",
            "with the script shown below.",
            "Note that this will download all the data",
            "associated with these source IDs,",
            "which is likely to be much more data",
            "than you actually need to run your model.",
            "",
            "```sh",
            "#!/bin/bash",
            "",
            f'EXPERIMENT_NAME="{self.experiment_name}"',
            "",
            f"esgpull add --track --tag ${{EXPERIMENT_NAME}} source_id:{','.join(source_ids)}",  # noqa: E501
            "esgpull update --tag ${EXPERIMENT_NAME} --yes",
            "esgpull download --tag ${EXPERIMENT_NAME}",
            "```",
        ]

        out_l.extend(
            [
                "<!--- End other-experiment-info -->",
                "",
                *forcings_lines,
                "",
                *esgpull_download_lines,
                "",
            ]
        )

        return "\n".join(out_l)


def main() -> None:
    """
    Run the script
    """
    GRAPH_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/graph.jsonld"
    CONTEXT_URL = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP7-CVs/refs/heads/main/src-data/experiment/_context_"

    EXPERIMENT_TO_FORCINGS_FILE = (
        HERE.parents[0] / "input-data" / "experiment-to-forcings.json"
    )
    FORCINGS_TO_SOURCE_ID_FILE = (
        HERE.parents[0] / "input-data" / "forcings-to-source-id.json"
    )

    with open(EXPERIMENT_TO_FORCINGS_FILE) as fh:
        experiment_to_forcings = json.load(fh)

    with open(FORCINGS_TO_SOURCE_ID_FILE) as fh:
        forcings_to_source_id = json.load(fh)

    data = cmipld.jsonld.frame(GRAPH_URL, CONTEXT_URL)

    experiment_files_l = []
    for entry in data["@graph"]:
        experiment_name = entry["label"]
        if experiment_name not in [
            "historical",
            "piControl",
            "abrupt-2xCO2",
            "abrupt-4xCO2",
        ]:
            # Don't generate for now
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
            info = {}

        info["experiment_name"] = experiment_name
        info["experiment_one_line_description"] = entry["long-label"]
        info["experiment_longer_description"] = entry["description"]

        parent_experiment_id = entry["parent-experiment"]
        if isinstance(parent_experiment_id, str):
            if parent_experiment_id == "cmip7:experiment/none":
                info["parent_experiment"] = None
                info["parent_experiment_activity"] = None
            else:
                parent_info = get_info(parent_experiment_id)
                info["parent_experiment"] = parent_info["label"]
                parent_activity_info = get_info(parent_info["activity"])
                info["parent_experiment_activity"] = parent_activity_info["label"]

        forcings_shorthand = experiment_to_forcings[experiment_name]
        forcings_info = tuple(
            ForcingInfo(shorthand=sh, **forcings_to_source_id[sh])
            for sh in forcings_shorthand
        )
        info["forcings_info"] = forcings_info
        experiment_description = ExperimentDescriptionFile(**info)

        doc_file.parent.mkdir(exist_ok=True, parents=True)
        with open(doc_file, "w") as fh:
            fh.write(experiment_description.to_markdown())

        experiment_files_l.append(doc_file)


if __name__ == "__main__":
    main()
