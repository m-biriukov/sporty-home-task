from pydantic import BaseModel, ConfigDict, Field

from helpers.enums import Selection


class PlaceBetModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    match_id: str = Field(alias="matchId")
    selection: Selection
    stake: float
    additional_prop: dict | None = Field(
        default_factory=dict, alias="additionalProp1"
    )


class SuccessBetModel(BaseModel):
    message: str
    matchId: str
    selection: Selection
    stake: float
    odds: float
    payout: float
    balance: float
    currency: str
