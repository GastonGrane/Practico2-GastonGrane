# Estas pruebas necesitan que la app este corriendo de verdad en docker antes de ejecutar el test (a diferencia de los
# tests de los Ejercicios 1 y 2, que no necesitaban nada levantado).
# Correr primero: docker-compose up --build -d   (desde la carpeta Ejercicio4/)
import requests

BASE_URL = 'http://localhost:8081'


def test_busqueda_no_se_evalua_como_codigo():
    # mando una expresion matematica simple (2*3) como si fuera un texto de busqueda cualquiera
    # si la app sigue vulnerable, la interpreta como codigo SpEL de verdad y la evalua,
    # mostrando el resultado calculado (6) en vez del texto que escribi
    respuesta = requests.get(f'{BASE_URL}/', params={'buscar': '2*3'})
    html = respuesta.text

    # si ya esta mitigada, el mensaje tiene que mostrar "2*3" tal cual, nunca "6"
    # (este es el mismo payload que probe a mano con burp en el practico 2)
    assert 'Resultados buscando por: 6' not in html