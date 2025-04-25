# Offload quartus cmds to windows
from fabric import Connection
from pathlib import Path, PurePosixPath
from invoke.exceptions import UnexpectedExit
import subprocess
import hashlib
import json
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from helper.config import (
    HASH_FILE,
    REMOTE_HOST,
    SSH_KEY_PATH,
    REMOTE_DIR
    )

# === UTILS ===
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def should_send(path):
    key = str(path)
    current = file_hash(path)
    hashes = {}
    if HASH_FILE.exists():
        hashes = json.loads(HASH_FILE.read_text())
    if hashes.get(key) != current:
        hashes[key] = current
        HASH_FILE.write_text(json.dumps(hashes, indent=2))
        return True
    return False

def sync_files(input_files: list[str]):
    print("Syncing files...")
    for f in input_files:
        local_path = Path(f)
        if local_path.is_file() and not should_send(local_path):
            print(f"Skipping unchanged: {f}")
            continue
        
        remote_f_dir = REMOTE_DIR / PurePosixPath(f).parent if local_path.is_file() else REMOTE_DIR / PurePosixPath(f)
        print(f"Syncing {f} to {remote_f_dir}/")

        subprocess.run(
            f'ssh -i "{SSH_KEY_PATH}" {REMOTE_HOST} '
            f'"bash.exe -c \\"mkdir -p {remote_f_dir}\\""',
            shell=True, check=True
        )

        subprocess.run(
            f'scp -q -i "{SSH_KEY_PATH}" -r "{f}" {REMOTE_HOST}:{remote_f_dir}',
            shell=True, check=True
        )

def run(cmd: str, dir: str = REMOTE_DIR):
    print(f"Running '{cmd}' in dir: {dir} remotely...")
    conn = Connection(REMOTE_HOST, connect_kwargs={"key_filename": str(SSH_KEY_PATH)})
    
    try:
        with conn.cd(str(REMOTE_DIR / dir)):
            # check for interrupts
            cmd_wrapped = f"bash -c 'trap \"echo __INTERRUPTED__; exit 130\" INT TERM; {cmd}'"
            result = conn.run(cmd_wrapped, pty=True, hide=False, warn=True)
            if result.stdout.splitlines()[-1] == "__INTERRUPTED__":
                return -1
    except UnexpectedExit as e:
        print(f"\nRemote command failed: {cmd}")
        print(f"Exit code: {e.result.exited}")
        return -1
    
def get_output_files(dir: str):
    conn = Connection(REMOTE_HOST, connect_kwargs={"key_filename": str(SSH_KEY_PATH)})
    remote_dir_path = REMOTE_DIR / dir

    try:
        result = conn.run(f"bash -c \"ls -p {remote_dir_path} | grep -v /\"", hide=True)
        output_files = result.stdout.strip().splitlines()

        for f in output_files:
            local_path = dir / Path(f)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            remote_file = remote_dir_path / Path(f)
            
            try:
                print(f"Fetching {remote_file} to {local_path}...")
                conn.get(str(remote_file), local=str(local_path))
            except Exception as e:
                print(f"Skipped fetching {remote_file}: {e}")
    except UnexpectedExit as e:
        print(f"\nRemote command failed while fetching outputing files")
        print(f"Exit code: {e.result.exited}")
        return -1
