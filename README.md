# Instagram Profile & Post Scraper con Playwright

## Descripción

Script desarrollado en Python que utiliza **Playwright** para extraer información visible de un perfil de Instagram, recopilar enlaces de publicaciones y reels, realizar un scraping detallado de cada post (texto, likes, comentarios y fecha), y guardar todos los resultados estructurados en un archivo JSON.

---

## Características

* **Datos de Perfil:** Extrae nombre, biografía, seguidores y seguidos.
* **Scraping de Publicaciones:** Visita cada post/reel para extraer su texto (caption), cantidad de likes, comentarios y fecha.
* **Prevención de Duplicados:** Evita procesar enlaces repetidos durante el desplazamiento (*scroll*).
* **Autenticación Segura:** Utiliza cookies externas independientes del código principal.
* **Exportación JSON:** Guarda toda la información de manera ordenada en un archivo único.

---

## Requisitos

* Python 3.8 o superior
* Playwright

---

## Instalación

1. Clona el repositorio o descarga los archivos del proyecto.
2. Instala las dependencias necesarias mediante el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt

3. Instala el navegador Chromium necesario para Playwright:
    ```bash
    playwright install chromium

---

## Configuración

### 1. Configurar las Cookies (Importante)
> **Nota:** Este programa permite el uso de cookies configuradas manualmente o mediante una extensión del navegador.
Para evitar bloqueos de inicio de sesión, el script requiere cookies válidas:
1. Crea un archivo llamado `cookies.json` en la raíz del proyecto (puedes guiarte de la estructura de `cookiesEjemplo.json`).
2. Exporta tus cookies de sesión de Instagram desde el navegador y pégalas en el archivo `cookies.json`.

> **Advertencia de Seguridad:** Nunca subas tu archivo `cookies.json` a GitHub ni lo compartas públicamente, ya que contiene acceso directo a tu cuenta. El proyecto cuenta con un archivo `.gitignore` para protegerlo automáticamente.

### 2. Parámetros del Script
Abre el archivo `scraper.py` y ajusta el usuario que deseas analizar y el límite de publicaciones:
```python
USERNAME = "nombre_de_usuario" 
MAX_POSTS = 10
```

---

## Ejecución

Ejecuta el script en tu terminal con el siguiente comando:
```bash
python scraper.py
```

--- 

## Tecnologías Utilizadas
1. Python
2. Playwright
3. JSON

