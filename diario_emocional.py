import streamlit as st
import text2emotion as te

class DiarioEmocional:
    def __init__(self):
        self.diario = []

    def analizar_emocion(self, texto):
        emocion = te.get_emotion(texto)
        return emocion

    def mostrar_diario(self):
        st.title("Diario Emocional")
        user_input = st.text_area("Escribe sobre tu día...")

        if st.button("Guardar entrada"):
            emocion = self.analizar_emocion(user_input)
            self.diario.append({"texto": user_input, "emocion": emocion})
            st.success("Entrada guardada con éxito!")

        if self.diario:
            st.subheader("Tus entradas:")
            for i, entrada in enumerate(self.diario):
                st.write(f"Entrada {i + 1}: {entrada['texto']}")
                st.write(f"Emoción detectada: {entrada['emocion']}")