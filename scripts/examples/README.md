# Example Scripts

The examples are organized by shape, not just by API area.

- `quickstart.py`: the shortest possible happy path.
- `<domain>/...`: focused examples for one API area such as auth, invoices, or sessions.
- `scenarios/...`: multi-step demos that coordinate test data, multiple actors, or several SDK surfaces in one flow.

Run examples as modules from the repository root.
Use `uv run -m ...`:

```bash
uv run -m scripts.examples.quickstart
uv run -m scripts.examples.invoices.send_invoice
uv run -m scripts.examples.invoices.send_batch
uv run -m scripts.examples.invoices.submit_batch
uv run -m scripts.examples.scenarios.download_purchase_invoices
```
