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
        Saves a text entry in the FAISS index.

        Args:
            text (str): The text of the entry to be saved.

        This method encodes the text using the embeddings model,
        adds the resulting vector to the FAISS index and saves the index to a file.
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
        Retrieves the most similar entries to a given text using an embeddings model.

        Args:
            text (str): The text for which you want to find similar entries.
            k (int, optional): The number of similar entries to retrieve. Default is 3.

        Returns:
            list: An index list of the most similar entries. If no entries are found, returns an empty list.
        """
        vector = self.modelo_embeddings.encode([texto])
        vector = np.array(vector, dtype=np.float32)
        D, I = self.index.search(vector, k)  # Buscar las k entradas más similares
        return I if len(I) > 0 else []


    def resumir_texto(self, texto, emocion, max_tokens=50, system_personality="You are an agent specializing in very short summaries."):
        """
        Uses a a chatbot to summarize a text based on a given emotion.
        """
        # Crea un prompt para solicitar el resumen del texto
        prompt = f"Please write directly the reason for the feeling {emocion} in this text:{texto}."
        # Llama al método 'llamar_chatbot' del objeto 'chatbot'
        respuesta = self.chatbot.llamar_chatbot(prompt, max_tokens=max_tokens, system_personality=system_personality)
        return respuesta
    
    def mostrar_diario(self):
        """
        Displays the emotional diary interface in Streamlit.

        This method creates an interface in Streamlit where the user can write about his day,
        save the entry and view the entries saved in the journal.
        Args:
            None

        Returns:
            None
        """
        st.title("Emotional Diary")
        user_input = st.text_area("Write about your day...")

        if st.button("Save the entry"):
            emocion = self.analizar_emocion(user_input)
            resumen = self.resumir_texto(texto=user_input, emocion=emocion)
            self.guardar_entrada(resumen)
            st.success("Entry saved successfully!")
            st.write(f"Detected emotion: {emocion}")
            st.write(f"Entry summary: {resumen}")