import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import requests

class Chatbot:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()  # Inicializa el analizador de VADER
        self.respuestas = {
            "positive": "¡Me alegra que te sientas feliz! ¿Qué te ha hecho sentir así?",
            "negative": "Lamento escuchar que te sientes triste. ¿Quieres hablar más sobre ello?",
            "neutral": "Gracias por compartir. ¿Hay algo más en lo que pueda ayudarte?"
        }
        self.archivo_objetivos = "objetivos.txt"  # Archivo de objetivos

    def cargar_objetivos(self):
        """
        Carga los objetivos del usuario desde el archivo de texto.
        """
        if os.path.exists(self.archivo_objetivos):
            with open(self.archivo_objetivos, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def detectar_emocion(self, texto):
        """
        Analiza el texto usando VADER y devuelve la emoción predominante.
        """
        sentiment = self.analyzer.polarity_scores(texto)
        if sentiment["compound"] >= 0.05:
            return "positive"  # Emoción positiva
        elif sentiment["compound"] <= -0.05:
            return "negative"  # Emoción negativa
        else:
            return "neutral"  # Emoción neutral

    def mostrar_chatbot(self):
        st.title("Chatbot Empático")
        user_input = st.text_input("Escribe algo...")

        if user_input:
            emocion = self.detectar_emocion(user_input)  # Detecta la emoción del texto
            st.write(f"Emoción detectada: {emocion}")
            st.write(self.respuestas.get(emocion, "Gracias por compartir. ¿Hay algo más en lo que pueda ayudarte?"))

            # Mostrar recomendaciones basadas en los objetivos
            objetivos = self.cargar_objetivos()
            if objetivos:
                st.subheader("Recomendaciones basadas en tus objetivos:")
                for objetivo in objetivos:
                    st.write(f"- Para lograr '{objetivo.strip()}', podrías intentar [sugerencia].")

    def llamar_chatbot(self, prompt, model="mistral-7B", max_tokens=150, system_personality="Eres un asistente muy amable, siempre buscando animar a la gente"):
        """
        Envía una consulta al chatbot de Mistral con el prompt proporcionado.

        Parámetros:
            prompt (str): El mensaje que se enviará al chatbot.
            model (str): El modelo a utilizar (por defecto "mistral-7B").
            max_tokens (int): La cantidad máxima de tokens para la respuesta.

        Retorna:
            str: La respuesta generada por el chatbot, o False en caso de error.
        """
        api_url = "https://api.mistral.ai/v1/chat"  # Ejemplo de URL, ajusta según la documentación oficial
        api_key = "TU_API_KEY"  # Reemplaza con tu API key real

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
