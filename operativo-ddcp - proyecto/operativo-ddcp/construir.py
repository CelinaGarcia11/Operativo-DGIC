#!/usr/bin/env python3
"""
Genera las dos salidas del operativo a partir de datos.json:

  1. index.html                      -> version para editar y ver en VS Code
  2. dist/OPERATIVO DDCP - 57 ALFA.html -> archivo unico para mandar por WhatsApp
     (todo embebido: estilos, script y escudo; funciona sin internet)

Uso:   python3 construir.py
"""
import base64, html, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
def ruta(*p): return os.path.join(AQUI, *p)

MID_MYMAPS = '14AjdFykVaFdksTAxMjMvi9UzfzBmQ7o'   # mapa del operativo en My Maps
e = html.escape

# Miniatura de la fachada que se embebe en el archivo unico de dist/.
# EMBEBER_FOTOS = False -> ese archivo sale liviano, sin fotos.
EMBEBER_FOTOS = True
ANCHO_MINI = 460


def imagen(tipo, n):
    """Ruta relativa de la imagen si esta cargada, o None."""
    p = os.path.join('assets', 'fotos', tipo, f'alfa{n}.jpg')
    return p if os.path.exists(ruta(p)) else None


def imagen_embebida(tipo, n):
    """La misma imagen como data URI, achicada, para el archivo unico de dist/."""
    p = imagen(tipo, n)
    if not p or not EMBEBER_FOTOS:
        return None
    try:
        import io
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(ruta(p)).convert('RGB')
    if im.width > ANCHO_MINI:
        im = im.resize((ANCHO_MINI, round(im.height * ANCHO_MINI / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=72, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

def recursos_html(txt):
    partes = [t.strip() for t in re.split(r'[/\-]', txt or '') if t.strip()]
    if not partes:
        return '<span class="val empty">&mdash;</span>'
    return ''.join(f'<span class="tag">{e(p)}</span>' for p in partes)

def construir_cuerpo(rows, escudo_src, embebido=False):
    dame = (lambda t, n: imagen_embebida(t, n)) if embebido else imagen
    chips, fichas = [], []
    for i, r in enumerate(rows):
        n = r['n']
        chips.append(
            f'<a class="chip" href="#alfa{n}" data-n="{n}" '
            f'title="ALFA {n} &mdash; {e(r["objetivo"])}">{n}</a>')

        info = ''
        if r.get('info'):
            info = ('<div class="row info"><span class="lbl">Informaci&oacute;n relevante</span>'
                    f'<span class="val">{e(r["info"])}</span></div>')

        botones = ''
        if r.get('mapa'):
            botones += (f'<a class="mapbtn" href="{e(r["mapa"])}" target="_blank" '
                        'rel="noopener">Ver en Google Maps &uarr;</a>')
        if r.get('lat') is not None:
            mymaps = (f'https://www.google.com/maps/d/viewer?mid={MID_MYMAPS}'
                      f'&ll={r["lat"]}%2C{r["lon"]}&z=19')
            botones += (f'<a class="mapbtn alt" href="{e(mymaps)}" target="_blank" '
                        'rel="noopener">Mapa del operativo &uarr;</a>')
            botones += f'<span class="coord">{r["lat"]}, {r["lon"]}</span>'

        def figura(tipo, alt, epigrafe):
            src = dame(tipo, n)
            if not src:
                return ''
            img = f'<img src="{src}" alt="{alt}" loading="lazy">'
            envuelto = img if embebido else f'<a href="{src}" target="_blank" rel="noopener">{img}</a>'
            return f'<figure class="fachada">{envuelto}<figcaption>{epigrafe}</figcaption></figure>'

        foto = figura('fachadas', f'Frente del domicilio de ALFA {n}', 'Frente del domicilio')
        croquis = figura('croquis', f'Croquis ilustrativo de ALFA {n}', 'Croquis ilustrativo')

        refs = ''
        if r.get('referencias'):
            refs = ('<div class="row refs"><span class="lbl">Descripci&oacute;n del frente</span>'
                    f'<span class="val">{e(r["referencias"])}</span></div>')

        fichas.append(f'''<article class="card ficha" id="alfa{n}" data-n="{n}">
      <div class="card-head"><div class="head-text">
        <span class="code">ALFA {n}</span>
        <h2>{e(r["objetivo"])}</h2>
      </div></div>
      <div class="row dom"><span class="lbl">Domicilio exacto a allanar</span><span class="val">{e(r["domicilio"])}</span>{botones}</div>
      {refs}
      {foto}
      {croquis}
      {info}
      <div class="row"><span class="lbl">Comisionado a cargo</span><span class="val">{e(r["comisionado"]) or "&mdash;"}</span></div>
      <div class="row"><span class="lbl">Recursos asignados</span><span class="tags">{recursos_html(r["recursos"])}</span></div>
      <div class="nav"><span class="pos">{i+1} / {len(rows)}</span>
        <a class="topbtn" href="#indice">&uarr; Volver al &iacute;ndice</a>
        <span class="navbtns">
          <button type="button" class="navbtn" data-dir="-1">&#9664; Anterior</button>
          <button type="button" class="navbtn" data-dir="1">Siguiente &#9654;</button>
        </span></div>
    </article>''')

    return f'''<div class="band"><div class="inner">
  <div class="crest"><img src="{escudo_src}" alt="Escudo de la Direcci&oacute;n Delitos contra la Propiedad &mdash; Polic&iacute;a de C&oacute;rdoba"></div>
  <div class="titles">
    <p class="eyebrow">Polic&iacute;a de C&oacute;rdoba</p>
    <h1>Operativo Direcci&oacute;n de Delitos contra la Propiedad</h1>
  </div>
  <div class="tally">
    <div><b>{len(rows)}</b><span>objetivos</span></div>
  </div>
</div></div>

<div class="inner"><div class="layout">
  <p class="panel-lbl" id="indice">Seleccionar objetivo</p>
  <input class="search" id="q" type="search" placeholder="Buscar objetivo o domicilio" autocomplete="off" aria-label="Buscar objetivo o domicilio">
  <div class="grid">{''.join(chips)}</div>
  {''.join(fichas)}
</div></div>'''

FUENTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
           'family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&'
           'family=IBM+Plex+Sans:wght@400;500;600&'
           'family=IBM+Plex+Mono:wght@500;600&display=swap">')

def main():
    rows = json.load(open(ruta('datos.json'), encoding='utf-8'))
    rows.sort(key=lambda r: r['n'])
    css = open(ruta('styles.css'), encoding='utf-8').read()
    js  = open(ruta('app.js'), encoding='utf-8').read()
    escudo_b64 = 'data:image/png;base64,' + base64.b64encode(
        open(ruta('assets/escudo.png'), 'rb').read()).decode()

    # 1) version para editar
    open(ruta('index.html'), 'w', encoding='utf-8').write(
f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Operativo Delitos contra la Propiedad</title>
{FUENTES}
<link rel="stylesheet" href="styles.css">
</head>
<body>
{construir_cuerpo(rows, 'assets/escudo.png', embebido=False)}
<script src="app.js"></script>
</body>
</html>
''')

    # 2) archivo unico para repartir
    os.makedirs(ruta('dist'), exist_ok=True)
    salida = ruta('dist', 'OPERATIVO DDCP - 57 ALFA.html')
    open(salida, 'w', encoding='utf-8').write(
f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Operativo Delitos contra la Propiedad</title>
{FUENTES}
<style>{css}</style>
</head>
<body>
{construir_cuerpo(rows, escudo_b64, embebido=True)}
<script>{js}</script>
</body>
</html>
''')
    print(f'index.html  -> {len(rows)} objetivos')
    print(f'{salida}  ({os.path.getsize(salida)//1024} KB)')

if __name__ == '__main__':
    main()
