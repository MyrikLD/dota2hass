# Dota 2 to Home Assistant Bridge

Bridge Dota 2 Game State Integration with Home Assistant via MQTT. Track game statistics in real-time.

## Quick Start

```bash
docker run -d \
  --name dota2hass \
  -p 8000:8000 \
  -e MQTT_BROKER=your-mqtt-ip \
  ghcr.io/myrikld/dota2hass:latest
```

## Dota 2 Configuration

To enable Game State Integration in Dota 2, create a configuration file:

**Location**: `steamapps/common/dota 2 beta/game/dota/cfg/gamestate_integration/gamestate_integration_hass.cfg`

**Content**:
```
"Dota 2 Integration Configuration"
{
    "uri"           "http://YOUR_SERVER_IP:8000/"
    "timeout"       "5.0"
    "buffer"        "0.1"
    "throttle"      "0.1"
    "heartbeat"     "30.0"
    "data"
    {
        "provider"      "0"
        "map"           "1"
        "player"        "1"
        "hero"          "1"
        "abilities"     "0"
        "items"         "0"
    }
}
```

Replace `YOUR_SERVER_IP` with the IP address where this service is running.

## Available Sensors

Sensors automatically appear in Home Assistant under device "Dota 2":
- **Player**: Kills, deaths, assists, GPM, XPM, gold, last hits, denies
- **Hero**: Name, level, health/mana, position, status effects, items
- **Map**: Game time, day/night, game state, team scores, match ID

## Development

```bash
# Install dependencies
uv sync

# Run locally
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Build Docker image
docker build -t dota2hass .
```

## Configuration

| Variable                      | Default            | Description            |
|-------------------------------|--------------------|------------------------|
| `MQTT_BROKER`                 | `192.168.1.160`    | MQTT broker IP         |
| `MQTT_PORT`                   | `1883`             | MQTT broker port       |
| `MQTT_BASE_TOPIC`             | `dota2`            | MQTT broker port       |
| `HASS_DISCOVERY_PREFIX`       | `homeassistant`    | MQTT broker port       |