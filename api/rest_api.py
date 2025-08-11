# rest_api.py - FastAPI wrapper stub
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from model_pipeline.pipeline import main as process_pipeline
import uuid, tempfile, os

app = FastAPI()

@app.post('/process')
async def process_audio(file: UploadFile = File(...)):
    tmp_in = f'/tmp/{uuid.uuid4()}_in.wav'
    tmp_out = f'/tmp/{uuid.uuid4()}_out.wav'
    with open(tmp_in, 'wb') as f:
        f.write(await file.read())
    # Call pipeline - in stubs, pipeline prints fingerprint
    os.system(f'python -m model_pipeline.pipeline --input {tmp_in} --output {tmp_out}')
    # In real impl, load and return structured result
    return JSONResponse({'status':'processed','output':tmp_out})
