import openai
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from nltk.sentiment import SentimentIntensityAnalyzer
from database import SessionLocal, DiarioEmocional

# Configurar la API y VADER
MISTRAL_API_KEY = "pvWRQA9Z5VoQRPhlcJEIqYutMA7DGQaI"
openai.api_key = MISTRAL_API_KEY
app = FastAPI()
sia = SentimentIntensityAnalyzer()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo de datos para recibir mensajes
class Message(BaseModel):
    text: str

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a KeleaCare con Mistral AI"}

@app.post("/analizar_sentimiento/")
def analizar_sentimiento(msg: Message, db: Session = Depends(get_db)):
    sentimiento = sia.polarity_scores(msg.text)

    # Clasificación de la emoción
    if sentimiento["compound"] >= 0.05:
        emocion = "Positivo"
        respuesta = "¡Me alegra saber que te sientes bien! Cuéntame más sobre tu día."
    elif sentimiento["compound"] <= -0.05:
        emocion = "Negativo"
        respuesta = "Lamento que te sientas así. Si quieres hablar de ello, estoy aquí para escucharte."
    else:
        emocion = "Neutral"
        respuesta = "¿Quieres compartir algo más?"

    # Guardar en la base de datos
    entrada = DiarioEmocional(
        texto=msg.text,
        emocion_detectada=emocion,
        score_negativo=sentimiento["neg"],
        score_neutro=sentimiento["neu"],
        score_positivo=sentimiento["pos"],
        score_compuesto=sentimiento["compound"],
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)

    return {
        "emocion_detectada": emocion,
        "puntajes_vader": sentimiento,
        "respuesta": respuesta
    }
