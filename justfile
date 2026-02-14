# Run integration tests (requires KSEF credentials in .env)
integration:
    source .env.test && uv run pytest tests/integration/ -v -m integration


sync:
    uv sync --all-groups


test:
    uv run pytest tests/unit/ -v


coverage:
    uv run python scripts/api_coverage.py


lint:
    uv run ruff check src/ tests/

format-check:
    uv run ruff format --check src/ tests/

typecheck:
    #!/usr/bin/env bash
    output=$(uv run basedpyright --level error 2>&1)
    echo "$output"
    echo "$output" | grep -q "0 errors"


fetch-spec:
    wget https://api-test.ksef.mf.gov.pl/docs/v2/openapi.json -O openapi.json


regenerate-models:
    uv run --group codegen datamodel-codegen \
      --input openapi.json \
      --input-file-type openapi \
      --output models.py \
      --output-model-type pydantic_v2.BaseModel \
      --use-annotated \
      --field-constraints \
      --use-standard-collections \
      --use-union-operator \
      --strict-nullable \
      --collapse-root-models \
      --reuse-model \
      --use-schema-description \
      --use-field-description \
      --disable-timestamp \
      --target-python-version 3.12 \
      --output src/ksef2/infra/schema/api/spec.py