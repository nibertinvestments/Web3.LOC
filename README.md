# Web3.LOC
Web3 contracts being compiled into the Web3 Library of Congress (not government, just scope inspiration).

## Opportunity Scout Pipeline (High-Demand / Low-Supply Problem Discovery)

This repository now also contains a data pipeline to surface underserved software problem niches you can build into revenue streams.

### Pipeline Stages
1. Collect Google Autocomplete suggestions (`data_collect/google_autocomplete.py`).
2. Normalize & deduplicate phrases (`processing/normalize.py`).
3. Embed + cluster semantically (`processing/embed_cluster.py`).
4. Simulate demand & supply signals, compute opportunity scores (`processing/scoring.py`).
5. Output CSV + JSON reports (`reports/`).

### Quick Start (Windows PowerShell)
Create & activate a virtual environment, install dependencies, then run the pipeline script.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\scripts\run_pipeline.ps1 -SkipInstall
```

Outputs (after run):
- `data/autocomplete.jsonl`
- `data/queries_clean.jsonl`
- `data/clusters.csv`
- `reports/opportunities_simulated.csv`
- `reports/top10.json`

### Tests
```powershell
pytest -q
```

### Secret Handling & Security
Use a real `.env` file (never committed) for API keys and credentials. This repo omits any sample `.env.example` to avoid accidental production key leakage. Add `.env` to your local `.gitignore` (already present) and supply only actual keys you control. Rotate keys immediately if ever exposed.

### Next Steps
- Replace simulated metrics with real Reddit / StackOverflow / GitHub collectors.
- Add SERP/API based supply measurement.
- Enhance scoring with pain signal extraction.

---

Original scope (Web3 contract library) remains; pipeline lives alongside and can help identify smart-contract tooling gaps.
