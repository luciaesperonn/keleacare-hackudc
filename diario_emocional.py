import streamlit as st
import text2emotion as te
from chatbot import resumir_texto

class DiarioEmocional:
    def __init__(self):
        self.diario = []

    def analizar_emocion(self, texto):
        emocion = te.get_emotion(texto)
        return emocion

    def resumir_texto(self, texto, max_tokens=50, system_personality="Eres un agente especializado en resúmenes, se te pasará un texto y tendrás que resumir en pocas palabras la razón del sentimiento"):
        respuesta = resumir_texto(texto, max_tokens, system_personality)
        return respuesta



    def mostrar_diario(self):
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            
            resumen = self.resumir_texto(user_input)
            if not resumen:
                st.error("No se pudo generar un resumen. Inténtalo de nuevo.")
                return
            emocion = self.analizar_emocion(user_input)
            self.diario.append({"texto": resumen, "emocion": emocion}) # texto es la razón del sentimiento y emocion es el sentimiento
            st.success("Entrada guardada con éxito!")

        if self.diario:
            st.subheader("Tus entradas:")
            for i, entrada in enumerate(self.diario):
                st.write(f"Entrada {i + 1}: {entrada['texto']}")
                st.write(f"Emoción detectada: {entrada['emocion']}")