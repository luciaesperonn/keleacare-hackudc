import streamlit as st
from chatbot import Chatbot
from diario_emocional import DiarioEmocional
from perfilado_personalidad import PerfiladoPersonalidad
from objetivos_personales import ObjetivosPersonales

# Configuración de la página
st.set_page_config(page_title="KeleaCare", layout="wide")

# Menú de navegación
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Elige una opción:", ["Chatbot", "Diario Emocional", "Perfil de Personalidad", "Objetivos Personales"])

# Instancias de los módulos
chatbot = Chatbot()
diario = DiarioEmocional()
perfil = PerfiladoPersonalidad()
objetivos = ObjetivosPersonales()

# Mostrar la opción seleccionada
if opcion == "Chatbot":
    chatbot.mostrar_chatbot()
elif opcion == "Diario Emocional":
    diario.mostrar_diario()
elif opcion == "Perfil de Personalidad":
    perfil.mostrar_perfil()
elif opcion == "Objetivos Personales":
    objetivos.mostrar_objetivos()