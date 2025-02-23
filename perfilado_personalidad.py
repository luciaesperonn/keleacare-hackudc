import streamlit as st
import os

class PerfiladoPersonalidad:
    """
    Clase que permite guardar el resultado del test de personalidad y guardarlo en un archivo
    
    Esta clase permite guardar los resultados de un test de personalidad en un archivo de texto 
    llamado 'diario.txt'.
    """
    def __init__(self):
        """
        Este método configura el nombre del archivo donde se guardarán los resultados del test de personalidad 
        y permite el uso de este archivo en los métodos de la clase.
        """
        self.archivo_diario = "diario.txt"  # Mismo archivo que el diario emocional

    def guardar_personalidad(self, personalidad):
        """
        Guarda el resultado del test de personalidad en el archivo 'diario.txt'.

        Este método agrega el resultado del test de personalidad al archivo de texto 'diario.txt'. 
        El texto se agrega al final del archivo, y el formato incluye la palabra "Personalidad:" seguida 
        del valor ingresado por el usuario.
        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(f"Personalidad: {personalidad}\n")

    def mostrar_perfil(self):
        """
        Muestra la interfaz de perfil de personalidad en Streamlit.
        
        Este método genera una interfaz interactiva en Streamlit, donde el usuario obtiene 
        un enlace para realizar el test de personalidad y luego interpretar el resultado obtenido.
        """
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