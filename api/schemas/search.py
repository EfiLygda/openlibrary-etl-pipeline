"""
Module for the type definitions of the search endpoint

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from pydantic import BaseModel
from typing import Optional

class SearchAuthor(BaseModel):
    author_key: str
    author_name: Optional[str]

class SearchWork(BaseModel):
    work_key: str
    title: Optional[str]
    authors: list[SearchAuthor]
