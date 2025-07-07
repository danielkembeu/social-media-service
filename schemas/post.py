from typing import Optional
from uuid import uuid4, UUID
from pydantic import BaseModel


class Post(BaseModel):
    id: UUID = uuid4()
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None
