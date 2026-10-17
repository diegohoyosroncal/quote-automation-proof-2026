# AI-assisted supplier quoting — reproducible synthetic proof

This **portfolio demo is synthetic**. It is not a completed customer contract, a production n8n deployment, or evidence of paid sales.

The Python engine processes 10 fictional suppliers, 50 valid catalogue items and 1 deliberately invalid item. It applies a minimum gross margin, detects anomalous price changes, ranks in-stock matches, writes a quote draft (clearly marked **DEMO — DO NOT SEND**) and creates a traceable output report.

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
