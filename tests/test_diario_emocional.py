import pytest
import sys
#sys.path.append('../')
from diario_emocional import DiarioEmocional
from unittest.mock import MagicMock

@pytest.fixture
def diario():
    diario = DiarioEmocional()
    diario.chatbot = MagicMock()  # Simular el chatbot
    return diario

@pytest.fixture
def archivo_temporal(tmp_path):
    return tmp_path / "diario.txt"

def test_cargar_diario_archivo_no_existe(diario, tmp_path):
    diario.archivo_diario = str(tmp_path / "no_existe.txt")
    assert diario.cargar_diario() == []

def test_guardar_y_cargar_diario(diario, archivo_temporal):
    diario.archivo_diario = str(archivo_temporal)
    diario.guardar_diario("Hoy fue un buen día")
    assert diario.cargar_diario() == ["Hoy fue un buen día\n"]

def test_resumir_texto(diario):
    diario.chatbot.llamar_chatbot.return_value = "Día positivo"
    resumen = diario.resumir_texto("Hoy me siento feliz", "joy")
    assert resumen == "Día positivo"
    diario.chatbot.llamar_chatbot.assert_called_once()
