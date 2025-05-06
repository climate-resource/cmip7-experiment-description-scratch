import json
from pathlib import Path

import requests
from pyld import jsonld

HERE = Path(__file__).parent

JSONLD_DIR = HERE / "jsonld"

# with open(JSONLD_DIR / "experiment" / "abrupt-2xco2.json") as fh:
#     abrupt2xco2 = jsonld.expand(json.load(fh))

abrupt2xco2 = jsonld.expand(
    "https://raw.githubusercontent.com/climate-resource/cmip7-experiment-description-scratch/698b95d0c342959b58fee74f914dde8e964de316/jsonld/experiment/abrupt-2xco2.json"
)
print(json.dumps(abrupt2xco2, indent=2))

abrupt2xco2_compacted = jsonld.compact(
    abrupt2xco2,
    "https://raw.githubusercontent.com/climate-resource/cmip7-experiment-description-scratch/698b95d0c342959b58fee74f914dde8e964de316/jsonld/experiment/000_context.jsonld",
)
print(json.dumps(abrupt2xco2_compacted, indent=2))

one_hour_expanded = jsonld.expand(
    "https://raw.githubusercontent.com/WCRP-CMIP/WCRP-universe/refs/heads/esgvoc/frequency/1hr.json"
)
print(json.dumps(one_hour_expanded, indent=2))

for value in one_hour_expanded:
    for key in value:
        if key in ["@id"]:
            urls_to_check = [value[key]]
        elif key in ["@type"]:
            urls_to_check = value[key]
        else:
            urls_to_check = [key]

        for url_to_check in urls_to_check:
            print(url_to_check)
            # Should not give a 404
            response = requests.get(url_to_check, timeout=5)
            try:
                response.raise_for_status()
            except Exception as exc:
                print(f"Error for {key}. {exc}")

one_hour_compact = jsonld.compact(
    one_hour_expanded,
    "https://raw.githubusercontent.com/WCRP-CMIP/WCRP-universe/refs/heads/esgvoc/frequency/000_context.jsonld",
)
print(json.dumps(one_hour_compact, indent=2, sort_keys=True))

one_hour_raw_response = requests.get(
    "https://raw.githubusercontent.com/WCRP-CMIP/WCRP-universe/refs/heads/esgvoc/frequency/1hr.json",
    timeout=5,
)
one_hour_raw = one_hour_raw_response.json()
print(json.dumps(one_hour_raw, indent=2, sort_keys=True))
# compact = {
#     "@context": {
#         "@vocab": "http://schema.org/",
#         "first_name": "givenName",
#         "last_name": "familyName",
#         "alias": "alternateName",
#         "email": "email",
#     },
#     "first_name": "Benjamin",
#     "last_name": "Young",
#     "alias": "BigBlueHat",
#     "email": "byoung@bigbluehat.com",
# }
# expanded = jsonld.expand(compact)
#
# print(json.dumps(expanded, indent=2))
#
#
# compacted = jsonld.compact(expanded, compact["@context"])
#
# print(json.dumps(compacted, indent=2))
#
# expanded_universe = jsonld.expand(
#     "https://raw.githubusercontent.com/WCRP-CMIP/WCRP-universe/refs/heads/esgvoc/frequency/1hr.json"
# )
#
# print(json.dumps(expanded_universe, indent=2))
#
# compacted_universe = jsonld.compact(
#     expanded_universe,
#     "https://raw.githubusercontent.com/WCRP-CMIP/WCRP-universe/refs/heads/esgvoc/frequency/000_context.jsonld",
# )
#
# print(json.dumps(compacted_universe, indent=2))
