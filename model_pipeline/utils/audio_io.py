# audio_io.py - simple audio I/O helpers (requires soundfile)
import soundfile as sf
def load_wav(path):
    data, sr = sf.read(path)
    return data, sr
def save_wav(path, data, sr):
    sf.write(path, data, sr)
