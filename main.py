import logging
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from aiomqtt import Client
from fastapi import Depends, FastAPI
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from hass_tools import publish_to_mqtt, setup_hass_discovery
from schemas import DotaGameState


async def mqtt_client():
    async with Client(settings.MQTT_BROKER, port=settings.MQTT_PORT) as client:
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
last_msg = {}


@app.post("/")
async def receive_gamestate(client: MqttClient, gs: DotaGameState):
    """
    Receive game state from Dota 2
    """
    global last_msg

    last_msg = gs.model_dump(mode="json", exclude_unset=True)

    try:
        # Publish to MQTT
        if gs.player:
            await publish_to_mqtt(
                client, f"{settings.MQTT_BASE_TOPIC}/player", gs.player.model_dump()
            )

        if gs.hero:
            await publish_to_mqtt(
                client, f"{settings.MQTT_BASE_TOPIC}/hero", gs.hero.model_dump()
            )

        if gs.map:
            await publish_to_mqtt(
                client, f"{settings.MQTT_BASE_TOPIC}/map", gs.map.model_dump()
            )

        return {"status": "ok"}

    except Exception as e:
        logging.exception(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": str(e)},
        )


@app.get("/last", response_model=DotaGameState, response_model_exclude_unset=True)
def get_last():
    global last_msg

    return last_msg


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
