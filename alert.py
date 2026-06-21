import requests
from config import DISCORD_WEBHOOK_URL

_ICONS = {
    "CRITICAL":    "🚨",
    "WARNING":     "⚠️",
    "PRE-WARNING": "🔔",
    "ERROR":       "❌",
}

def send_alert(device: dict) -> None:
    severity = device["severity"]
    icon = _ICONS.get(severity, "ℹ️")

    temp_str = f"{device['temperature']}°C" if device['temperature'] is not None else "N/A"
    volt_str = f"{device['voltage']}V" if device['voltage'] is not None else "N/A"

    for reason in device["reasons"]:
        message = (
            f"{icon} [{severity}] {device['id']} | "
            f"{device['type']} | {device['location']} | "
            f"{reason} | Temp: {temp_str} | Voltage: {volt_str}"
        )
        print(f"  → ALERT: {message}")
        _send_discord(message)

def _send_discord(message: str) -> None:
    if not DISCORD_WEBHOOK_URL:
        return

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=5,
        )
        if response.status_code != 204:
            print(f"  → Discord error: {response.status_code}")
    except Exception as e:
        print(f"  → Discord unreachable: {e}")