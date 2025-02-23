import streamlit as st
import os
 
class PerfiladoPersonalidad:
    """
    Clase para gestionar el perfilado de personalidad.

    Esta clase permite guardar, cargar y mostrar el perfil de personalidad de un usuario, utilizando
    un archivo de texto específico para almacenar los resultados del test de personalidad.

    Atributos:
    ----------
    archivo_personalidad : str
        El nombre del archivo donde se guardan los resultados del test de personalidad. 
        El archivo por defecto es 'personalidad.txt'.
    """

    def __init__(self):
        """
        Inicializa la clase con el nombre del archivo de personalidad."""
        self.archivo_personalidad = "personalidad.txt"  # Archivo específico para personalidad
 
    def guardar_personalidad(self, personalidad):
        """
        Guarda el resultado del test de personalidad en el archivo 'personalidad.txt'.

        Este método agrega el resultado del test de personalidad al archivo 'personalidad.txt'. 
        El texto se agrega al final del archivo, guardando solo el valor de la personalidad introducida.

        Args:
        -----
        personalidad (str): El resultado del test de personalidad obtenido por el usuario.

        Returns:
        --------
        None
        """
        with open(self.archivo_personalidad, "a", encoding="utf-8") as archivo:
            archivo.write(f"{personalidad}\n")  # Guarda solo la personalidad
 
    def cargar_personalidad(self):
        """
        Carga la última personalidad guardada desde el archivo 'personalidad.txt'.

        Este método lee el archivo 'personalidad.txt' y devuelve la última línea del archivo, 
        que corresponde al último resultado del test de personalidad guardado. Si el archivo está vacío 
        o no existe, retorna "No disponible".

        Returns:
        --------
        str: La última personalidad guardada o un mensaje indicando que no hay personalidad disponible.
        """
        if os.path.exists(self.archivo_personalidad):
            with open(self.archivo_personalidad, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                return lineas[-1].strip() if lineas else "No disponible"
        return "No disponible"
 
    def mostrar_perfil(self):
        """
        Muestra la interfaz del perfil de personalidad en Streamlit.

        Este método genera una interfaz interactiva en Streamlit, donde el usuario puede obtener un enlace 
        para realizar el test de personalidad Big Five y luego ingresar el resultado obtenido en un campo de texto.
        Si el usuario introduce un resultado, este se guarda en el archivo 'personalidad.txt'. Además, se muestra 
        la última personalidad guardada.

        Args:
        -----
        None

        Returns:
        --------
        None
        """
        st.title("Perfil de Personalidad")
        st.write("Si quieres saber qué personalidad tienes, realiza este test: [Big Five Test](https://bigfive-test.com/es)")
        st.write("Luego, escribe aquí el resultado que obtuviste.")
 
        # Mostrar la última personalidad guardada
        ultima_personalidad = self.cargar_personalidad()
        st.write(f"Última personalidad guardada: {ultima_personalidad}")
 
        # Entrada de texto para la nueva personalidad
        personalidad = st.text_input("Introduce tu resultado del test de personalidad:")
 
        if st.button("Guardar personalidad"):
            if personalidad:
                self.guardar_personalidad(personalidad)
                st.success("¡Personalidad guardada con éxito!")
            else:
                st.warning("Por favor, introduce tu resultado del test.")