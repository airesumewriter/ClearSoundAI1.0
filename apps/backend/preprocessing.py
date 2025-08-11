
import numpy as np
import time
def aaep_process(audio, sr):
    # AAEP stub: normalize, simple denoise placeholder, return metadata
    try:
        # normalize
        maxv = max(abs(audio)) if hasattr(audio,'__len__') and len(audio)>0 else 1.0
        if maxv > 0:
            audio = audio / float(maxv)
    except Exception:
        pass
    # placeholder processing time
    time.sleep(0.01)
    meta = {'processed_at': time.time(), 'sr': sr, 'notes': 'AAEP stub applied'}
    return audio, meta

def read_audio_file(path):
    # lightweight reader; prefer soundfile if available
    try:
        import soundfile as sf
        data, sr = sf.read(path, always_2d=False)
        if hasattr(data, 'ndim') and data.ndim > 1:
            data = data.mean(axis=1)
        return data, int(sr)
    except Exception:
        # fallback: read binary and return dummy array
        with open(path, 'rb') as f:
            b = f.read()
        return [0]*16000, 16000
