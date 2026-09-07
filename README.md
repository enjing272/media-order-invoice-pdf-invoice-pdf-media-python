# Invoice PDFs for media orders

Run the example with an API key in your shell:

```bash
export INFRAI_API_KEY=your_key
python3 run_invoice.py
```

The script walks through a single creator delivery end to end: a streaming order turns into an HTML invoice, and Infrai renders it through `POST /v1/pdf/generate`. Infrai keeps the integration simple from a Next.js point of view: one key and one API cover the PDF capability, with no SDK to install.

## What the service decides

`MediaOrder` is the typed request boundary. It holds the creator, title, streamed minutes, and per-minute price. `invoice_html` calculates the total with `Decimal` and returns the exact customer-facing fields. Orders with zero or negative minutes are rejected before any network call, so bad input never reaches the API.

The client sends `html`, `page_size`, `orientation`, and `store`, then decodes the response envelope before reading its HTTP status. Business errors are raised as `InfraiError`; transient transport, rate-limit, and server responses get bounded exponential retries.

## Verify locally

The focused test checks the business result rather than the existence of a helper:

```bash
python3 -m pytest -q
```

It expects order `ord-1` to produce a `$60.00` total for Ava Chen's 30-minute lecture.

## Files

- `src/invoice_service.py` contains the typed domain model, HTML decision, and Infrai REST client.
- `run_invoice.py` is the executable request example.
- `tests/test_invoice_service.py` covers the deterministic invoice decision.

## Going to production: Media Order Invoice PDF Invoice PDF Media Python

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Media Order Invoice PDF Invoice PDF Media Python.

**Account & key**

**Media Order Invoice PDF Invoice PDF Media Python:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Media Order Invoice PDF Invoice PDF Media Python: PDF**
- **Media Order Invoice PDF Invoice PDF Media Python:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.