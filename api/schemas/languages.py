"""
Module for the language type definitions of API responses

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
    2. APIResponse is deprecated
"""
from typing import Optional
from pydantic import BaseModel

class Language(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
