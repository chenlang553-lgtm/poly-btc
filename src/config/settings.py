from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    poly_market_ws_url: str = Field(..., alias="POLY_MARKET_WS_URL")
    poly_rtds_ws_url: str = Field(..., alias="POLY_RTDS_WS_URL")
    poly_gamma_api_url: str = Field(..., alias="POLY_GAMMA_API_URL")
    data_dir: Path = Field(default=Path("data"), alias="DATA_DIR")

    entry_min_sec: int = Field(default=3, alias="ENTRY_MIN_SEC")
    entry_max_sec: int = Field(default=120, alias="ENTRY_MAX_SEC")
    min_edge: float = Field(default=0.02, alias="MIN_EDGE")
    max_spread: float = Field(default=0.08, alias="MAX_SPREAD")
    daily_loss_cap: float = Field(default=100.0, alias="DAILY_LOSS_CAP")
    max_consecutive_losses: int = Field(default=5, alias="MAX_CONSECUTIVE_LOSSES")


def get_settings() -> Settings:
    return Settings()
