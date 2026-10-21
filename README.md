# CineBuscador - Práctico 4: Tests automatizados

> **Disclaimer:** Los tests fueron escritos y ejecutados por mí, en mi propia máquina virtual, para las dos ramas (`main` y `practico-2`). Conté con asistencia de una herramienta de IA para la ayuda en la estructura de los tests, resolver problemas de configuración (Maven, versiones de Java, Docker) y redactar esta sección.

Esta rama (`main`) tiene el código **vulnerable** original. Los tests de abajo deben **fallar** acá, y **pasar** en la rama `practico-2` (que tiene las mitigaciones). El informe completo del Práctico 2 (PoC + mitigaciones de cada vulnerabilidad) está en el `README.md` de la rama `practico-2`.

## Requisitos previos

Para correr los tests hacen falta instalados:

- **Python 3 con `pip`** (para los Ejercicios 1, 2, 3 y 4). En Kali ya viene instalado por defecto, se puede confirmar con:
  ```bash
  python3 --version
  ```

- **Maven con un JDK** (para el Ejercicio 5). En Kali no instala solo con `apt install maven` (trae únicamente el JRE, sin compilador), hace falta también el JDK completo:
  ```bash
  sudo apt update
  sudo apt install -y maven openjdk-25-jdk
  ```
  El proyecto pide Java 17, pero un JDK más nuevo (acá quedó la 25, que es lo único que ofrece el repo rolling de Kali) compila igual apuntando a esa versión, no hace falta que coincida exacto.

- **Docker y docker-compose** (para los Ejercicios 3 y 4, que son pruebas de integración contra la app real corriendo). Ya debería estar instalado desde el Práctico 1/2; se puede confirmar con:
  ```bash
  docker --version
  docker-compose --version
  ```

## Cómo correr los tests

Agregué pruebas automatizadas para cada vulnerabilidad del Práctico 2, que confirman que la mitigación sigue funcionando (y que fallarían si alguien reintrodujera el bug sin querer).

### Ejercicio 1 - SQLi (Pytest)

```bash
cd Ejercicio1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Ejercicio 2 - XSS (Pytest)

```bash
cd Ejercicio2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Ejercicio 3 - File Upload (prueba de integración, necesita Docker levantado)

```bash
cd Ejercicio3
docker-compose up --build -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Ejercicio 4 - SSTI (prueba de integración, necesita Docker levantado)

```bash
cd Ejercicio4
docker-compose up --build -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Ejercicio 5 - Almacenamiento inseguro (JUnit)

```bash
cd Ejercicio5
mvn test
```
