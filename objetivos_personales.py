import streamlit as st
import os

class ObjetivosPersonales:
    def __init__(self):
        self.archivo_objetivos = "objetivos.txt"  # Archivo donde se guardan los objetivos

    def cargar_objetivos(self):
        """
        Carga los objetivos previos desde el archivo de texto.
        Si el archivo no existe, retorna una lista vacía.
        """
        if os.path.exists(self.archivo_objetivos):
            with open(self.archivo_objetivos, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def guardar_objetivos(self, objetivos):
        """
        Guarda los objetivos en el archivo de texto.
        """
        with open(self.archivo_objetivos, "w", encoding="utf-8") as archivo:
            for objetivo in objetivos:
                archivo.write(objetivo + "\n")

    def mostrar_objetivos(self):
        st.title("Objetivos Personales")
        st.write("Escribe tus objetivos personales. El chatbot los usará para darte recomendaciones personalizadas.")

        # Cargar objetivos previos
        objetivos = self.cargar_objetivos()

        # Mostrar objetivos existentes
        if objetivos:
            st.subheader("Tus objetivos actuales:")
            for i, objetivo in enumerate(objetivos):
                st.write(f"{i + 1}. {objetivo.strip()}")

        # Entrada de nuevos objetivos
        nuevo_objetivo = st.text_input("Escribe un nuevo objetivo:")

        if st.button("Guardar objetivo"):
            if nuevo_objetivo:
                objetivos.append(nuevo_objetivo)  # Añade el nuevo objetivo a la lista
                self.guardar_objetivos(objetivos)  # Guarda la lista actualizada en el archivo
                st.success("¡Objetivo guardado con éxito!")
            else:
                st.warning("Por favor, escribe un objetivo antes de guardar.")