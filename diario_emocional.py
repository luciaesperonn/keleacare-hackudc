import streamlit as st
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sentence_transformers import SentenceTransformer
from chatbot import Chatbot

class DiarioEmocional:
    def __init__(self):
        self.modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = self.cargar_diario()
        self.chatbot = Chatbot()
        self.model_name = "bhadresh-savani/bert-base-uncased-emotion"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

    def cargar_diario(self):
        try:
            index = faiss.read_index("diario.index")
        except:
            index = faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings
        return index

    def guardar_entrada(self, texto):
        """
        Guarda una entrada de texto en el índice FAISS.

        Args:
            texto (str): El texto de la entrada que se va a guardar.

        Este método codifica el texto utilizando el modelo de embeddings,
        añade el vector resultante al índice FAISS y guarda el índice en un archivo.

        Returns:
            None
        """
        vector = self.modelo_embeddings.encode([texto])
        self.index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.index, "diario.index")

    def analizar_emocion(self, texto):
        inputs = self.tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probabilidades = torch.softmax(logits, dim=-1).squeeze().numpy()
        emocion_predominante = self.emotion_labels[np.argmax(probabilidades)]
        return emocion_predominante

    def recuperar_entradas_similares(self, texto, k=3):
        """
        Recupera las entradas más similares a un texto dado utilizando un modelo de embeddings.

        Args:
            texto (str): El texto para el cual se desean encontrar entradas similares.
            k (int, opcional): El número de entradas similares a recuperar. Por defecto es 3.

        Returns:
            list: Una lista de índices de las entradas más similares. Si no se encuentran entradas, retorna una lista vacía.
        """
        vector = self.modelo_embeddings.encode([texto])
        vector = np.array(vector, dtype=np.float32)
        D, I = self.index.search(vector, k)  # Buscar las k entradas más similares
        return I if len(I) > 0 else []


    def resumir_texto(self, texto, emocion, max_tokens=50, system_personality="Eres un agente especializado en resúmenes muy cortos."):
        """
        Utiliza el chatbot para resumir el texto.
        """
        # Crea un prompt para solicitar el resumen del texto
        prompt = f"Por favor, escribe directamente la razón del sentimiento {emocion} en este texto:\n\n{texto}"
        # Llama al método 'llamar_chatbot' del objeto 'chatbot'
        respuesta = self.chatbot.llamar_chatbot(prompt, max_tokens=max_tokens, system_personality=system_personality)
        return respuesta
    
    def mostrar_diario(self):
        """
        Muestra la interfaz del diario emocional en Streamlit.

        Este método crea una interfaz en Streamlit donde el usuario puede escribir sobre su día,
        guardar la entrada y ver las entradas guardadas en el diario.

        Args:
            None

        Returns:
            None
        """
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            emocion = self.analizar_emocion(user_input)
            resumen = self.resumir_texto(texto=user_input, emocion=emocion)
            self.guardar_entrada(resumen)
            st.success("Entrada guardada con éxito!")
            st.write(f"Emoción detectada: {emocion}")
            st.write(f"Resumen de la entrada: {resumen}")