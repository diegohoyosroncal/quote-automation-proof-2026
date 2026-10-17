# Supplier Quote Automation — tested synthetic proof

**Ten automated tests passed on the exact code published here** (see [execution receipt](evidence/2026-10-16_execution_receipt.json)). This is a reproducible synthetic-data demo, **not** a paid customer deployment or an n8n/WhatsApp integration.

## Have a supplier-price or quotation workflow to automate?

**[Request a scoped paid pilot by email](mailto:diegohoyos2024@gmail.com?subject=Paid%20Pilot%20Inquiry%20-%20Supplier%20Quotes)**

Tell us (using fictional or redacted examples; **never email secrets or customer personal information**):

- Current input format (CSV, Excel export, email, etc.) and desired output.
- Number of suppliers, approximate rows, business rules and required exception flags.
- Acceptance tests and target delivery date.

A first paid milestone can cover **CSV normalization, price/stock validation, anomaly and duplicate detection, quotation draft generation, tests and written handoff**. Exact scope, fixed price, payment arrangements, and acceptance criteria are agreed **before** implementation. No one is billed by this repository; it does not collect payments.

**Looking for a ready-made digital tool instead of a custom implementation?** [AR and invoice tracker (Excel, US$11.90)](https://whop.com/ar-tracker/products/accounts-receivable-tracker-for-small-business-excel/) or [WhatsApp sales follow-up kit (US$10.90)](https://whop.com/ar-tracker/products/kit-express-whatsapp-sales-collections-system-for-small-business/). These are separate downloadable products, not capabilities built into this demo.

---

## Run

```bash
python -m unittest -v test_motor.py
python motor.py --out resultados
```

Only standard Python is needed. No customer data, credentials, payment, internet, external APIs or messaging services are used.

## Deliverables

- `motor.py` — validation, margin, supplier comparison and quote-draft generation
- `test_motor.py` — 10 executable tests
- `resultados/catalogo_demo.csv`, `alertas_demo.json`, `cotizacion_demo.txt`, `registro_prueba.json` generated locally

The demonstration does **not** import real supplier lists, convert RFQ PDFs, send WhatsApp messages, run in n8n or access Google Sheets. Those integrations must be scoped separately against a buyer's approved data schema and environment. Human supplier price approval remains the buyer's own business control; this is not the owner's labor.

Built as a no-human-labor-on-the-seller-side, buyer-evaluable technical demonstration. Seller owner: Diego Hoyos, Lima, Peru.
