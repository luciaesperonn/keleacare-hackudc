import os
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from chatbot import Chatbot

class DiarioEmocional:
    def __init__(self):
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
        """
        if os.path.exists(self.archivo_diario):
            with open(self.archivo_diario, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def guardar_diario(self, entrada):
        """
        Guarda una nueva entrada en el archivo de texto.
        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(entrada + "\n")

    def analizar_emocion(self, texto):
        """
        Analiza el texto usando el modelo BERT y devuelve la emoción predominante.
        """
        # Tokenizar el texto
        inputs = self.tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
        
        # Obtener las predicciones del modelo
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        # Calcular las probabilidades usando softmax
        probabilidades = torch.softmax(logits, dim=-1).squeeze().numpy()
        
        # Obtener la emoción con la probabilidad más alta
        emocion_predominante = self.emotion_labels[np.argmax(probabilidades)]
        
        return emocion_predominante

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

            # Formatear la entrada para guardarla en el archivo
            entrada_formateada = f"Entrada {len(self.diario) + 1}: {resumen} | Emoción: {emocion}"
            
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