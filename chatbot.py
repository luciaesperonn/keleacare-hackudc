import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from sentence_transformers import SentenceTransformer

class Chatbot:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        self.faiss_index = self.cargar_objetivos()
        self.model_name = "bhadresh-savani/bert-base-uncased-emotion"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]
    
    def cargar_objetivos(self):
        """
        Carga los objetivos desde FAISS si existen, o crea un nuevo índice.
        """
        try:
            index = faiss.read_index("objetivos.index")
        except:
            index = faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings
        return index
    
    def agregar_objetivo(self, objetivo):
        """
        Agrega un nuevo objetivo al índice FAISS.
        """
        vector = self.modelo_embeddings.encode([objetivo])
        self.faiss_index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.faiss_index, "objetivos.index")
    
    def analizar_emocion(self, texto):
        """
        Analiza la emoción predominante en el texto usando un modelo preentrenado.
        """
        inputs = self.tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probabilidades = torch.softmax(logits, dim=-1).squeeze().numpy()
        emocion_predominante = self.emotion_labels[np.argmax(probabilidades)]
        return emocion_predominante
    
    def enriquecer_prompt(self, texto, emocion, personalidad, emocion_diario, razon_diario, objetivos):
        return f"Responde en función de la emoción ‘{emocion}’ manifestada por una persona de personalidad {personalidad}, quien ha experimentado recientemente sentimientos de {emocion_diario} debido a {razon_diario}. Si la situación lo permite, ofrece un consejo práctico que le ayude a alcanzar sus objetivos personales: {objetivos}. Analiza y responde basándote en el siguiente texto: {texto}"

    def obtener_info_desde_embeddings(self, k=3):
        """
        Obtiene la información relevante desde los embeddings almacenados, recuperando los k más cercanos.
        """
        def obtener_multiples_resultados(query):
            vector = self.modelo_embeddings.encode([query], convert_to_numpy=True)
            D, I = self.faiss_index.search(vector, k)
            resultados = ["No disponible" if idx == -1 else f"Resultado {i+1} almacenado" for i, idx in enumerate(I[0])]
            return resultados
        
        # Obtener múltiples valores para cada categoría
        personalidad = obtener_multiples_resultados("personalidad")
        emocion_diario = obtener_multiples_resultados("emocion_diario")
        razon_diario = obtener_multiples_resultados("razon_diario")
        objetivos = obtener_multiples_resultados("objetivos")
        
        # Imprimir resultados para verlos en consola
        print(f"Personalidades obtenidas: {personalidad}")
        print(f"Emociones del diario obtenidas: {emocion_diario}")
        print(f"Razones del diario obtenidas: {razon_diario}")
        print(f"Objetivos obtenidos: {objetivos}")
        
        return personalidad, emocion_diario, razon_diario, objetivos

    def mostrar_chatbot(self):
        st.title("Chatbot Empático")
        user_input = st.text_input("Escribe algo...")

        if user_input:
            emocion = self.analizar_emocion(user_input)
            personalidad, emocion_diario, razon_diario, objetivos = self.obtener_info_desde_embeddings()
            
            st.write(f"Emoción detectada: {emocion}")
            prompt_rico = self.enriquecer_prompt(user_input, emocion, personalidad, emocion_diario, razon_diario, objetivos)
            st.write(self.llamar_chatbot(prompt=prompt_rico))


    
    def llamar_chatbot(self, prompt, model="mistral-small-latest", max_tokens=150, system_personality="Eres un asistente muy amable, siempre buscando animar a la gente"):
        api_url = "https://api.mistral.ai/v1/chat/completions"
        api_key = "fxjfZhsoN3PYMis5poL5rs8AHicjlwHO"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_personality},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            respuesta = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return respuesta.strip() if respuesta else False
        else:
            return False
