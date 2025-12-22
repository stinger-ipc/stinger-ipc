from pydantic import BaseModel
from .interface_types import *


class SimpleInitialPropertyValues(BaseModel):

    school: str
    school_version: int = 0
