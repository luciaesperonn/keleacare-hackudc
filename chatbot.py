import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class Chatbot:
    """
    Esta clase define un chatbot empático que interactúa con el usuario, detecta emociones en sus mensajes y utiliza modelos de IA para generar respuestas personalizadas. 
    """
    def __init__(self):
        """
        Inicializa las variables y objetos necesarios para el funcionamiento del chatbot.
        Se configuran los archivos de texto, el modelo BERT para análisis de emociones, y el analizador VADER para sentimientos.

        Atributos:
        -----------
        analyzer : SentimentIntensityAnalyzer
            Analizador de sentimientos VADER.
        emotion_labels : list
            Lista de etiquetas de emociones.
        model_name : str
            Nombre del modelo BERT para análisis de emociones.
        tokenizer : AutoTokenizer
            Tokenizador del modelo BERT.
        model : AutoModelForSequenceClassification
            Modelo BERT para análisis de emociones.
        archivo_objetivos : str
            Nombre del archivo de objetivos.
        archivo_personalidad : str
            Nombre del archivo de personalidad.
        archivo_diario : str
            Nombre del archivo de diario.

        Métodos:
        --------    
        cargar_info_desde_txt(archivo)
            Carga la información desde un archivo de texto.
        extraer_resumen_y_emocion(texto)
            Extrae el resumen y la emoción desde una línea del diario.
        obtener_info_desde_txt()
            Obtiene la información de personalidad, emoción diaria y objetivos desde los archivos de texto.
        analizar_emocion(texto)
            Analiza el texto usando el modelo BERT y devuelve la emoción predominante.
        enriquecer_prompt(texto, emocion, personalidad, emocion_diario, resumen, objetivos)
            Enriquece el prompt con la emoción y el texto proporcionados.
        mostrar_chatbot()
            Muestra la interfaz del chatbot en Streamlit.
        llamar_chatbot(prompt, model="mistral-small-latest", max_tokens=150, system_personality="Eres un asistente muy amable, siempre buscando animar a la gente")
            Envía una consulta al chatbot de Mistral con el prompt proporcionado.
    
        """
        self.analyzer = SentimentIntensityAnalyzer()  # Inicializa el analizador de VADER
        self.emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]   # Etiquetas de emociones
        self.model_name = "bhadresh-savani/bert-base-uncased-emotion"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.archivo_objetivos = "objetivos.txt"  # Archivo de objetivos
        self.archivo_personalidad = "personalidad.txt"  # Archivo de personalidad
        self.archivo_diario = "diario.txt"  # Archivo de diario (contiene resumen y emoción)

    def cargar_info_desde_txt(self, archivo):
        """
        Carga la información desde un archivo de texto.
        Si el archivo no existe, devuelve un valor por defecto.

        Parámetros:
            archivo (str): El nombre del archivo de texto.

        Return:
            str: El contenido del archivo o "No disponible" si el archivo no existe

        """
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                return lineas[-1].strip() if lineas else "No disponible"
        return "No disponible"

    def extraer_resumen_y_emocion(self, texto):
        """
        Extrae el resumen y la emoción desde una línea del diario.

        Parámetros:
            texto (str): La línea del diario que contiene el resumen y la emoción.
        
        Return:
            tuple: Una tupla con el resumen y la emoción extraídos, o ("No disponible", "No disponible") si no se puede extraer.
        """
        if " | " in texto:
            resumen, emocion = texto.split(" | ")
            return resumen.strip(), emocion.strip()
        return "No disponible", "No disponible"

    def obtener_info_desde_txt(self):
        """
        Obtiene la información de personalidad, emoción diaria y objetivos desde los archivos de texto.

        Return:
            tuple: Una tupla con la personalidad, emoción diaria, resumen y
            objetivos extraídos de los archivos de texto.
        """
        # Obtener personalidad y objetivos desde sus archivos
        personalidad = self.cargar_info_desde_txt(self.archivo_personalidad)
        objetivos = self.cargar_info_desde_txt(self.archivo_objetivos)

        # Obtener resumen y emoción desde diario.txt
        linea_diario = self.cargar_info_desde_txt(self.archivo_diario)
        resumen, emocion_diario = self.extraer_resumen_y_emocion(linea_diario)

        return personalidad, emocion_diario, resumen, objetivos

    def analizar_emocion(self, texto):
        """
        Analiza el texto usando el modelo BERT y devuelve la emoción predominante.

        Parámetros:
            texto (str): El texto a analizar.

        Return:
            str: La emoción predominante detectada en el
            texto o "No disponible" si no se puede detectar.
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

    def enriquecer_prompt(self, texto: str, emocion, personalidad, emocion_diario, resumen, objetivos):
        """
        Enriquece el prompt con la emoción y el texto proporcionados.

        Parámetros:
            texto (str): El texto proporcionado por el usuario.
            emocion (str): La emoción detectada en el texto.
            personalidad (str): La personalidad del usuario.
            emocion_diario (str): La emoción diaria del usuario.
            resumen (str): El resumen de la entrada del diario.
            objetivos (str): Los objetivos personales del usuario.
        
        Return:
            str: El prompt enriquecido con la información proporcion
        """
        return f"Responde en función de la emoción “{emocion}” manifestada por una persona de personalidad {personalidad}, quien ha experimentado recientemente sentimientos de {emocion_diario} debido a {resumen}. Si la situación lo permite, ofrece un consejo práctico que le ayude a alcanzar sus objetivos personales: {objetivos}. Analiza y responde basándote en el siguiente texto: {texto}"

    def mostrar_chatbot(self):
        """
        Muestra la interfaz del chatbot en Streamlit.
        """
        st.title("Chatbot Empático")
        user_input = st.text_input("Escribe algo...")

        if user_input:
            emocion = self.analizar_emocion(user_input)  # Detecta la emoción del texto
            st.write(f"Emoción detectada: {emocion}")

            # Obtener información desde los archivos de texto   
            personalidad, emocion_diario, resumen, objetivos = self.obtener_info_desde_txt()

            # Crear el prompt enriquecido
            prompt_rico = self.enriquecer_prompt(user_input, emocion, personalidad, emocion_diario, resumen, objetivos)
            st.write(self.llamar_chatbot(prompt=prompt_rico))  # Llama al chatbot con el prompt enriquecido

    def llamar_chatbot(self, prompt, model="mistral-small-latest", max_tokens=150, system_personality="Eres un asistente muy amable, siempre buscando animar a la gente"):
        """
        Envía una consulta al chatbot de Mistral con el prompt proporcionado.

        Parámetros:
            prompt (str): El mensaje que se enviará al chatbot.
            model (str): El modelo a utilizar (por defecto "mistral-small-latest").
            max_tokens (int): La cantidad máxima de tokens para la respuesta.

        Retorna:
            str: La respuesta generada por el chatbot, o False en caso de error.
        """
        api_url = "https://api.mistral.ai/v1/chat/completions"  # URL de la API de Mistral
        api_key = "fxjfZhsoN3PYMis5poL5rs8AHicjlwHO"  # Reemplaza con tu API key real

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