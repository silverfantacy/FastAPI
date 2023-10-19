from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, otp, user, authentication, openai

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(openai.router)
app.include_router(otp.router)
