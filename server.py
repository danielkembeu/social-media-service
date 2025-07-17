from typing import Optional
from fastapi import Body, FastAPI, status
from fastapi.exceptions import HTTPException

#
import psycopg2
from psycopg2.extras import RealDictCursor

#
from datetime import datetime
from dotenv import load_dotenv
import os
import time

#
from schemas.post import Post

# ==============================================================================================================================================
# Database connection configuration
# ==============================================================================================================================================

# load the .env file content.
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PWD")
db_name = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")


while (
    True
):  # Adding this loop so that it keeps trying to connect to the db because of some unexpected issues

    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user=user,
            password=password,
            port=port,
            # This line is for making sure that the rows in the database is returned with the column names.
            # That's how the library works. And we import it from {psycopg2.extras}
            cursor_factory=RealDictCursor,
        )

        cursor = conn.cursor()
        print("Database connection successful !!")
        break

    except Exception as error:
        print(f"Database connection failed: {error}")
        conn = None

        time.sleep(5)  # Wait 05 seconds before retrying.

# ==============================================================================================================================================
# Fast API instance
# ==============================================================================================================================================

app = FastAPI(
    title="Social Media API",
    description="A Web API service for a social media platform",
    version="1.0.0",
)


# Get all posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    return {"message": "All posts retrieved!", "data": all_posts}


# Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    # Using fstring here makes my endpoint vulnerable for SQL injection
    # Better use input sanitazation (%s)
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
        (payload.title, payload.content),
    )
    new_post = cursor.fetchone()

    if conn is not None:
        conn.commit()  # Actually save the connection

    return {"message": "Posts created successfully!", "data": new_post}


# Get single post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_single_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    retrieved_post = cursor.fetchone()

    return {"message": "Post retrieved successfully", "data": retrieved_post}


# Update post
@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, payload: Optional[Post] = Body()):
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payload is required."
        )

    cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s, updated_at=%s WHERE id = %s RETURNING *""",
        (payload.title, payload.content, payload.published, datetime.now(), post_id),
    )

    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    if conn is not None:
        conn.commit()

    return {"message": "Post updated successfully", "data": updated_post}


# Delete a single post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()

    print(deleted_post)

    return {"message": "Post deleted successfully"}
