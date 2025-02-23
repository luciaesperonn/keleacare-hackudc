import streamlit as st
import os

class ObjetivosPersonales:
    """
    Clase para gestionar los objetivos personales.
    """
    def __init__(self):
        """
        Inicializa la clase con el nombre del archivo de objetivos.

        Atributos: 
            archivo_objetivos : str
                El nombre del archivo donde se guardan los objetivos. 
                El archivo por defecto es 'objetivos.txt'.
        
        Métodos:
            cargar_objetivos()
                Carga los objetivos previos desde el archivo de texto.
            guardar_objetivos(objetivos)
                Guarda los objetivos en el archivo de texto.
            mostrar_objetivos()
                Muestra la interfaz de objetivos personales en Streamlit.
        """
        self.archivo_objetivos = "objetivos.txt"  # Archivo donde se guardan los objetivos

    def cargar_objetivos(self):
        """
        Carga los objetivos previos desde el archivo de texto.
        Si el archivo no existe, retorna una lista vacía.

        Returns:
            list: Una lista de objetivos personales.
        """
        if os.path.exists(self.archivo_objetivos):
            with open(self.archivo_objetivos, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        return []

    def guardar_objetivos(self, objetivos):
        """
        Guarda los objetivos en el archivo de texto.

        Este método guarda los objetivos en el archivo 'objetivos.txt'.
        Cada objetivo se guarda en una línea separada.

        Parámetros:
            objetivos (list): Una lista de objetivos personales.

        Returns:
            None
        """
        with open(self.archivo_objetivos, "w", encoding="utf-8") as archivo:
            for objetivo in objetivos:
                archivo.write(objetivo + "\n")

    def mostrar_objetivos(self):
        """
        Muestra la interfaz de objetivos personales en Streamlit.

        Esta función permite al usuario escribir y guardar sus objetivos personales.

        Returns:
            None
        """
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