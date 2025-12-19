
from typing import Callable, Optional

from pydantic import BaseModel
from .interface_types import *



class SimplePropertyAccess(BaseModel):
    
    school_getter: Callable[[], str]
    
    school_setter: Callable[[str], None]
    
    

