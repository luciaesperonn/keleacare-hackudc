# import streamlit as st

# class PerfiladoPersonalidad:
#     def __init__(self):
#         self.rasgos = {
#             "Openness": 0,
#             "Conscientiousness": 0,
#             "Extraversion": 0,
#             "Agreeableness": 0,
#             "Neuroticism": 0
#         }

#     def calcular_rasgos(self, respuestas):
#         # Simulación de cálculo de rasgos (puedes usar un modelo más avanzado)
#         self.rasgos["Openness"] = respuestas.get("openness", 0)
#         self.rasgos["Conscientiousness"] = respuestas.get("conscientiousness", 0)
#         self.rasgos["Extraversion"] = respuestas.get("extraversion", 0)
#         self.rasgos["Agreeableness"] = respuestas.get("agreeableness", 0)
#         self.rasgos["Neuroticism"] = respuestas.get("neuroticism", 0)

#     def mostrar_perfil(self):
#         st.title("Perfil de Personalidad")
#         st.write("Responde a las siguientes preguntas para conocer tu perfil.")

#         respuestas = {
#             "openness": st.slider("¿Te consideras una persona creativa y abierta a nuevas experiencias?", 0, 10),
#             "conscientiousness": st.slider("¿Eres una persona organizada y responsable?", 0, 10),
#             "extraversion": st.slider("¿Te gusta socializar y estar rodeado de gente?", 0, 10),
#             "agreeableness": st.slider("¿Eres una persona amable y compasiva?", 0, 10),
#             "neuroticism": st.slider("¿Tiendes a sentirte ansioso o estresado con facilidad?", 0, 10)
#         }

#         if st.button("Calcular perfil"):
#             self.calcular_rasgos(respuestas)
#             st.subheader("Tu perfil de personalidad (Big Five):")
#             st.write(self.rasgos)
import streamlit as st
import os

class PerfiladoPersonalidad:
    def __init__(self):
        self.archivo_diario = "diario.txt"  # Mismo archivo que el diario emocional

    def guardar_personalidad(self, personalidad):
        """
        Guarda el resultado del test de personalidad en el archivo diario.txt.
        """
        with open(self.archivo_diario, "a", encoding="utf-8") as archivo:
            archivo.write(f"Personalidad: {personalidad}\n")

    def mostrar_perfil(self):
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