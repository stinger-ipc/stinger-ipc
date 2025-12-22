from typing import Callable, Optional

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


class FullPropertyAccess(BaseModel):

    favorite_number_getter: Callable[[], int]

    favorite_number_setter: Callable[[int], None]

    favorite_foods_getter: Callable[[], FavoriteFoodsProperty]

    favorite_foods_setter: Callable[[FavoriteFoodsProperty], None]

    lunch_menu_getter: Callable[[], LunchMenuProperty]

    family_name_getter: Callable[[], str]

    family_name_setter: Callable[[str], None]

    last_breakfast_time_getter: Callable[[], datetime]

    last_breakfast_time_setter: Callable[[datetime], None]

    last_birthdays_getter: Callable[[], LastBirthdaysProperty]

    last_birthdays_setter: Callable[[LastBirthdaysProperty], None]
