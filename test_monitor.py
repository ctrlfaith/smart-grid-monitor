import unittest
from unittest.mock import patch
from monitor import _check_device, _detect_trend, _temp_history

class TestAnomalyDetection(unittest.TestCase):

    def setUp(self):
        _temp_history.clear()

    def _make_device(self, temp, voltage, status="online"):
        return {
            "id": "TF-TEST",
            "type": "Transformer",
            "location": "Test Station",
            "temperature": temp,
            "voltage": voltage,
            "status": status,
        }

    # TC-001: Normal values
    def test_normal(self):
        result = _check_device(self._make_device(60.0, 220.0))
        self.assertEqual(result["severity"], "INFO")
        self.assertEqual(result["reasons"], ["NORMAL"])

    # TC-002: Temperature exceeds threshold
    def test_overheat(self):
        result = _check_device(self._make_device(80.0, 220.0))
        self.assertEqual(result["severity"], "WARNING")
        self.assertIn("OVERHEAT", result["reasons"])

    # TC-003: Temperature exactly at threshold (boundary)
    def test_temp_boundary(self):
        result = _check_device(self._make_device(75.0, 220.0))
        self.assertEqual(result["severity"], "INFO")

    # TC-004: Voltage drops below threshold
    def test_brownout(self):
        result = _check_device(self._make_device(60.0, 200.0))
        self.assertEqual(result["severity"], "WARNING")
        self.assertIn("BROWNOUT", result["reasons"])

    # TC-005: Voltage exactly at threshold (boundary)
    def test_voltage_boundary(self):
        result = _check_device(self._make_device(60.0, 210.0))
        self.assertEqual(result["severity"], "INFO")

    # TC-006: Device offline
    def test_offline(self):
        result = _check_device(self._make_device(60.0, 220.0, status="offline"))
        self.assertEqual(result["severity"], "CRITICAL")
        self.assertIn("OFFLINE", result["reasons"])

    # TC-007: Offline overrides warning conditions
    def test_offline_overrides_warning(self):
        result = _check_device(self._make_device(80.0, 200.0, status="offline"))
        self.assertEqual(result["severity"], "CRITICAL")

    # TC-008: Trend detected after 3 consecutive rises
    def test_trend_detected(self):
        _detect_trend("TF-TEST", 68.0)
        _detect_trend("TF-TEST", 70.5)
        result = _check_device(self._make_device(73.0, 220.0))
        self.assertEqual(result["severity"], "PRE-WARNING")
        self.assertIn("TEMP RISING TREND", result["reasons"])

    # TC-009: Trend not triggered with only 2 rounds
    def test_trend_not_enough_rounds(self):
        _detect_trend("TF-TEST", 68.0)
        result = _check_device(self._make_device(70.5, 220.0))
        self.assertEqual(result["severity"], "INFO")

    # TC-010: Trend not triggered if rise is not continuous
    def test_trend_not_continuous(self):
        _detect_trend("TF-TEST", 68.0)
        _detect_trend("TF-TEST", 72.0)
        result = _check_device(self._make_device(70.0, 220.0))
        self.assertEqual(result["severity"], "INFO")

    # TC-011: Edge case — missing temperature (None)
    def test_missing_temperature(self):
        result = _check_device(self._make_device(None, 220.0))
        self.assertNotEqual(result["severity"], None)
        self.assertIn("MISSING DATA", result["reasons"])

    # TC-012: Edge case — unknown status
    def test_unknown_status(self):
        result = _check_device(self._make_device(60.0, 220.0, status="unknown"))
        self.assertIsNotNone(result["severity"])

    # TC-013: Both overheat and brownout detected simultaneously
    def test_overheat_and_brownout(self):
        result = _check_device(self._make_device(80.0, 200.0))
        self.assertEqual(result["severity"], "WARNING")
        self.assertIn("OVERHEAT", result["reasons"])
        self.assertIn("BROWNOUT", result["reasons"])
        self.assertEqual(len(result["reasons"]), 2)

    # TC-014: Trend detection is skipped when a WARNING condition already exists
    def test_trend_skipped_when_warning_exists(self):
        _detect_trend("TF-TEST", 68.0)
        _detect_trend("TF-TEST", 70.5)
        result = _check_device(self._make_device(80.0, 220.0))  # overheat triggers WARNING
        self.assertEqual(result["severity"], "WARNING")
        self.assertIn("OVERHEAT", result["reasons"])
        self.assertNotIn("TEMP RISING TREND", result["reasons"])


if __name__ == "__main__":
    unittest.main(verbosity=2)