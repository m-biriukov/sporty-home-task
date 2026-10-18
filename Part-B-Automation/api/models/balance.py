from pydantic import BaseModel


class BalanceModel(BaseModel):
    balance: float
    currency: str


class BalanceResetModel(BalanceModel):
    message: str
