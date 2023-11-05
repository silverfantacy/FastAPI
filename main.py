from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import blog, otp, user, authentication, openai, fief

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# CORS middleware to allow all origins
# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fief.router)
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(openai.router)
app.include_router(otp.router)
