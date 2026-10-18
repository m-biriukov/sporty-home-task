from pydantic import BaseModel, ValidationError


def is_model_valid(model: type[BaseModel], data: str | dict) -> bool:
    try:
        if isinstance(data, str):
            model.model_validate_json(data)
        else:
            model.model_validate(data)
        return True
    except ValidationError:
        return False
