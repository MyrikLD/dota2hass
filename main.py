import json
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from aiomqtt import Client
from fastapi import Depends, FastAPI, Request

from schemas import DotaGameState


async def mqtt_client():
    async with Client(MQTT_BROKER, port=MQTT_PORT) as client:
        yield client


MqttClient = Annotated[Client, Depends(mqtt_client)]
mqtt_client = asynccontextmanager(mqtt_client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Dota 2 GSI to MQTT...")
    async with mqtt_client() as client:
        await setup_hass_discovery(client)

    print("✅ MQTT discovery configured")
    yield


app = FastAPI(title="Dota 2 GSI to MQTT", lifespan=lifespan)

# MQTT Config
MQTT_BROKER = "192.168.1.160"  # Your MQTT broker
MQTT_PORT = 1883
MQTT_BASE_TOPIC = "dota2"
HASS_DISCOVERY_PREFIX = "homeassistant"


async def setup_hass_discovery(client):
    """
    Setup Home Assistant auto-discovery for all sensors
    """

    with open('sensors.json') as f:
        sensors = json.load(f)

    for sensor_id, config in sensors.items():
        # Split sensor_id to get category (player/hero/map)
        category = sensor_id.split('_')[0]

        discovery_topic = f"{HASS_DISCOVERY_PREFIX}/sensor/dota2/{sensor_id}/config"
        state_topic = f"{MQTT_BASE_TOPIC}/{category}"

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
                "manufacturer": "Valve"
            }
        }

        if config["unit"]:
            discovery_payload["unit_of_measurement"] = config["unit"]

        if config["device_class"]:
            discovery_payload["device_class"] = config["device_class"]

        await client.publish(
            discovery_topic,
            payload=json.dumps(discovery_payload),
            retain=True
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


@app.post("/")
async def receive_gamestate(request: Request, client: MqttClient):
    """
    Receive game state from Dota 2
    """
    try:
        data = await request.json()
        if data['hero'] == {"id": 0}:
            data["hero"] = None
        gs = DotaGameState(**data)

        # Publish to MQTT
        if gs.player:
            await publish_to_mqtt(client, f"{MQTT_BASE_TOPIC}/player", gs.player.model_dump())

        if gs.hero:
            await publish_to_mqtt(client, f"{MQTT_BASE_TOPIC}/hero", gs.hero.model_dump())

        if gs.map:
            await publish_to_mqtt(client, f"{MQTT_BASE_TOPIC}/map", gs.map.model_dump())

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=4000,
        log_level="info"
    )
