import streamlit as st
import os

class PerfiladoPersonalidad:
    def __init__(self):
        self.archivo_diario = "diario.txt"  # Mismo archivo que el diario emocional

    def guardar_personalidad(self, personalidad):
        """
        Guarda el resultado del test de personalidad en el archivo diario.txt.
        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(f"Personalidad: {personalidad}\n")

    def mostrar_perfil(self):
        st.title("Perfil de Personalidad")
        st.write("Si quieres saber qué personalidad tienes, realiza este test: [Big Five Test](https://bigfive-test.com/es)")
        st.write("Luego, escribe aquí el resultado que obtuviste.")

        personalidad = st.text_input("Introduce tu resultado del test de personalidad:")

        if st.button("Guardar personalidad"):
            if personalidad:
                self.guardar_personalidad(personalidad)
                st.success("¡Personalidad guardada con éxito!")
            else:
                st.warning("Por favor, introduce tu resultado del test.")