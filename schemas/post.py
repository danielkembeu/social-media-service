from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Posts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
