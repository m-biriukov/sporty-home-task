from pydantic import BaseModel


class ErrorModel(BaseModel):
    error: str


class ErrorMessageModel(ErrorModel):
    message: str
