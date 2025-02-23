import os
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from chatbot import Chatbot

class DiarioEmocional:
    """
    Clase para gestionar el diario emocional.
    """
    def __init__(self):
        """
        Inicializa la clase con los atributos necesarios para el diario emocional.

        Atributos:
        -----------
        archivo_diario : str
            El nombre del archivo donde se guardan las entradas del diario.
        model_name : str
            Nombre del modelo BERT para análisis de emociones.
        tokenizer : AutoTokenizer
            Tokenizador del modelo BERT.
        model : AutoModelForSequenceClassification
            Modelo BERT para análisis de emociones.
        emotion_labels : list
            Lista de etiquetas de emociones.
        diario : list
            Lista de entradas del diario.
        chatbot : Chatbot
            Objeto de la clase Chatbot para resumir el texto
        
        Métodos:
        --------
        cargar_diario()
            Carga las entradas previas del diario desde el archivo de texto.
        guardar_diario(entrada)
            Guarda una nueva entrada en el archivo de texto.
        resumir_texto(texto, emocion, max_tokens=50, system_personality="Eres un agente especializado en resúmenes extremadamente cortos.")
            Utiliza el chatbot para resumir el texto.
        mostrar_diario()
            Muestra la interfaz del diario emocional en Stream
        
        """

        self.archivo_diario = "diario.txt"  # Archivo donde se guardan las entradas
        # Cargar el modelo y el tokenizador para análisis de emociones
        self.model_name = "bhadresh-savani/bert-base-uncased-emotion"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]
        self.diario = self.cargar_diario()  # Carga las entradas previas del diario
        self.chatbot = Chatbot()

    def cargar_diario(self):
        """
        Carga las entradas previas del diario desde el archivo de texto.
        Si el archivo no existe, retorna una lista vacía.

        Returns:
            list: Una lista de entradas del diario.

        """
        if os.path.exists(self.archivo_diario):
            with open(self.archivo_diario, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def guardar_diario(self, entrada):
        """
        Guarda una nueva entrada en el archivo de texto.

        Parámetros:
            entrada (str): La nueva entrada del diario.

        Returns:
            None

        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(entrada + "\n")

    def resumir_texto(self, texto, emocion, max_tokens=50, system_personality="Eres un agente especializado en resúmenes extremadamente cortos."):
        """
        Utiliza el chatbot para resumir el texto.

        Parámetros:
            texto (str): El texto a resumir.
            emocion (str): La emoción asociada al texto.
            max_tokens (int): Número máximo de tokens para el resumen.
            system_personality (str): Personalidad del sistema para el resumen.

        Returns:
            str: El resumen generado por el chatbot.

        """
        # Crea un prompt para solicitar el resumen del texto
        prompt = f"Por favor, obtén la razón del sentimiento {emocion} en este texto:\n\n{texto}"
        # Llama al método 'llamar_chatbot' del objeto 'chatbot'
        respuesta = self.chatbot.llamar_chatbot(prompt, max_tokens=max_tokens, system_personality=system_personality)
        return respuesta

    def mostrar_diario(self):
        """
        Muestra la interfaz del diario emocional en Streamlit.

        Returns:
            None

        """ 
        
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            emocion = self.chatbot.analizar_emocion(user_input)
            resumen = self.resumir_texto(texto=user_input, emocion=emocion)
            if not resumen:
                st.error("No se pudo generar un resumen. Inténtalo de nuevo.")
                return

            # Formatear la entrada para guardarla en el archivo
            entrada_formateada = f"{resumen} | {emocion}"
            
            # Guardar la entrada en el archivo
            self.guardar_diario(entrada_formateada)
            
            # Añadir la entrada al diario en memoria
            self.diario.append(entrada_formateada)
            
            st.success("Entrada guardada con éxito!")

        # Mostrar las entradas del diario
        if self.diario:
            st.subheader("Tus entradas:")
            for entrada in self.diario:
                st.write(entrada)