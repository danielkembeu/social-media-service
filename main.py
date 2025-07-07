from fastapi import FastAPI

# Schemas
from schemas.post import Post

app = FastAPI(title="Social Media API", version="1.0.0")


# Routing
@app.get("/posts", tags=["Posts"])
def get_posts():
    return {"message": "Hello world!"}


@app.get("/posts/single/{post_id}", tags=["Posts"])
def get_single_post(post_id: int):
    return {"message": "Post retrieved!", "data": post_id}


@app.get("/posts/all", tags=["Posts"])
def get_all_posts():
    return {"message": "This is all the posts"}


@app.post("/posts/create", tags=["Posts"])
def create_post(payload: Post):
    print(dict(payload))
    return {"message": "New post created successfully!", "data": payload}


@app.patch("/posts/partial/{post_id}", tags=["Posts"])
def partial_update_post(post_id: int):
    return {"message": "Post partial update successfull!", "data": post_id}


@app.put("/posts/full/{post_id}", tags=["Posts"])
def full_update_post(post_id: int):
    return {"message": "Post full update successfull!", "data": post_id}


@app.delete("/posts/delete/{post_id}", tags=["Posts"])
def delete_single_post(post_id: int):
    return {"message": "Deletion successfull!", "data": post_id}
