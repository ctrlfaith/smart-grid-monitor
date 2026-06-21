import time
from datetime import datetime
from config import MONITOR_INTERVAL_SECONDS
from monitor import run_monitor
from reporter import print_summary, export_csv

def run_scheduler() -> None:
    print("⚡ Smart Grid Monitor started. Press Ctrl+C to stop.\n")

    total_runs = 0
    total_alerts = 0

    try:
        while True:
            results = run_monitor()
            print_summary(results)
            export_csv(results)

            total_runs += 1
            total_alerts += sum(1 for r in results if r["severity"] != "INFO")

            print(f"\n⏱️  Next check in {MONITOR_INTERVAL_SECONDS} seconds...")
            time.sleep(MONITOR_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print(f"\n⛔ Stopped by user (Ctrl+C)")
        print(f"📋 Summary: {total_runs} runs completed | {total_alerts} alerts triggered")
        print("✅ System shutdown complete.")

if __name__ == "__main__":
    run_scheduler()