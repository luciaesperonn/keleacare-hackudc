import streamlit as st
import text2emotion as te

class Chatbot:
    def __init__(self):
        self.respuestas = {
            "Happy": "¡Me alegra que te sientas feliz! ¿Qué te ha hecho sentir así?",
            "Sad": "Lamento escuchar que te sientes triste. ¿Quieres hablar más sobre ello?",
            "Angry": "Entiendo que estés enfadado. ¿Puedes contarme qué ha pasado?",
            "Surprise": "¡Vaya! Parece que algo te ha sorprendido. ¿Qué ha sido?",
            "Fear": "El miedo puede ser abrumador. ¿Quieres compartir qué te preocupa?"
        }

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