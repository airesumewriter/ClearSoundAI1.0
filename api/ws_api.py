# ws_api.py - websocket stub using FastAPI
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get('/')
async def homepage():
    return HTMLResponse('<html><body>WebSocket stub</body></html>')

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text('Connected to ClearSound AI model WS stub')
    await websocket.close()
