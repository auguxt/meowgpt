from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()


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
