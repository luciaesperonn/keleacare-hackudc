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
        Carga los objetivos previos desde FAISS si existen, o crea un nuevo índice.
        """
        try:
            index = faiss.read_index("objetivos.index")
        except:
            index = faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings
        return index
    
    def agregar_objetivo(self, objetivo):
        """
        Agrega un nuevo objetivo al índice FAISS.
        """
        vector = self.modelo_embeddings.encode([objetivo])
        self.faiss_index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.faiss_index, "objetivos.index")
    
    def mostrar_objetivos(self):
        st.title("Objetivos Personales")
        st.write("Escribe tus objetivos personales. El chatbot los usará para darte recomendaciones personalizadas.")

        # Entrada de nuevos objetivos
        nuevo_objetivo = st.text_input("Escribe un nuevo objetivo:")

        if st.button("Guardar objetivo"):
            if nuevo_objetivo:
                self.agregar_objetivo(nuevo_objetivo)  # Guarda el objetivo en FAISS
                st.success("¡Objetivo guardado con éxito!")
            else:
                st.warning("Por favor, escribe un objetivo antes de guardar.")
