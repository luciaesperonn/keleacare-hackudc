import os
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from chatbot import Chatbot


class DiarioEmocional:
    def __init__(self):
        self.archivo_diario = "diario.txt"  # Archivo donde se guardan las entradas
        self.analyzer = SentimentIntensityAnalyzer()  # Inicializa el analizador de VADER
        self.diario = self.cargar_diario()  # Carga las entradas previas del diario
        self.chatbot = Chatbot()

    def cargar_diario(self):
        """
        Carga las entradas previas del diario desde el archivo de texto.
        Si el archivo no existe, retorna una lista vacía.
        """
        if os.path.exists(self.archivo_diario):
            with open(self.archivo_diario, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def guardar_diario(self):
        """
        Guarda las entradas del diario en el archivo de texto.
        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(f"- Día {len(self.diario) + 1}: {self.diario[-1]}\n")

    def analizar_emocion(self, texto):
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

    def resumir_texto(self, texto, emocion, max_tokens=50, system_personality="Eres un agente especializado en resúmenes extremadamente cortos."):
        """
        Utiliza el chatbot para resumir el texto.
        """
        # Crea un prompt para solicitar el resumen del texto
        prompt = f"Por favor, obtén la razón del sentimiento {emocion} en este texto:\n\n{texto}"
        # Llama al método 'llamar_chatbot' del objeto 'chatbot'
        respuesta = self.chatbot.llamar_chatbot(prompt, max_tokens=max_tokens, system_personality=system_personality)
        return respuesta

    def mostrar_diario(self):
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            emocion = self.analizar_emocion(user_input)
            resumen = self.resumir_texto(texto=user_input, emocion=emocion)
            if not resumen:
                st.error("No se pudo generar un resumen. Inténtalo de nuevo.")
                return
            # Se guarda la entrada como un diccionario
            self.diario.append({"texto": resumen, "emocion": emocion})
            st.success("Entrada guardada con éxito!")

        st.subheader("Tus entradas:")
        for index, entrada in enumerate(self.diario):
            # Verificamos que la entrada sea un diccionario
            if isinstance(entrada, dict):
                st.write(f"Entrada {index + 1}: {entrada['texto']}")
                st.write(f"Emoción detectada: {entrada['emocion']}")
            else:
                st.write(f"Entrada {index + 1}: {entrada}")
