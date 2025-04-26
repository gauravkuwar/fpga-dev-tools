import hashlib
import json

def is_clock_port(name):
    return name.lower() in ["clk", "clock"]

def get_vector_idx(port_type):
    j, i = port_type.split('(')[-1].replace(')', '').split('downto')
    return int(i), int(j)

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def file_changed(path, hash_file):
    key = str(path)
    current = file_hash(path)
    hashes = {}
    if hash_file.exists():
        hashes = json.loads(hash_file.read_text())
    if hashes.get(key) != current:
        hashes[key] = current
        hash_file.write_text(json.dumps(hashes, indent=2))
        return True
    return False

