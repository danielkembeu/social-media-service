from fastapi import Body, FastAPI, status

from data.posts import posts
from schemas.post import Post


app = FastAPI(title="Social Media API", version="1.0.0")


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"message": "Posts retrieved!", "data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    return {"message": "Posts created successfully!", "data": payload}
