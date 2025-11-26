import json

from aiomqtt import Client

from config import settings


async def setup_hass_discovery(client):
    """
    Setup Home Assistant auto-discovery for all sensors
    """

    with open("sensors.json") as f:
        sensors = json.load(f)

    for sensor_id, config in sensors.items():
        # Split sensor_id to get category (player/hero/map)
        category = sensor_id.split("_")[0]

        discovery_topic = (
            f"{settings.HASS_DISCOVERY_PREFIX}/sensor/dota2/{sensor_id}/config"
        )
        state_topic = f"{settings.MQTT_BASE_TOPIC}/{category}"

        discovery_payload = {
            "name": config["name"],
            "unique_id": f"dota2_{sensor_id}",
            "state_topic": state_topic,
            "value_template": config["value_template"],
            "icon": config["icon"],
            "device": {
                "identifiers": ["dota2_gsi"],
                "name": "Dota 2",
                "model": "Game State Integration",
                "manufacturer": "Valve",
            },
        }

        if config["unit"]:
            discovery_payload["unit_of_measurement"] = config["unit"]

        if config["device_class"]:
            discovery_payload["device_class"] = config["device_class"]

        await client.publish(
            discovery_topic, payload=json.dumps(discovery_payload), retain=True
        )
        print(f"✅ Published discovery for {sensor_id}")


async def publish_to_mqtt(client: Client, topic: str, payload: dict):
    """
    Publish data to MQTT
    """
    try:
        await client.publish(topic, payload=json.dumps(payload), qos=1)
    except Exception as e:
        print(f"❌ MQTT publish error: {e}")
