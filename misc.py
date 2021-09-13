import typing as ty
import json
from pydantic import BaseModel



class SettingsModel(BaseModel):
    access_token: str
    admin_id: int
    db_url: str = "sqlite://db.sqlite"
    debug: bool = False
    day_change_time: str = "11:00"
    nigth_change_time: str = "23:00"



def load_settings() -> SettingsModel:
    with open('settings.json', 'r', encoding='utf-8') as file:
        return SettingsModel(**json.loads(file.read()))


def b2s(value: ty.Any) -> str:
    return "✅" if value else "🚫"

def value_or_default(value: ty.Any, default: str = 'отсутствует') -> str:
    return value if value else default