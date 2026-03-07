"""Extract the API version from openapi.json and write it to __openapi_version__.py."""

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OPENAPI_PATH = ROOT / "openapi.json"
OUTPUT_PATH = ROOT / "src" / "ksef2" / "__openapi_version__.py"

MARKER = "**Wersja API:** "


def extract_openapi_version(spec: dict[str, Any]) -> str:
    return spec["openapi"]


def extract_ksef_api_version(spec: dict[str, Any]) -> str:
    description: str = spec["info"]["description"]
    start = description.index(MARKER) + len(MARKER)
    end = description.index(" ", start)
    return description[start:end]


def main() -> None:
    spec = json.loads(OPENAPI_PATH.read_text())
    version = extract_ksef_api_version(spec)
    _ = OUTPUT_PATH.write_text(f'version = "{version}"\n')
    print(f'Set version = "{version}" in {OUTPUT_PATH.relative_to(ROOT)}')


if __name__ == "__main__":
    main()
