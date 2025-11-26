from typing import Any

from pydantic import BaseModel, Field, field_validator


class DotaProvider(BaseModel):
    """Dota 2 game provider information"""
    appid: int
    name: str
    timestamp: int
    version: int


class DotaPlayer(BaseModel):
    """Player state and statistics"""
    accountid: str
    steamid: str
    name: str
    activity: str
    team_name: str
    team_slot: int
    player_slot: int
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    kill_streak: int
    commands_issued: int
    gold: int
    gold_reliable: int
    gold_unreliable: int
    gold_from_creep_kills: int
    gold_from_hero_kills: int
    gold_from_income: int
    gold_from_shared: int
    gpm: int
    xpm: int
    kill_list: dict[str, Any]


class DotaMap(BaseModel):
    """Map and game state information"""
    name: str
    matchid: str
    game_time: int
    clock_time: int
    daytime: bool
    nightstalker_night: bool
    game_state: str
    paused: bool
    win_team: str
    customgamename: str
    radiant_score: int
    dire_score: int
    ward_purchase_cooldown: int

    @field_validator("game_state")
    def validate_game_state(cls, v: str):
        return v.lower().replace("dota_gamerules_state_", "")


class DotaHero(BaseModel):
    """Hero state and attributes"""
    id: int | None = None
    name: str | None = None
    level: int | None = None
    alive: bool | None = None
    respawn_seconds: int | None = None
    buyback_cost: int | None = None
    buyback_cooldown: int | None = None
    health: int | None = None
    max_health: int | None = None
    health_percent: int | None = None
    mana: int | None = None
    max_mana: int | None = None
    mana_percent: int | None = None
    xp: int | None = None
    xpos: int | None = None
    ypos: int | None = None
    facet: int | None = None
    attributes_level: int | None = None
    # Status effects
    silenced: bool | None = None
    stunned: bool | None = None
    disarmed: bool | None = None
    magicimmune: bool | None = None
    hexed: bool | None = None
    muted: bool | None = None
    break_status: bool | None = Field(None, alias="break")  # 'break' is a Python keyword
    has_debuff: bool | None = None
    smoked: bool | None = None
    # Items
    aghanims_scepter: bool | None = None
    aghanims_shard: bool | None = None
    # Talents
    talent_1: bool | None = None
    talent_2: bool | None = None
    talent_3: bool | None = None
    talent_4: bool | None = None
    talent_5: bool | None = None
    talent_6: bool | None = None
    talent_7: bool | None = None
    talent_8: bool | None = None
    # Buffs
    permanent_buffs: dict[str, Any] | None = None

    @field_validator("name")
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.replace("npc_dota_hero_", "")


class DotaGameState(BaseModel):
    provider: DotaProvider | None = None
    map: DotaMap | None = None
    player: DotaPlayer | None = None
    hero: DotaHero | None = None
    abilities: dict[str, Any] | None = None
    items: dict[str, Any] | None = None
    auth: dict[str, Any] | None = None
