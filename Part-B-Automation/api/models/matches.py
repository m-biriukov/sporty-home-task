import datetime

from pydantic import BaseModel, Field, ConfigDict


class OddsModel(BaseModel):
    home: float
    draw: float
    away: float


class MatchModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    competition: str
    kickoff_date: datetime.date = Field(alias="kickoffDate")
    homeTeam: str
    awayTeam: str
    odds: OddsModel
