import sys
sys.path.append('../')  # Agrega la ruta del directorio principal
import pytest
from unittest.mock import mock_open, patch
from perfilado_personalidad import PerfiladoPersonalidad

@pytest.fixture
def perfilado():
    """Crea una instancia de PerfiladoPersonalidad para las pruebas."""
    return PerfiladoPersonalidad()

def test_guardar_personalidad(perfilado):
    """Prueba que el método guardar_personalidad escriba en el archivo correctamente."""
    personalidad_test = "Introvertido"

    with patch("builtins.open", mock_open()) as mocked_file:
        perfilado.guardar_personalidad(personalidad_test)
        # Verifica que el archivo se abrió en modo 'a' (append)
        mocked_file.assert_called_once_with("personalidad.txt", "a", encoding="utf-8")
        # Verifica que se escribió la personalidad en el archivo
        mocked_file().write.assert_called_once_with("Introvertido\n")

def test_cargar_personalidad_con_datos(perfilado):
    """Prueba que cargar_personalidad devuelva la última línea del archivo cuando hay datos."""
    contenido_mock = "Extrovertido\nAmigable\nAnalítico\n"

    with patch("builtins.open", mock_open(read_data=contenido_mock)), patch("os.path.exists", return_value=True):
        resultado = perfilado.cargar_personalidad()
        assert resultado == "Analítico"  # Última línea del archivo

def test_cargar_personalidad_sin_datos(perfilado):
    """Prueba que cargar_personalidad devuelva 'No disponible' si el archivo está vacío."""
    with patch("builtins.open", mock_open(read_data="")), patch("os.path.exists", return_value=True):
        resultado = perfilado.cargar_personalidad()
        assert resultado == "No disponible"

def test_cargar_personalidad_archivo_no_existe(perfilado):
    """Prueba que cargar_personalidad devuelva 'No disponible' si el archivo no existe."""
    with patch("os.path.exists", return_value=False):
        resultado = perfilado.cargar_personalidad()
        assert resultado == "No disponible"
