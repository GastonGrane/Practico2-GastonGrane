import requests
# Estas pruebas necesitan que la app este corriendo de verdad en docker antes de ejecutar el test (a diferencia de los
# tests de los Ejercicios 1 y 2, que no necesitaban nada levantado).
# Correr primero: docker-compose up --build -d   (desde la carpeta Ejercicio3/)
BASE_URL = 'http://localhost:8081'


def test_subir_archivo_html_es_rechazado():
    # armo un archivo falso en memoria, no necesito un archivo real en disco para esto
    # el (nombre, contenido, content-type) es el mismo formato que usa requests para simular un upload
    archivo_malicioso = {
        'afiche': ('ataque.html', b"<script>alert('hackeado')</script>", 'text/html'),
    }

    # pego la request de upload directo a la app que esta corriendo en docker, como hice a mano con burp
    # pongo allow_redirects=False porque si la app acepta el archivo, redirige al buscador (302) y no quiero que
    # la libreria "siga" esa redireccion sola, quiero ver el codigo de estado real de la respuesta al upload
    respuesta = requests.post(f'{BASE_URL}/upload/1', files=archivo_malicioso, allow_redirects=False)

    # si la app sigue vulnerable, acepta cualquier archivo y redirige (302), como si hubiera subido una imagen real
    # si ya esta mitigada, rechaza el .html por la extension y tira una excepcion (devuelve 500, no 302)
    assert respuesta.status_code != 302