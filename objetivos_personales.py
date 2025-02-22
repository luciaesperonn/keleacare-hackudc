import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class ObjetivosPersonales:
    def __init__(self):
        self.modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        self.faiss_index = self.cargar_objetivos()
    
    def cargar_objetivos(self):
        """
        Load previous targets from FAISS if they exist, or create a new index.
        """
        try:
            index = faiss.read_index("objetivos.index")
        except:
            index = faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings
        return index
    
    def agregar_objetivo(self, objetivo):
        """
        Adds a new target to the FAISS index.
        """
        vector = self.modelo_embeddings.encode([objetivo])
        self.faiss_index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.faiss_index, "objetivos.index")
    
    def mostrar_objetivos(self):
        st.title("Personal Goals")
        st.write("Enter your personal goals. The chatbot will use them to give you personalized recommendations.")

        # Entrada de nuevos objetivos
        nuevo_objetivo = st.text_input("Write a new goal:")

        if st.button("Save the goal"):
            if nuevo_objetivo:
                self.agregar_objetivo(nuevo_objetivo)  # Guarda el objetivo en FAISS
                st.success("Goal successfully saved!")
            else:
                st.warning("Please write a goal before saving.")
