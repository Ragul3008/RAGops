import subprocess
import os
import sys
import time
import psutil

# ── Venv guard ────────────────────────────────────────────────────────────────
# Ensure this script always runs inside the project's virtual environment.
# If launched with the wrong Python (e.g. system Python), we re-exec ourselves
# under the venv interpreter automatically.
_VENV_PYTHON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ".venv", "Scripts", "python.exe"
)
if os.path.exists(_VENV_PYTHON) and os.path.abspath(sys.executable) != os.path.abspath(_VENV_PYTHON):
    print(f"[INFO] Not running in venv. Re-launching with: {_VENV_PYTHON}")
    import subprocess
    sys.exit(subprocess.run([_VENV_PYTHON] + sys.argv).returncode)
# ──────────────────────────────────────────────────────────────────────────────

# Target ports to free up
TARGET_PORTS = [8000, 8001, 8002, 8003, 8501]

def kill_port_processes():
    print("[INFO] Scanning and clearing active ports:", TARGET_PORTS)
    killed = set()
    try:
        # Scan connections using psutil
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.port in TARGET_PORTS and conn.pid:
                pid = conn.pid
                if pid not in killed:
                    try:
                        proc = psutil.Process(pid)
                        print(f"[INFO] Killing process {proc.name()} (PID: {pid}) running on port {conn.laddr.port}")
                        proc.kill()
                        killed.add(pid)
                    except Exception as e:
                        print(f"[WARN] Failed to kill process {pid}: {e}")
    except Exception as e:
        print(f"[WARN] psutil connection scan failed ({e}), falling back to netstat command...")
        for port in TARGET_PORTS:
            try:
                out = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode('utf-8', errors='ignore')
                for line in out.splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        pid = int(parts[-1])
                        if pid > 0 and pid not in killed:
                            print(f"[INFO] Killing process with PID {pid} on port {port}...")
                            subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            killed.add(pid)
            except Exception:
                pass
    print("[INFO] Port cleanup completed.")

# Services definitions
scripts_dir = os.path.dirname(sys.executable)
celery_path = os.path.join(scripts_dir, "celery.exe")
streamlit_path = os.path.join(scripts_dir, "streamlit.exe")

SERVICES = [
    {
        "name": "Auth Service",
        "env_override": {"PYTHONPATH": "services/auth;services/shared"},
        "args": [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000", "--host", "127.0.0.1"]
    },
    {
        "name": "Embedding Service",
        "env_override": {"PYTHONPATH": "services/embedding;services/shared"},
        "args": [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8001", "--host", "127.0.0.1"]
    },
    {
        "name": "Evaluation Service",
        "env_override": {"PYTHONPATH": "services/evaluation;services/shared"},
        "args": [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8002", "--host", "127.0.0.1"]
    },
    {
        "name": "RAG Engine Service",
        "env_override": {"PYTHONPATH": "services/rag-engine;services/shared"},
        "args": [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8003", "--host", "127.0.0.1"]
    },
    {
        "name": "Celery Worker",
        "env_override": {"PYTHONPATH": "services/evaluation;services/shared"},
        "args": [celery_path, "-A", "app.workers", "worker", "-Q", "embedding,evaluation", "--pool=solo", "--loglevel=info"]
    }
]

STREAMLIT_SERVICE = {
    "name": "Streamlit Dashboard",
    "env_override": {},
    "args": [streamlit_path, "run", "streamlit_app.py", "--server.port", "8501"]
}

def wait_for_port(port, host="127.0.0.1", timeout=15):
    import socket
    print(f"[INFO] Waiting for service on port {port} to start...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"[OK] Service on port {port} is ready.")
                return True
        except (TimeoutError, ConnectionRefusedError):
            time.sleep(0.5)
    print(f"[WARN] Service on port {port} did not start within {timeout} seconds.")
    return False

def main():
    # 1. Clean ports first to prevent socket binding errors
    kill_port_processes()
    
    # 2. Launch processes
    processes = []
    print("\n[INFO] Starting all backend services...")
    for s in SERVICES:
        # Build environment
        env = os.environ.copy()
        if s["env_override"]:
            for k, v in s["env_override"].items():
                env[k] = v
                
        print(f"[STARTING] {s['name']}...")
        try:
            # We start it as a subprocess redirecting outputs to stdout
            p = subprocess.Popen(
                s["args"],
                env=env,
                stdout=None, # Share stdout/stderr with the main runner console
                stderr=None
            )
            processes.append((s["name"], p))
        except Exception as e:
            print(f"[ERROR] Failed to start {s['name']}: {e}")
            
    # Wait for API ports before launching Streamlit Dashboard
    print("\n[INFO] Verifying backend services are ready before starting Dashboard...")
    for port in [8000, 8001, 8002, 8003]:
        wait_for_port(port)
        
    print(f"[STARTING] {STREAMLIT_SERVICE['name']}...")
    try:
        env = os.environ.copy()
        p = subprocess.Popen(
            STREAMLIT_SERVICE["args"],
            env=env,
            stdout=None, # Share stdout/stderr with the main runner console
            stderr=None
        )
        processes.append((STREAMLIT_SERVICE["name"], p))
    except Exception as e:
        print(f"[ERROR] Failed to start {STREAMLIT_SERVICE['name']}: {e}")
        
    print("\n[OK] All backend services launched! Streamlit is available at http://localhost:8501.")
    print("Press Ctrl+C to terminate all services simultaneously.\n")
    
    try:
        # 3. Monitor running processes
        while True:
            time.sleep(1)
            for name, p in processes:
                poll = p.poll()
                if poll is not None:
                    print(f"[CRASH] Service '{name}' exited unexpectedly with code {poll}!")
                    # Remove it from monitoring to prevent spam
                    processes.remove((name, p))
    except KeyboardInterrupt:
        print("\n[INFO] Terminating all backend processes...")
        for name, p in processes:
            print(f"[STOPPING] {name}...")
            try:
                p.terminate()
                p.wait(timeout=2)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        print("[OK] All processes stopped. Goodbye!")

if __name__ == "__main__":
    main()
