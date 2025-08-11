
ClearSound1.0 - Backend (FAISS matching, AAEP stub, IP Tracker)

Quick start (WSL / Linux):
1. cd ~/clearsound1.0/apps/backend
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
   # if faiss-cpu fails to install on your platform, remove it from requirements and use the fallback search
5. Start the server:
   uvicorn main:app --reload --port 8000

Endpoints:
- POST /api/v1/scan  (multipart file upload) -> returns fingerprint & AAEP meta
- POST /api/v1/match  (JSON: { "fingerprint": "<hex>", "k": 5}) -> returns match results
- POST /api/v1/build_index (JSON: { "fingerprints": ["hex1","hex2",...] }) -> builds index

Data directories:
- /data/index  -> FAISS index and metadata (persistent if using Docker volume)
- /data/logs   -> IP tracker logs (jsonl)

IP Tracker:
- ip_tracker.log_ip_event(author, title, description) records a jsonl entry with sha256 hash for provenance.
