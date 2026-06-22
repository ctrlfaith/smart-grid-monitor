import logging
from datetime import datetime
from config import THRESHOLDS, CB_THRESHOLDS
from simulator import generate_sensor_data
from alert import send_alert
from detector import detect as adaptive_detect

logging.basicConfig(
    filename="smart_grid.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_temp_history: dict[str, list[float]] = {}

def _detect_trend(device_id: str, temp: float) -> bool:
    history = _temp_history.setdefault(device_id, [])
    history.append(temp)

    if len(history) > THRESHOLDS["TREND_WINDOW"]:
        history.pop(0)

    if len(history) < THRESHOLDS["TREND_WINDOW"]:
        return False

    return all(
        history[i + 1] - history[i] >= THRESHOLDS["TREND_RISE_DELTA"]
        for i in range(len(history) - 1)
    )

_SEVERITY_RANK = {"CRITICAL": 4, "ERROR": 3, "WARNING": 2, "PRE-WARNING": 1, "INFO": 0}

def _check_device(device: dict) -> dict:
    device_id = device["id"]
    temp = device["temperature"]
    voltage = device["voltage"]
    status = device["status"]

    reasons: list[str] = []
    severities: list[str] = []

    # Select threshold set based on device type.
    # Circuit Breakers use CB_THRESHOLDS (lower max temp); all others use THRESHOLDS.
    thresholds = CB_THRESHOLDS if device.get("type") == "Circuit Breaker" else THRESHOLDS

    if status == "offline":
        return {**device, "severity": "CRITICAL", "reasons": ["OFFLINE"]}

    if temp is None or voltage is None:
        return {**device, "severity": "ERROR", "reasons": ["MISSING DATA"]}

    if temp > thresholds["MAX_TEMP_CELSIUS"]:
        reasons.append("OVERHEAT")
        severities.append("WARNING")

    if voltage < thresholds["MIN_VOLTAGE_V"]:
        reasons.append("BROWNOUT")
        severities.append("WARNING")

    if not reasons and _detect_trend(device_id, temp):
        reasons.append("TEMP RISING TREND")
        severities.append("PRE-WARNING")

    # Adaptive detection always updates baseline.
    # Flags anomaly only when no fixed-threshold alert exists (PRE-WARNING level).
    adaptive_reasons = adaptive_detect(device_id, temp, voltage)
    if not reasons and adaptive_reasons:
        reasons.extend(adaptive_reasons)
        severities.append("PRE-WARNING")

    if not reasons:
        return {**device, "severity": "INFO", "reasons": ["NORMAL"]}

    top_severity = max(severities, key=lambda s: _SEVERITY_RANK[s])
    return {**device, "severity": top_severity, "reasons": reasons}

def run_monitor() -> list[dict]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- ⚡ Smart Grid Monitor | {timestamp} ---")

    devices = generate_sensor_data()
    results = []

    for device in devices:
        result = _check_device(device)
        results.append(result)

        temp_str = f"{result['temperature']}°C" if result['temperature'] is not None else "N/A"
        volt_str = f"{result['voltage']}V" if result['voltage'] is not None else "N/A"

        line = (
            f"[{result['id']}] {result['type']} | "
            f"Temp: {temp_str} | Voltage: {volt_str} | "
            f"Status: {result['status']} → {result['severity']} ({', '.join(result['reasons'])})"
        )

        print(line)
        logging.info(line)

        if result["severity"] != "INFO":
            send_alert(result)

    return results

if __name__ == "__main__":
    from reporter import print_summary
    results = run_monitor()
    print_summary(results)
    print("--- 🏁 Done ---\n")