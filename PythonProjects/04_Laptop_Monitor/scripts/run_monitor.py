import sys
import pathlib
from dotenv import load_dotenv

# Load .env from project root
env_path = pathlib.Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded environment from {env_path}")
else:
    print("⚠️  .env file not found. Using default configuration.\n")

print("""
📦 LaptopMonitor Configuration Options (.env):

PING_HOST           → Host to ping (default: google.com)
MONITOR_INTERVAL    → Delay between cycles in seconds (default: 10)
MAX_CYCLES          → Max monitoring cycles before auto-exit (default: 0 = unlimited)

MONITOR_FOLDER_PATH → Override folder path for file monitoring
ENABLE_SPEEDTEST    → Toggle speed test on/off (true or false, default: true)
LOG_LEVEL           → Logging level (INFO, DEBUG, WARNING, etc., default: INFO)
PROCESS_KEYWORDS    → Comma-separated process names to monitor (default: chrome, vscode, etc.)
""")

# Add 'src' to Python path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from laptopmonitor.laptop_monitor import LaptopMonitor

def main():
    monitor = LaptopMonitor()
    monitor.run_all()

if __name__ == "__main__":
    main()
