#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : LaptopMonitor – HDD, CPU, Network, Files        ###
###                 Real-time system insights using psutil, ping, speedtest ###
###  Date         : 24-10-2025                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import os
import time
import logging
import threading
import platform
import pathlib
import psutil
from ping3 import ping
import speedtest
from datetime import datetime

class LaptopMonitor:
    def __init__(self):
        # Folder path override
        self.folder_path = os.getenv("MONITOR_FOLDER_PATH") or str(pathlib.Path(__file__).resolve().parent.parent.parent)

        # Core parameters
        self.ping_host = os.getenv("PING_HOST", "google.com")
        self.interval = int(os.getenv("MONITOR_INTERVAL", "10"))
        self.max_cycles = int(os.getenv("MAX_CYCLES", "0"))  # 0 = unlimited

        # Optional toggles
        self.enable_speedtest = os.getenv("ENABLE_SPEEDTEST", "true").lower() == "true"

        # Logging level
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(level=getattr(logging, log_level, logging.INFO), format='%(message)s')

        # Process keywords override
        default_keywords = ["chrome", "firefox", "edge", "notepad", "word", "excel", "powerpnt",
                            "python", "vscode", "teams", "zoom", "skype", "explorer", "cmd"]
        raw_keywords = os.getenv("PROCESS_KEYWORDS")
        self.process_keywords = [k.strip().lower() for k in raw_keywords.split(",")] if raw_keywords else default_keywords

        # Monitor map
        self.monitors = {
            "🖴 Disk Space"         : self.monitor_disk_space,
            "📁 Files"              : self.monitor_files,
            "🌐 Network Usage"      : self.monitor_network_usage,
            "📶 Network Latency"    : self.monitor_network_latency,
            "⏱️ Speed Test"         : self.monitor_speed_test if self.enable_speedtest else self.skip_speed_test,
            "🧠 CPU Usage"          : self.monitor_cpu_usage,
            "⚙️ Processes"          : self.monitor_processes,
            "🧭 Active Interfaces"  : self.monitor_active_interfaces,
        }

    def monitor_disk_space(self):
        try:
            path = os.environ.get('SystemDrive', '/') if platform.system() == 'Windows' else '/'
            disk_usage = psutil.disk_usage(path)
            gb = 1024 ** 3
            logging.info(f"  Total : {disk_usage.total / gb:.2f} GB | Used : {disk_usage.used / gb:.2f} GB | Free : {disk_usage.free / gb:.2f} GB | Usage : {disk_usage.percent}%")
        except Exception as e:
            logging.warning(f"  ⚠️ Disk monitoring failed: {e}")

    def monitor_files(self):
        total_size = 0
        file_count = 0
        if not os.path.exists(self.folder_path):
            logging.warning(f"  ❌ Folder not found: {self.folder_path}")
            return
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    logging.info(f"  {file_path} ({size} bytes)")
                    total_size += size
                    file_count += 1
                except Exception as e:
                    logging.warning(f"  ⚠️ Error accessing {file}: {e}")
        logging.info(f"  📊 Total Files: {file_count} | Total Size: {total_size} bytes")

    def monitor_network_usage(self):
        stats = psutil.net_io_counters(pernic=True)
        for iface, data in stats.items():
            logging.info(f"  [{iface}] Sent: {data.bytes_sent} | Received: {data.bytes_recv}")

    def monitor_active_interfaces(self):
        stats = psutil.net_if_stats()
        active = [name for name, s in stats.items() if s.isup]
        for name in active:
            iface = stats[name]
            logging.info(f"  {name} → Speed: {iface.speed} Mbps | MTU: {iface.mtu}")
        logging.info(f"  Active: {', '.join(active)}")

    def monitor_network_latency(self):
        hosts = [self.ping_host, "cloudflare.com", "1.1.1.1"]
        for host in hosts:
            try:
                latency = ping(host)
                if latency is not None:
                    logging.info(f"  Ping to {host}: {latency:.2f} ms")
                    break
                else:
                    logging.warning(f"  ⚠️ No response from {host}")
            except Exception as e:
                logging.warning(f"  ⚠️ Ping failed for {host}: {e}")

    def monitor_cpu_usage(self):
        model = platform.processor() or platform.uname().processor
        usage = psutil.cpu_percent(interval=1)
        logging.info(f"  Model: {model} | Usage: {usage}%")

    def monitor_processes(self):
        seen = set()
        for proc in psutil.process_iter(['name', 'pid', 'memory_info']):
            try:
                name = proc.info['name'].lower()
                if any(k in name for k in self.process_keywords) and name not in seen:
                    mem = proc.info['memory_info'].rss / (1024 ** 2)
                    logging.info(f"  🔹 {name} | PID: {proc.info['pid']} | RAM: {mem:.2f} MB")
                    seen.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def monitor_speed_test(self):
        logging.info("  Running… please wait.")
        def run_speedtest():
            try:
                st = speedtest.Speedtest()
                server = st.get_best_server()
                down = st.download() / 1_000_000
                up = st.upload() / 1_000_000
                logging.info(f"  Server: {server['host']} ({server['name']})")
                logging.info(f"  ↓ Download: {down:.2f} Mbps | ↑ Upload: {up:.2f} Mbps")
            except Exception as e:
                logging.warning(f"  ⚠️ Speed test failed: {e}")
        thread = threading.Thread(target=run_speedtest)
        thread.daemon = True
        thread.start()
        thread.join(timeout=10)
        if thread.is_alive():
            logging.warning("  ⚠️ Speed test timed out.")

    def skip_speed_test(self):
        logging.info("  ⏱️ Speed test skipped (ENABLE_SPEEDTEST=false).")

    def prompt_quit(self):
        try:
            user_input = input("🔧 Type 'q' to quit or press Enter to continue: ").strip().lower()
            return user_input == 'q'
        except EOFError:
            return False

    def run_all(self):
        logging.info("\n🖥️ LaptopMonitor – Real-time Stats\n")
        cycle = 1
        try:
            while True:
                if self.max_cycles and cycle > self.max_cycles:
                    logging.info(f"\n📴 Reached MAX_CYCLES={self.max_cycles}. Exiting.")
                    break

                logging.info(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} – Starting Cycle #{cycle}")
                for label, func in self.monitors.items():
                    logging.info(f"\n▶️ {label}")
                    func()

                logging.info(f"\n✅ Cycle #{cycle} complete. Sleeping for {self.interval} seconds…\n")

                if cycle % 3 == 0:
                    if self.prompt_quit():
                        logging.info("👋 Exiting on user request.")
                        break

                cycle += 1
                time.sleep(self.interval)

        except KeyboardInterrupt:
            logging.info("\n🚫 Monitoring interrupted by user.")
        finally:
            logging.info("✅ Cleanup complete. Exiting gracefully.")
