from enum import StrEnum


class Selection(StrEnum):
    HOME = "HOME"
    DRAW = "DRAW"
    AWAY = "AWAY"

    @property
    def label(self) -> str:
        """Human-readable form shown in the UI, e.g. 'Home'."""
        return self.value.title()
