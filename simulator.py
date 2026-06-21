import random
from config import DEVICES, THRESHOLDS

_trend_counters: dict[str, int] = {device["id"]: 0 for device in DEVICES}

def _get_base_temp(device_id: str) -> float:
    if _trend_counters[device_id] > 0:
        base = 75.0 - (THRESHOLDS["TREND_WINDOW"] * THRESHOLDS["TREND_RISE_DELTA"])
        delta = _trend_counters[device_id] * THRESHOLDS["TREND_RISE_DELTA"]
        _trend_counters[device_id] += 1
        return round(base + delta, 1)
    return round(random.uniform(50.0, 74.0), 1)

def generate_sensor_data() -> list[dict]:
    results = []

    for device in DEVICES:
        device_id = device["id"]

        # Randomly trigger scenarios for demo purposes
        scenario = random.choices(
            ["normal", "overheat", "brownout", "offline", "trend"],
            weights=[50, 10, 10, 10, 20],
            k=1
        )[0]

        if scenario == "overheat":
            temp = round(random.uniform(76.0, 95.0), 1)
            voltage = round(random.uniform(215.0, 230.0), 1)
            status = "online"
        elif scenario == "brownout":
            temp = round(random.uniform(50.0, 74.0), 1)
            voltage = round(random.uniform(180.0, 209.0), 1)
            status = "online"
        elif scenario == "offline":
            temp = None
            voltage = None
            status = "offline"
        elif scenario == "trend":
            _trend_counters[device_id] = 1
            temp = _get_base_temp(device_id)
            voltage = round(random.uniform(215.0, 230.0), 1)
            status = "online"
        else:
            temp = round(random.uniform(50.0, 74.0), 1)
            voltage = round(random.uniform(215.0, 230.0), 1)
            status = "online"

        results.append({
            "id": device_id,
            "type": device["type"],
            "location": device["location"],
            "temperature": temp,
            "voltage": voltage,
            "status": status,
        })

    return results