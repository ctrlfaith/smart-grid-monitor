THRESHOLDS = {
    "MAX_TEMP_CELSIUS": 75.0,
    "MIN_VOLTAGE_V": 210.0,
    "TREND_WINDOW": 3,
    "TREND_RISE_DELTA": 2.0,
}

CB_THRESHOLDS = {
    "MAX_TEMP_CELSIUS": 65.0,
    "MIN_VOLTAGE_V": 210.0,
}

MONITOR_INTERVAL_SECONDS = 10

DEVICES = [
    {"id": "TF-001", "type": "Transformer",     "location": "Substation A"},
    {"id": "TF-002", "type": "Transformer",     "location": "Substation B"},
    {"id": "TF-003", "type": "Transformer",     "location": "Substation C"},
    {"id": "SW-001", "type": "Switch Gear",     "location": "Main Line"},
    {"id": "SW-002", "type": "Switch Gear",     "location": "Secondary Line"},
    {"id": "CB-001", "type": "Circuit Breaker", "location": "Main Panel"},
    {"id": "CB-002", "type": "Circuit Breaker", "location": "Secondary Panel"},
]

# Get Webhook URL from: Discord > Channel Settings > Integrations > Webhooks
DISCORD_WEBHOOK_URL = "your-discord-webhook-url-here"