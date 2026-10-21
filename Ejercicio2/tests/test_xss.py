import pathlib
import sys

# necesito que python encuentre app.py, que esta un nivel arriba de tests/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from app import app as flask_app
from init_db import init_db


def test_xss_no_se_ejecuta():
    # reseteo la base para arrancar siempre del mismo estado conocido
    init_db()

    # el test_client de flask me deja simular requests http (get/post) sin tener que levantar un servidor real ni usar docker
    cliente = flask_app.test_client()

    # este es el mismo payload que probe a mano con burp en el practico 2
    payload = "<script>alert('hackeado')</script>"

    # hago un post como si estuviera editando la pelicula con id 1 (Dune) y en vez de poner una descripcion normal, meto el script
    cliente.post('/edit/1', data={
        'nombre': 'Dune: Parte Dos',
        'genero': 'Ciencia Ficcion',
        'director': 'Denis Villeneuve',
        'descripcion': payload,
    })

    # ahora pido de vuelta la pagina de edicion, como si fuera alguien
    # mas entrando a ver/editar esa pelicula despues
    respuesta = cliente.get('/edit/1')
    html = respuesta.data.decode('utf-8')

    # aca esta la prueba en si: si la app sigue vulnerable (tiene el |safe en el template), el script aparece tal cual en el html, listo para
    # ejecutarse en el navegador de quien abra esa pagina. Si ya esta mitigada, jinja2 lo escapa solo y en vez de <script>
    # aparece como texto &lt;script&gt;, entonces el assert de abajo pasa.
    assert payload not in html