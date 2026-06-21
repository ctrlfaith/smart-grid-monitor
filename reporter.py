import csv
from datetime import datetime

def print_summary(results: list[dict]) -> None:
    total = len(results)
    counts = {"CRITICAL": 0, "WARNING": 0, "PRE-WARNING": 0, "ERROR": 0, "INFO": 0}

    for r in results:
        counts[r["severity"]] = counts.get(r["severity"], 0) + 1

    print(f"\n📋 Summary: {total} devices checked | ", end="")
    print(f"✅ {counts['INFO']} normal | ", end="")
    print(f"🔔 {counts['PRE-WARNING']} pre-warning | ", end="")
    print(f"⚠️  {counts['WARNING']} warning | ", end="")
    print(f"🚨 {counts['CRITICAL']} critical | ", end="")
    print(f"❌ {counts['ERROR']} error")

def export_csv(results: list[dict]) -> None:
    filename = "smart_grid_report.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fieldnames = ["timestamp", "id", "type", "location", "temperature", "voltage", "status", "severity", "reason"]

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if f.tell() == 0:
            writer.writeheader()

        for r in results:
            writer.writerow({
                "timestamp": timestamp,
                "id": r["id"],
                "type": r["type"],
                "location": r["location"],
                "temperature": r["temperature"],
                "voltage": r["voltage"],
                "status": r["status"],
                "severity": r["severity"],
                "reason": ", ".join(r["reasons"]),
            })

    print(f"📊 Report exported → {filename}")