from pydantic import BaseModel
from .interface_types import *


class FullInitialPropertyValues(BaseModel):

    favorite_number: int
    favorite_number_version: int = 0

    favorite_foods: FavoriteFoodsProperty
    favorite_foods_version: int = 0

    lunch_menu: LunchMenuProperty
    lunch_menu_version: int = 0

    family_name: str
    family_name_version: int = 0

    last_breakfast_time: datetime
    last_breakfast_time_version: int = 0

    last_birthdays: LastBirthdaysProperty
    last_birthdays_version: int = 0
