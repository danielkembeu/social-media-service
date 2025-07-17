from datetime import datetime
from typing import Any, Optional
from uuid import uuid4, UUID
from pydantic import BaseModel


class Post(BaseModel):
    id: int = 1
    title: str
    content: str
    published: bool = True
    created_at: datetime = datetime.now()
