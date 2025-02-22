import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class PerfiladoPersonalidad:
    def __init__(self):
        self.modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        self.faiss_index = self.cargar_perfiles()
    
    def cargar_perfiles(self):
        """
        Load the index FAISS with profiles of personality if it exists, or create a new one.
        """
        try:
            index = faiss.read_index("personalidades.index")
        except:
            index = faiss.IndexFlatL2(384)  # Dimensión del modelo de embeddings
        return index
    
    def guardar_personalidad(self, personalidad):
        """
        Save the personality test result in FAISS.
        """
        vector = self.modelo_embeddings.encode([personalidad])
        self.faiss_index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.faiss_index, "personalidades.index")
    
    def mostrar_perfil(self):
        st.title("Personality Profile")
        st.write("If you want to know what personality you have, take this test: [Big Five Test](https://bigfive-test.com/es)")
        st.write("Then, write the result you got here.")

        personalidad = st.text_input("Enter your personality test result:")

        if st.button("Save personality"):
            if personalidad:
                self.guardar_personalidad(personalidad)
                st.success("Personality saved successfully!")
            else:
                st.warning("Please enter your test result.")
