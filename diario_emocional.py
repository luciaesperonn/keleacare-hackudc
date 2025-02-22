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
        vector = self.modelo_embeddings.encode([texto])
        self.index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.index, "diario.index")


    def recuperar_entradas_similares(self, texto, k=3):
        vector = self.modelo_embeddings.encode([texto])
        vector = np.array(vector, dtype=np.float32)
        D, I = self.index.search(vector, k)  # Buscar las k entradas más similares
        return I if len(I) > 0 else []

    def mostrar_diario(self):
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")
        if st.button("Guardar entrada"):
            emocion = self.chatbot.analizar_emocion(user_input)
            self.guardar_entrada(user_input)
            st.success("Entrada guardada con éxito!")

        if st.button("Buscar entradas similares"):
            similares = self.recuperar_entradas_similares(user_input)
            if similares.any():
                st.subheader("Entradas similares encontradas:")
                for idx in similares[0]:
                    st.write(f"- Entrada {idx + 1}")
            else:
                st.write("No se encontraron entradas similares.")
