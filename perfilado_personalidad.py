import streamlit as st

class PerfiladoPersonalidad:
    def __init__(self):
        self.rasgos = {
            "Openness": 0,
            "Conscientiousness": 0,
            "Extraversion": 0,
            "Agreeableness": 0,
            "Neuroticism": 0
        }

    def calcular_rasgos(self, respuestas):
        # Simulación de cálculo de rasgos (puedes usar un modelo más avanzado)
        self.rasgos["Openness"] = respuestas.get("openness", 0)
        self.rasgos["Conscientiousness"] = respuestas.get("conscientiousness", 0)
        self.rasgos["Extraversion"] = respuestas.get("extraversion", 0)
        self.rasgos["Agreeableness"] = respuestas.get("agreeableness", 0)
        self.rasgos["Neuroticism"] = respuestas.get("neuroticism", 0)

    def mostrar_perfil(self):
        st.title("Perfil de Personalidad")
        st.write("Responde a las siguientes preguntas para conocer tu perfil.")

        respuestas = {
            "openness": st.slider("¿Te consideras una persona creativa y abierta a nuevas experiencias?", 0, 10),
            "conscientiousness": st.slider("¿Eres una persona organizada y responsable?", 0, 10),
            "extraversion": st.slider("¿Te gusta socializar y estar rodeado de gente?", 0, 10),
            "agreeableness": st.slider("¿Eres una persona amable y compasiva?", 0, 10),
            "neuroticism": st.slider("¿Tiendes a sentirte ansioso o estresado con facilidad?", 0, 10)
        }

        if st.button("Calcular perfil"):
            self.calcular_rasgos(respuestas)
            st.subheader("Tu perfil de personalidad (Big Five):")
            st.write(self.rasgos)