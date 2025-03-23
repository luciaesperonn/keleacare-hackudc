import pytest
from unittest.mock import MagicMock, patch
import torch
from chatbot import Chatbot

@pytest.fixture
def chatbot_instance():
    bot = Chatbot()
    # Evitamos la carga real del modelo y tokenizador para agilizar las pruebas.
    bot.tokenizer = MagicMock()
    bot.model = MagicMock()
    return bot

def test_cargar_info_desde_txt(chatbot_instance, tmp_path):
    # El test está creado para la función que tenemos verificar que funciona 
    # según teníamos pensado, pero tal vez hay que replantearla. Solo obtiene el ultimo objetivo (al usarse con objetivos)

    # Creamos un archivo temporal con contenido.
    archivo = tmp_path / "test.txt"
    archivo.write_text("Linea 1\nLinea 2\nÚltima línea")
    resultado = chatbot_instance.cargar_info_desde_txt(str(archivo))
    assert resultado == "Última línea"

def test_cargar_info_desde_txt_no_existe(chatbot_instance, tmp_path):
    # Probamos cuando el archivo no existe.
    archivo = tmp_path / "no_existe.txt"
    resultado = chatbot_instance.cargar_info_desde_txt(str(archivo))
    assert resultado == "No disponible"

def test_extraer_resumen_y_emocion(chatbot_instance):
    # Caso correcto: el string contiene el separador ' | '.
    resumen, emocion = chatbot_instance.extraer_resumen_y_emocion("Resumen ejemplo | joy")
    assert resumen == "Resumen ejemplo"
    assert emocion == "joy"
    
    # Caso incorrecto: sin separador.
    resumen, emocion = chatbot_instance.extraer_resumen_y_emocion("Sin separador")
    assert resumen == "No disponible"
    assert emocion == "No disponible"

def test_obtener_info_desde_txt(chatbot_instance):
    # Simulamos cargar la información desde archivos
    # El orden esperado es: personalidad, objetivos y luego la línea del diario.
    # La línea del diario debe tener formato "Resumen | emoción"
    chatbot_instance.cargar_info_desde_txt = MagicMock(side_effect=[
        "Personalidad de prueba",  # Para archivo de personalidad
        "Objetivos de prueba",      # Para archivo de objetivos
        "Resumen diario | anger"    # Para archivo de diario
    ])
    resultado = chatbot_instance.obtener_info_desde_txt()
    # Se espera una tupla: (personalidad, emoción_diario, resumen, objetivos)
    assert resultado == ("Personalidad de prueba", "anger", "Resumen diario", "Objetivos de prueba")

def test_analizar_emocion(chatbot_instance):
    # Simulamos el comportamiento del tokenizador y del modelo.
    chatbot_instance.tokenizer.return_value = {"input_ids": [], "attention_mask": []}
    # Creamos logits ficticios: supongamos que chatbot_instance.emotion_labels es:
    # ["sadness", "joy", "love", "anger", "fear", "surprise"]
    # Y el índice 3 (anger) tiene el valor más alto.
    logits = torch.tensor([[0.1, 0.2, 0.05, 0.7, 0.1, 0.05]])
    chatbot_instance.model.return_value.logits = logits
    emocion = chatbot_instance.analizar_emocion("Hoy fue un buen día")
    assert emocion == "anger"

def test_enriquecer_prompt(chatbot_instance):
    prompt = chatbot_instance.enriquecer_prompt(
        texto="Texto de prueba",
        emocion="joy",
        personalidad="extrovertido",
        emocion_diario="tristeza",
        resumen="Resumen diario",
        objetivos="Objetivos personales"
    )
    # Verificamos que todos los argumentos se encuentren en el prompt generado.
    assert "Texto de prueba" in prompt
    assert "joy" in prompt
    assert "extrovertido" in prompt
    assert "tristeza" in prompt
    assert "Resumen diario" in prompt
    assert "Objetivos personales" in prompt

def test_llamar_chatbot(chatbot_instance):
    # Simulamos la respuesta de la API de Mistral usando patch en requests.post.
    with patch("requests.post") as mock_post:
        # Simulamos una respuesta exitosa.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                { "message": { "content": "Respuesta del chatbot" } }
            ]
        }
        mock_post.return_value = mock_response
        respuesta = chatbot_instance.llamar_chatbot("Prompt de prueba")
        assert respuesta == "Respuesta del chatbot"
        
        # Simulamos una respuesta fallida (status code != 200).
        mock_response.status_code = 400
        respuesta_error = chatbot_instance.llamar_chatbot("Otro prompt")
        assert respuesta_error == False
