
import json, os, hashlib, time, uuid
LOG_DIR = '/data/logs'
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'ip_log.jsonl')

def compute_hash(entry):
    s = json.dumps(entry, sort_keys=True).encode('utf-8')
    return hashlib.sha256(s).hexdigest()

def log_ip_event(author, title, description, files=None, tags=None):
    entry = {
        'id': str(uuid.uuid4()),
        'author': author,
        'title': title,
        'description': description,
        'files': files or [],
        'tags': tags or [],
        'timestamp': time.time()
    }
    entry['sha256'] = compute_hash(entry)
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry['sha256']

def list_logs(limit=100):
    if not os.path.exists(LOG_FILE):
        return []
    out = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                out.append(json.loads(line.strip()))
            except:
                pass
    return out[-limit:]
