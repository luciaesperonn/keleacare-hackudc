import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from sentence_transformers import SentenceTransformer

class Chatbot:
    """
    Chatbot que analiza sentimientos, genera embeddings y clasifica emociones en textos.

    Atributos:
        analyzer: SentimentIntensityAnalyzer
            Analizador de sentimientos de VADER.
        modelo_embeddings: SentenceTransformer
            Modelo de embeddings de frases basado en "all_MiniLM-L6-v2".
        faiss_index: faiss.IndexFlatL2
            Índice FAISS utilizado para la búsqueda eficiente de objetivos.
        model_name: str
            Nombre del modelo de clasificación de emociones ("bhadresh-savani/bert-base-uncased-emotion").
        model: AutoModelForSequenceClassification
            Modelo preentrenado de clasificación de emociones.
        tokenizer: AutoTokenizer
            Tokenizador asociado al modelo de clasificación de emociones.
        emotion_labels: list
            Lista de etiquetas de emociones utilizadas en la clasificación.
    
    Métodos:
        cargar_objetivos():
            Carga los objetivos desde FAISS si existen, o crea un nuevo índice.
        agregar_objetivo(objetivo):
            Añade un nuevo objetivo al índice FAISS.
        analizar_emocion(texto):
            Analiza la emoción predominante en el texto utilizando un modelo preentrenado.
        enriquecer_prompt(texto, emocion, personalidad, emocion_diario, razon_diario, objetivos):
            Enriquece el prompt con la información obtenida de los embeddings.
        obtener_info_desde_embeddings(k=3):
            Obtiene la información relevante de los embeddings almacenados, recuperando los k más cercanos.
        mostrar_chatbot():
            Muestra la interfaz del chatbot en Streamlit.
        llamar_chatbot(prompt, model="mistral-small-latest", max_tokens=300, system_personality="You are a very kind assistant, always looking to encourage people."):
            Llama al chatbot de Mistral AI y devuelve la respuesta generada.

    """
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
        Añade un nuevo objetivo al índice FAISS.
        """
        vector = self.modelo_embeddings.encode([objetivo])
        self.faiss_index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.faiss_index, "objetivos.index")
    
    def analizar_emocion(self, texto):
        """
        Analiza la emoción predominante en el texto utilizando
        un modelo preentrenado.
        """
        inputs = self.tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probabilidades = torch.softmax(logits, dim=-1).squeeze().numpy()
        emocion_predominante = self.emotion_labels[np.argmax(probabilidades)]
        return emocion_predominante
    
    def enriquecer_prompt(self, texto, emocion, personalidad, emocion_diario, razon_diario, objetivos):
        """
        Enriquece el prompt con la información obtenida de los embeddings.
        """
        return f"Responds based on the emotion ‘{emocion}’ manifested by a person of personality {personalidad}, who has recently experienced feelings of {emocion_diario} due to {razon_diario}. If the situation allows, offer practical advice to help him/her achieve his/her personal {objetivos}. But focus on analyze and respond based on the following text without forgiving the context previously given: {texto}"

    def obtener_info_desde_embeddings(self, k=3):
        """
        Obtiene la información relevante de los embeddings almacenados,
        recuperando los k más cercanos.
        """
        def obtener_multiples_resultados(query):
            vector = self.modelo_embeddings.encode([query], convert_to_numpy=True)
            D, I = self.faiss_index.search(vector, k)
            resultados = ["Not available" if idx == -1 else f"Result {i+1} stored" for i, idx in enumerate(I[0])]
            return resultados
        
        # Obtener múltiples valores para cada categoría
        personalidad = obtener_multiples_resultados("personalidad")
        emocion_diario = obtener_multiples_resultados("emocion_diario")
        razon_diario = obtener_multiples_resultados("razon_diario")
        objetivos = obtener_multiples_resultados("objetivos")
        
        return personalidad, emocion_diario, razon_diario, objetivos

    def mostrar_chatbot(self):
        """
        Muestra la interfaz del chatbot en Streamlit.
        """
        st.title("Empathic chatbot")
        user_input = st.text_input("Write something...")

        if user_input:
            emocion = self.analizar_emocion(user_input)
            personalidad, emocion_diario, razon_diario, objetivos = self.obtener_info_desde_embeddings()
            
            st.write(f"Detected emotion: {emocion}")
            prompt_rico = self.enriquecer_prompt(user_input, emocion, personalidad, emocion_diario, razon_diario, objetivos)
            st.write(self.llamar_chatbot(prompt=prompt_rico))


    
    def llamar_chatbot(self, prompt, model="mistral-small-latest", max_tokens=300, system_personality="You are a very kind assistant, always looking to encourage people."):
        """
        Llama al chatbot de Mistral AI y devuelve la respuesta generada.
        """
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
