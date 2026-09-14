from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "MeowGPT API is running 🐾"}


@app.post("/meow")
def meow(message: Message):
    text = message.text

    if text.lower() == "exit":
        response = "meow bye🐾"

    elif len(text) < 10:
        response = "meow " * random.randint(1, 5)

    else:
        response = "meow " * random.randint(6, 30)

    return {
        "response": response.strip()
    }
