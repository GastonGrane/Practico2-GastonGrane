import pathlib
import sys

# necesito que python encuentre app.py, que esta un nivel arriba de tests/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app import app as flask_app, buscar_funciones
from init_db import init_db


def test_busqueda_normal_funciona():
    # reseteo la base para saber bien que hay cargado
    init_db()
    with flask_app.app_context():
        resultados = buscar_funciones('Dune')
    # busco Dune, tiene que aparecer algo, si no algo esta mal
    assert len(resultados) > 0


def test_inyeccion_sql_no_funciona():
    init_db()
    with flask_app.app_context():
        # este es el mismo payload que probe a mano con Burp en el practico 2
        # si la app sigue vulnerable esto me trae TODAS las funciones (21)
        resultados = buscar_funciones("' OR 1=1 --")
    # no deberia encontrar nada, porque ninguna pelicula se llama asi
    assert len(resultados) == 0