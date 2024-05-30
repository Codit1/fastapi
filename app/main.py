from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True,
#     allow_origin_regex=None,
#     expose_headers=None,
#     max_age=1000,
# )



class Post(BaseModel):
    title : str
    content: str
    is_published : bool = True

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Jswebpro1', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as err:
        print('database connection failed')     
        print('trying again')
        time.sleep(3)

@app.get("/sqlalchemy")
def get_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'post': posts}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} was not found")
    return { "post": post}

@app.post("/posts")
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.is_published))
    post = cursor.fetchone()
    conn.commit()
    return {"post": post}

@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute("""DELET FROM post WHERE id = %s""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id: {id} was not found")
    
    return {"post": deleted_post}

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.is_published,str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post id: {id} was not found")
    
    return {"post": updated_post}