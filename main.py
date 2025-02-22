import openai
from fastapi import FastAPI

MISTRAL_API_KEY = "pvWRQA9Z5VoQRPhlcJEIqYutMA7DGQaI"

openai.api_key = MISTRAL_API_KEY
app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a KeleaCare con Mistral AI"}