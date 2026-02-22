"""Extract the API version from openapi.json and write it to _openapi.py."""

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OPENAPI_PATH = ROOT / "openapi.json"
OUTPUT_PATH = ROOT / "src" / "ksef2" / "_openapi.py"

MARKER = "**Wersja API:** "


def extract_openapi_version(spec: dict[str, Any]) -> str:
    return spec["openapi"]


def extract_ksef_api_version(spec: dict[str, Any]) -> str:
    description: str = spec["info"]["description"]
    start = description.index(MARKER) + len(MARKER)
    end = description.index(" ", start)
    return description[start:end]


def main() -> None:

    with open(OPENAPI_PATH, "r") as file:
        spec = json.load(file)

        openapi_version = extract_openapi_version(spec)
        ksef_api_version = extract_ksef_api_version(spec)

    to_write = f'''
__openapi_version__ = "{openapi_version}"
__ksef_api_version__ = "{ksef_api_version}"
'''

    _ = OUTPUT_PATH.write_text(to_write)


if __name__ == "__main__":
    main()
