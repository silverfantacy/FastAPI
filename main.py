from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/blog")
async def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int, q: Optional[str] = None):
    return {"id": id, "q": q}


@app.get("/blog/{id}/comments")
def comments(id: int, limit=10):
    return {"id": id, "limit": limit}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}

# 為了偵錯方便，所以在這裡啟動
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
