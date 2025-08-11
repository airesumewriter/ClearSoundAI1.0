
import numpy as np, hashlib, os, json
INDEX_PATH = '/data/index/clearsound_faiss.index'
META_PATH = '/data/index/clearsound_index_meta.npy'

def fingerprint_to_vector(fp_hex):
    try:
        b = bytes.fromhex(fp_hex)
    except Exception:
        # fallback: hash the string and use bytes
        b = hashlib.sha256(fp_hex.encode('utf-8')).digest()
    vec = np.frombuffer(b, dtype=np.uint8).astype('float32')
    if vec.size < 64:
        vec = np.pad(vec, (0, 64 - vec.size), 'constant')
    else:
        vec = vec[:64]
    vec = vec / 255.0
    return vec

# Try to import faiss if available
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    faiss = None
    FAISS_AVAILABLE = False

def build_index_from_list(fingerprint_list):
    os.makedirs('/data/index', exist_ok=True)
    if FAISS_AVAILABLE:
        vecs = np.stack([fingerprint_to_vector(fp) for fp in fingerprint_list]).astype('float32')
        dim = vecs.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(vecs)
        faiss.write_index(index, INDEX_PATH)
        np.save(META_PATH, np.array(fingerprint_list))
        return INDEX_PATH
    else:
        # fallback: save meta only for simple linear search
        import numpy as _np
        _np.save(META_PATH, _np.array(fingerprint_list))
        return META_PATH

def load_index_meta():
    if not os.path.exists(META_PATH):
        return None
    data = np.load(META_PATH, allow_pickle=True)
    return data.tolist()

def query_index(fp_hex, k=5):
    meta = load_index_meta()
    if meta is None:
        raise RuntimeError('Index not built. Please build the index first.')
    if FAISS_AVAILABLE:
        index = faiss.read_index(INDEX_PATH)
        vec = fingerprint_to_vector(fp_hex).reshape(1, -1).astype('float32')
        D, I = index.search(vec, k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            results.append({'meta': meta[idx].item() if hasattr(meta[idx],'item') else meta[idx], 'distance': float(dist)})
        return results
    else:
        # simple Hamming-like distance over bytes as fallback
        qv = fingerprint_to_vector(fp_hex)
        scores = []
        for i, m in enumerate(meta):
            mv = fingerprint_to_vector(m)
            dist = float(((qv - mv)**2).sum())
            scores.append((i, dist))
        scores.sort(key=lambda x: x[1])
        results = []
        for idx, dist in scores[:k]:
            results.append({'meta': meta[idx], 'distance': float(dist)})
        return results

def generate_fingerprint(audio, sr):
    # simple placeholder fingerprint: SHA256 of first 1s of audio bytes + sr
    try:
        import numpy as np
        segment = audio[:min(len(audio), sr)]
        b = segment.tobytes()
    except Exception:
        b = str(audio)[:1024].encode('utf-8')
    h = hashlib.sha256(b + str(sr).encode('utf-8')).hexdigest()
    return h
