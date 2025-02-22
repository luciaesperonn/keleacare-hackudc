from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Cargar el modelo y el tokenizador
model_name = "bhadresh-savani/bert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Definir las emociones que el modelo puede detectar
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

# Función para analizar todas las emociones
def analizar_todas_emociones(texto):
    # Tokenizar el texto
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
    
    # Obtener las predicciones del modelo
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Calcular las probabilidades usando softmax
    probabilidades = torch.softmax(logits, dim=-1).squeeze().numpy()
    
    # Crear un diccionario con las emociones y sus scores
    emociones = {emotion_labels[i]: float(probabilidades[i]) for i in range(len(emotion_labels))}
    
    return emociones

# Ejemplo de uso
texto = "Lo que hizo me parece completamente inaceptable"
todas_emociones = analizar_todas_emociones(texto)
print("Todas las emociones detectadas:", todas_emociones)