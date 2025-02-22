import streamlit as st
import text2emotion as te
import requests

class Chatbot:
    def __init__(self):
        self.respuestas = {
            "Happy": "¡Me alegra que te sientas feliz! ¿Qué te ha hecho sentir así?",
            "Sad": "Lamento escuchar que te sientes triste. ¿Quieres hablar más sobre ello?",
            "Angry": "Entiendo que estés enfadado. ¿Puedes contarme qué ha pasado?",
            "Surprise": "¡Vaya! Parece que algo te ha sorprendido. ¿Qué ha sido?",
            "Fear": "El miedo puede ser abrumador. ¿Quieres compartir qué te preocupa?"
        }
    

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

    def detectar_emocion(self, texto):
        emocion = te.get_emotion(texto)
        return max(emocion, key=emocion.get)  # Devuelve la emoción predominante

    def mostrar_chatbot(self):
        st.title("Chatbot Empático")
        user_input = st.text_input("Escribe algo...")

        if user_input:
            emocion = self.detectar_emocion(user_input)
            st.write(f"Emoción detectada: {emocion}")
            st.write(self.respuestas.get(emocion, "Gracias por compartir. ¿Hay algo más en lo que pueda ayudarte?"))