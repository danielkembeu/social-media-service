from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    id: int = 1
    title: str
    content: str
    published: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
