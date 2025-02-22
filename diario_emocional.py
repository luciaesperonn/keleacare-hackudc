import os
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class DiarioEmocional:
    def __init__(self):
        self.archivo_diario = "diario.txt"  # Archivo donde se guardan las entradas
        self.analyzer = SentimentIntensityAnalyzer()  # Inicializa el analizador de VADER
        self.diario = self.cargar_diario()  # Carga las entradas previas del diario

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

    def mostrar_diario(self):
        """
        Muestra la interfaz del diario emocional en Streamlit.
        """
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            emocion = self.analizar_emocion(user_input)  # Analiza la emoción del texto
            entrada = f"Texto: {user_input} | Emoción: {emocion}"  # Formato de la entrada
            self.diario.append(entrada)  # Añade la entrada al diario
            self.guardar_diario()  # Guarda el diario en el archivo de texto
            st.success("Entrada guardada con éxito!")

        if self.diario:
            st.subheader("Tus entradas:")
            for i, entrada in enumerate(self.diario):
                st.write(f"Entrada {i + 1}: {entrada}")