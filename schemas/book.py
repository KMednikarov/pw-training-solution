from typing import List, Optional

from pydantic import BaseModel, Field, PositiveInt


class Book(BaseModel):
    id: PositiveInt
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    isbn: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[int] = Field(default=None, alias="publishedYear")
    pages: int = Field(ge=0)
    language: Optional[str] = None
    price: float = Field(ge=0)
    rating: float = Field(ge=0, le=5)
    available: bool
    tags: List[str] = []