import json, random, re, time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


USERNAME = "nombre_usuario"   #cambia el nombre de usuario
MAX_POSTS = 50
COOKIES_JSON = r'''
#Tus cookies aquí
'''


SAMESITE = {"no_restriction": "None", "lax": "Lax", "strict": "Strict", "unspecified": "Lax"}
FIN_BIO = {"seguir", "siguiendo", "seguir también", "mensaje", "follow", "following", "message"}


def convertir_cookies(texto):
    resultado = []
    for c in json.loads(texto):
        ck = {
            "name": c["name"], "value": c["value"], "domain": c["domain"],
            "path": c.get("path", "/"), "secure": c.get("secure", False),
            "httpOnly": c.get("httpOnly", False),
            "sameSite": SAMESITE.get(str(c.get("sameSite", "")).lower(), "Lax"),
        }
        if not c.get("session") and "expirationDate" in c:
            ck["expires"] = int(c["expirationDate"])
        resultado.append(ck)
    return resultado


def pausa(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))


def obtener_perfil(page):
    """Lee el encabezado del perfil y lo separa en campos."""
    page.wait_for_selector("header", timeout=15000)
    texto = page.locator("header").first.inner_text()
    lineas = [l.strip() for l in texto.split("\n") if l.strip()]

    patron = re.compile(
        r"^([\d.,]+(?:\s*(?:mil|M|K))?)\s+(publicaciones|seguidores|seguidos|posts|followers|following)$",
        re.I,
    )
    perfil = {"usuario": USERNAME, "nombre": None, "seguidores": None,
              "seguidos": None, "biografia": ""}

    ultimo_contador = -1
    for i, linea in enumerate(lineas):
        m = patron.match(linea)
        if not m:
            continue
        ultimo_contador = i
        tipo = m.group(2).lower()
        if tipo in ("seguidores", "followers"):
            perfil["seguidores"] = m.group(1)
        elif tipo in ("seguidos", "following"):
            perfil["seguidos"] = m.group(1)


    if len(lineas) > 1 and not patron.match(lineas[1]):
        perfil["nombre"] = lineas[1]


    bio = []
    for linea in lineas[ultimo_contador + 1:]:
        if linea.lower() in FIN_BIO or linea.lower() == USERNAME.lower():
            break
        bio.append(linea)
    perfil["biografia"] = "\n".join(bio)
    return perfil


def recolectar_enlaces(page):
    enlaces = {}   
    sin_nuevos = 0
    while len(enlaces) < MAX_POSTS and sin_nuevos < 10:
        hrefs = page.eval_on_selector_all(
            'a[href*="/p/"], a[href*="/reel/"]', "els => els.map(e => e.href)"
        )
        antes = len(enlaces)
        for h in hrefs:
            m = re.search(r"/(p|reel)/([\w-]+)", h.split("?")[0])
            if m and m.group(2) not in enlaces:
                enlaces[m.group(2)] = f"https://www.instagram.com/{m.group(1)}/{m.group(2)}/"

        sin_nuevos = sin_nuevos + 1 if len(enlaces) == antes else 0
        if sin_nuevos >= 3:
            page.mouse.wheel(0, -600)  
            pausa(1, 2)
        page.mouse.wheel(0, random.randint(900, 1400))  
        pausa(1.5, 3)
    return list(enlaces.values())[:MAX_POSTS]


with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    context = navegador.new_context(
        viewport={"width": 1280, "height": 900}, locale="es-ES",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )
    context.add_cookies(convertir_cookies(COOKIES_JSON))
    page = context.new_page()

    page.goto(f"https://www.instagram.com/{USERNAME}/", wait_until="domcontentloaded")
    pausa(3, 5)

    if "accounts/login" in page.url:
        print("Cookies inválidas o expiradas. Vuelve a exportarlas.")
        navegador.close()
        raise SystemExit

    perfil = obtener_perfil(page)
    print("Perfil:", json.dumps(perfil, ensure_ascii=False, indent=2))

    enlaces = recolectar_enlaces(page)
    print(f"{len(enlaces)} enlaces encontrados")

    resultado = {"perfil": perfil, "enlaces_publicaciones": enlaces}
    with open(f"{USERNAME}_instagram.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("Listo. Resultados en", f"{USERNAME}_instagram.json")
    navegador.close()