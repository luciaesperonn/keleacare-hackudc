import streamlit as st
import os

class PerfiladoPersonalidad:
    def __init__(self):
        self.archivo_personalidad = "personalidad.txt"  # Archivo específico para personalidad

    def guardar_personalidad(self, personalidad):
        """
        Guarda el resultado del test de personalidad en el archivo personalidad.txt.
        """
        with open(self.archivo_personalidad, "a", encoding="utf-8") as archivo:
            archivo.write(f"{personalidad}\n")  # Guarda solo la personalidad

    def cargar_personalidad(self):
        """
        Carga la última personalidad guardada desde el archivo personalidad.txt.
        """
        if os.path.exists(self.archivo_personalidad):
            with open(self.archivo_personalidad, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                return lineas[-1].strip() if lineas else "No disponible"
        return "No disponible"

    def mostrar_perfil(self):
        st.title("Perfil de Personalidad")
        st.write("Si quieres saber qué personalidad tienes, realiza este test: [Big Five Test](https://bigfive-test.com/es)")
        st.write("Luego, escribe aquí el resultado que obtuviste.")

        # Mostrar la última personalidad guardada
        ultima_personalidad = self.cargar_personalidad()
        st.write(f"Última personalidad guardada: {ultima_personalidad}")

        # Entrada de texto para la nueva personalidad
        personalidad = st.text_input("Introduce tu resultado del test de personalidad:")

        if st.button("Guardar personalidad"):
            if personalidad:
                self.guardar_personalidad(personalidad)
                st.success("¡Personalidad guardada con éxito!")
            else:
                st.warning("Por favor, introduce tu resultado del test.")