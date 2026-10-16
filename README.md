Instagram Profile Scraper
Descripción

Script desarrollado en Python que utiliza Playwright para extraer información visible de un perfil de Instagram, recopilar enlaces de publicaciones y reels, y guardar los resultados en un archivo JSON.

Características
Extrae nombre, biografía, seguidores y seguidos.
Recopila enlaces de publicaciones y reels.
Evita enlaces duplicados.
Guarda los resultados en formato JSON.
Requisitos
Python 3
Playwright
Chromium
Instalación

Instala Playwright y Chromium:

pip install playwright
playwright install chromium

Configuración

En el código, configura el usuario y el número máximo de publicaciones:

USERNAME = "nombre_de_usuario"
MAX_POSTS = 50


También se requiere configurar las cookies de sesión válidas de Instagram.

Ejecución

Ejecuta el script con:

python instagram_scraper.py


Los resultados se guardarán en un archivo llamado nombre_de_usuario_instagram.json.

Tecnologías
Python
Playwright
JSON
Nota

Utiliza el script de forma responsable, respeta la privacidad de los usuarios y no compartas cookies de sesión ni las publiques en repositorios.