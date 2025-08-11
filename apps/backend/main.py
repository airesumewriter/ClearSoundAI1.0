
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uuid, os, tempfile, json, time
from matching import generate_fingerprint, query_index, build_index_from_list
from preprocessing import aaep_process, read_audio_file
from ip_tracker import log_ip_event

app = FastAPI(title='ClearSound1.0 Backend')

@app.post('/api/v1/scan')
async def scan_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file uploaded')
    ext = os.path.splitext(file.filename)[1].lower()
    tmp_in = f"/tmp/{uuid.uuid4().hex}_in{ext}"
    with open(tmp_in, 'wb') as f:
        content = await file.read()
        f.write(content)
    try:
        audio, sr = read_audio_file(tmp_in)
        cleaned, meta = aaep_process(audio, sr)
        fp = generate_fingerprint(cleaned, sr)
        # Log IP event for this scan (example)
        log_ip_event(author='system', title='Scan performed', description=f'Scan of {file.filename} fingerprint={fp}')
    finally:
        try:
            os.remove(tmp_in)
        except:
            pass
    return JSONResponse({'fingerprint': fp, 'sr': sr, 'aaep_meta': meta})

@app.post('/api/v1/match')
async def match_fingerprint(payload: dict):
    fp = payload.get('fingerprint')
    k = int(payload.get('k', 5))
    if not fp:
        return JSONResponse({'error': 'fingerprint required'}, status_code=400)
    try:
        results = query_index(fp, k=k)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)
    return JSONResponse({'results': results})

@app.post('/api/v1/build_index')
async def build_index_endpoint(payload: dict):
    # payload: { "fingerprints": ["hex1","hex2",...] }
    fps = payload.get('fingerprints', [])
    if not isinstance(fps, list) or len(fps) == 0:
        return JSONResponse({'error': 'provide fingerprints list'}, status_code=400)
    path = build_index_from_list(fps)
    log_ip_event(author='system', title='Index built', description=f'Index built with {len(fps)} entries')
    return JSONResponse({'index_path': path})
