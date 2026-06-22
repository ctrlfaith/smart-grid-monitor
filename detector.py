"""
detector.py — Adaptive Anomaly Detection (Sprint 7)
Z-Score based detector that learns per-device baseline from historical data.
Runs alongside fixed-threshold logic in monitor.py without replacing it.
"""

import math
from collections import defaultdict

# Minimum number of data points before Z-Score detection activates.
# Below this, the detector returns None (not enough baseline data).
MIN_SAMPLES = 10

# Z-Score threshold — values beyond this are flagged as anomalies.
# 2.5 is chosen to reduce false positives on noisy sensor data.
Z_SCORE_THRESHOLD = 2.5

# Rolling window size per device (keeps memory bounded).
WINDOW_SIZE = 50

# Internal store: device_id -> {"temp": [...], "voltage": [...]}
_history: dict[str, dict[str, list[float]]] = defaultdict(lambda: {"temp": [], "voltage": []})


def _push(values: list[float], value: float) -> None:
    """Append value to rolling window, evict oldest if over limit."""
    values.append(value)
    if len(values) > WINDOW_SIZE:
        values.pop(0)


def _z_score(values: list[float], value: float) -> float | None:
    """Return Z-Score of value against the list. Returns None if not enough data."""
    if len(values) < MIN_SAMPLES:
        return None
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std = math.sqrt(variance)
    if std == 0:
        return 0.0
    return abs((value - mean) / std)


def detect(device_id: str, temp: float | None, voltage: float | None) -> list[str]:
    """
    Run adaptive detection on a single device reading.
    Updates internal history, then checks Z-Score for temp and voltage.
    Returns a list of adaptive reason strings (may be empty).
    """
    store = _history[device_id]
    reasons: list[str] = []

    if temp is not None:
        z = _z_score(store["temp"], temp)
        _push(store["temp"], temp)
        if z is not None and z > Z_SCORE_THRESHOLD:
            reasons.append(f"ADAPTIVE TEMP ANOMALY (z={z:.2f})")

    if voltage is not None:
        z = _z_score(store["voltage"], voltage)
        _push(store["voltage"], voltage)
        if z is not None and z > Z_SCORE_THRESHOLD:
            reasons.append(f"ADAPTIVE VOLTAGE ANOMALY (z={z:.2f})")

    return reasons


def get_baseline(device_id: str) -> dict:
    """Return current baseline stats for a device (for logging/debug)."""
    store = _history[device_id]
    result = {}
    for metric, values in store.items():
        if len(values) >= 2:
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            result[metric] = {
                "samples": len(values),
                "mean": round(mean, 2),
                "std": round(math.sqrt(variance), 2),
            }
        else:
            result[metric] = {"samples": len(values), "mean": None, "std": None}
    return result


def clear_history(device_id: str | None = None) -> None:
    """Clear history for one device or all devices (used in tests)."""
    if device_id:
        _history[device_id] = {"temp": [], "voltage": []}
    else:
        _history.clear()