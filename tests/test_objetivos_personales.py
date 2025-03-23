import pytest
import sys


sys.path.append('../')  # Agrega la ruta del directorio principal
from objetivos_personales import ObjetivosPersonales 

def test_dummy():
    assert True


@pytest.fixture
def objetivos():
    return ObjetivosPersonales()

@pytest.fixture
def archivo_temporal(tmp_path):
    archivo = tmp_path / "objetivos.txt"
    return archivo

def test_cargar_objetivos_archivo_no_existe(objetivos, tmp_path):
    objetivos.archivo_objetivos = str(tmp_path / "no_existe.txt")
    assert objetivos.cargar_objetivos() == []

def test_guardar_y_cargar_objetivos(objetivos, archivo_temporal):
    objetivos.archivo_objetivos = str(archivo_temporal)
    objetivos.guardar_objetivos(["Aprender Python", "Hacer ejercicio"])
    assert objetivos.cargar_objetivos() == ["Aprender Python\n", "Hacer ejercicio\n"]

def test_guardar_objetivos_vacio(objetivos, archivo_temporal):
    objetivos.archivo_objetivos = str(archivo_temporal)
    objetivos.guardar_objetivos([])
    assert objetivos.cargar_objetivos() == []
