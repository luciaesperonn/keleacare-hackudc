import streamlit as st
from chatbot import Chatbot
from diario_emocional import DiarioEmocional
from perfilado_personalidad import PerfiladoPersonalidad
from objetivos_personales import ObjetivosPersonales

# Configuración de la página
st.set_page_config(page_title="KeleaCare", layout="wide")

# Menú de navegación
st.sidebar.title("Navigation")
opcion = st.sidebar.radio("Choose an option:", ["Chatbot", "Emotional Diary", "Personality Profile", "Personal Goals"])

# Instancias de los módulos
chatbot = Chatbot()
diario = DiarioEmocional()
perfil = PerfiladoPersonalidad()
objetivos = ObjetivosPersonales()

# Mostrar la opción seleccionada
if opcion == "Chatbot":
    chatbot.mostrar_chatbot()
elif opcion == "Emotional Diary":
    diario.mostrar_diario()
elif opcion == "Personality Profile":
    perfil.mostrar_perfil()
elif opcion == "Personal Goals":
    objetivos.mostrar_objetivos()