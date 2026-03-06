import json
import sys
from pathlib import Path

from ksef2 import endpoints
from ksef2.core.routes import ALL_ROUTES

OPENAPI_PATH = Path(__file__).resolve().parent.parent / "openapi.json"
BADGE_PATH = Path(__file__).resolve().parent.parent / "coverage.json"


def load_openapi_endpoints() -> set[str]:
    with open(OPENAPI_PATH) as f:
        spec = json.load(f)
    return {path for path, methods in spec["paths"].items() for method in methods}


def badge_color(pct: int) -> str:
    if pct >= 80:
        return "44cc11"
    if pct >= 60:
        return "dfb317"
    if pct >= 40:
        return "fe7d37"
    return "e05d44"


def main() -> None:
    api_endpoints = load_openapi_endpoints()
    sdk_endpoints = set(map(str, ALL_ROUTES))
    covered = set(ALL_ROUTES) & api_endpoints
    total = len(api_endpoints)
    count = len(covered)
    pct = round(count / total * 100) if total else 0

    badge = {
        "schemaVersion": 1,
        "label": "KSeF API coverage",
        "message": f"{count} / {total} ({pct}%)",
        "color": badge_color(pct),
    }

    with open(BADGE_PATH, "w") as f:
        json.dump(badge, f, indent=2)
        f.write("\n")

    print(json.dumps(badge, indent=2))

    missing = sorted(api_endpoints - sdk_endpoints)
    if missing:
        print(f"\nMissing endpoints ({len(missing)}):")
        for path in missing:
            print(f"    {path}")

    extra = sorted(sdk_endpoints - api_endpoints)
    if extra:
        print(f"\nSDK endpoints not in OpenAPI ({len(extra)}):")
        for path in extra:
            print(f"    {path}")

    sys.exit(0 if pct == 100 else 1)


if __name__ == "__main__":
    main()
