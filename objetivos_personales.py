import streamlit as st

class ObjetivosPersonales:
    def __init__(self):
        self.objetivos = []

    def generar_objetivos(self, perfil):
        if perfil["Neuroticism"] > 5:
            self.objetivos.append("Reducir el estrés y la ansiedad.")
        if perfil["Extraversion"] < 5:
            self.objetivos.append("Aumentar la interacción social.")

    def mostrar_objetivos(self):
        st.title("Objetivos Personales")
        st.write("Aquí tienes tus objetivos personalizados:")

        if st.button("Generar objetivos"):
            perfil = {"Neuroticism": 7, "Extraversion": 3}  # Ejemplo de perfil
            self.generar_objetivos(perfil)
            st.success("Objetivos generados con éxito!")

        if self.objetivos:
            st.subheader("Tus objetivos:")
            for objetivo in self.objetivos:
                st.write(f"- {objetivo}")