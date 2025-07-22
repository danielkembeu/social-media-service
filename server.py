from contextlib import asynccontextmanager
from typing import Optional, Annotated
from fastapi import Body, Depends, FastAPI, status
from fastapi.exceptions import HTTPException

#
from sqlmodel import SQLModel, select, create_engine, Session

#
from dotenv import load_dotenv
import os

#
from schemas.post import Posts

# ==============================================================================================================================================
# Database connection configuration
# ==============================================================================================================================================

# load the .env file content.
load_dotenv()

db_url = str(os.getenv("DB_URL"))

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Dependency to inject
SessionDep = Annotated[Session, Depends(get_session)]

# ==============================================================================================================================================
# Fast API instance
# ==============================================================================================================================================

app = FastAPI(
    title="Social Media API",
    description="A Web API service for a social media platform",
    version="1.0.0",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Get all posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_all_posts(session: SessionDep):
    statement = select(Posts)
    all_posts = session.exec(statement).all()

    return {"message": "All posts retrieved!", "data": all_posts}


# Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Posts, session: SessionDep):
    session.add(payload)
    session.commit()
    session.refresh(payload)

    return {"message": "Posts created successfully!", "data": payload}


# Get single post
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def get_single_post(post_id: int, session: SessionDep):
    post = session.get(Posts, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Post not found !"},
        )

    return {"message": "Post retrieved successfully", "data": post}


# Update post
@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, session: SessionDep, payload: Optional[Posts] = Body()):
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Post payload is required !"},
        )

    post = session.get(Posts, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Post not found !"},
        )

    post.title = payload.title
    post.content = payload.content
    post.published = payload.published

    session.add(post)
    session.commit()
    session.refresh(post)

    return {"message": "Post updated successfully", "data": post}


# Delete a single post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_post(post_id: int, session: SessionDep):
    post = session.get(Posts, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Post unexisting or already deleted !"},
        )

    session.delete(post)
    session.commit()

    return {"message": "Post deleted successfully"}
