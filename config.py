from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MQTT_BROKER: str
    MQTT_PORT: int = 1883
    MQTT_BASE_TOPIC: str = "dota2"
    HASS_DISCOVERY_PREFIX: str = "homeassistant"


settings = Settings()
