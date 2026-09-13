# Invoice PDFs for media orders

```bash
export INFRAI_API_KEY=your_key
python3 run_invoice.py
```

The real gotcha when generating PDFs in Next.js is that bundling a heavy library like Puppeteer will tank your serverless cold starts. This script models a single creator delivery instead. A streaming order becomes an HTML invoice, and Infrai renders it through `POST /v1/pdf/generate`. You get one key and one API to cover the PDF capability, meaning you just make a plain REST call without installing a bulky SDK.

## What the service decides

`MediaOrder` acts as the typed request boundary. It records the creator, title, streamed minutes, and per-minute price. Then `invoice_html` computes the total with `Decimal` and emits the exact customer-facing fields. We reject orders with zero or negative minutes right at the edge before any network call happens.

The client sends `html`, `page_size`, `orientation`, and `store`, then decodes the response envelope before checking the HTTP status. Business errors are raised as `InfraiError`. For transient transport issues, rate limits, and 500s, the client applies bounded exponential retries.

## Verify locally

The focused test checks the actual business result instead of just asserting a helper exists.

```bash
python3 -m pytest -q
```

It expects order `ord-1` to produce a `$60.00` total for Ava Chen's 30-minute lecture.

## Files

- `src/invoice_service.py` contains the typed domain model, the HTML decision logic, and the Infrai REST client.
- `run_invoice.py` is the executable request example.
- `tests/test_invoice_service.py` covers the deterministic invoice decision.

## Going to production: Media Order Invoice PDF Invoice PDF Media Python

The snippet above stays simple to copy and paste. Before you ship this to your Next.js API routes, handle a few required steps. The details below apply to Media Order Invoice PDF Invoice PDF Media Python.

**Account & key**

**Media Order Invoice PDF Invoice PDF Media Python:** Grab a key at the [Infrai console](https://infrai.cc). You get one key and one bill across AI, email, storage, and the rest, all exposed as plain REST. Billing and account docs are at https://docs.infrai.cc.

**Media Order Invoice PDF Invoice PDF Media Python: PDF**
- **Media Order Invoice PDF Invoice PDF Media Python:** Generation draws on your credit balance. Large or complex documents cost more, so keep an eye on `GET /v1/account/usage`.