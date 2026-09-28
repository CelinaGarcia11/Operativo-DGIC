#!/usr/bin/env python3
"""
Deja las fotos listas para la web: las achica y comprime, sin tocar los originales
de los sobres.

Poner los archivos así, con el número de ALFA como nombre:

    assets/fotos/rostros/alfa29.jpg     -> el rostro, recortado
    assets/fotos/fachadas/alfa29.jpg    -> el frente del domicilio

Acepta .jpg .jpeg .png .webp. Después:

    python3 preparar_fotos.py       # procesa todo
    python3 construir.py            # arma la pagina

Requiere Pillow:  pip install pillow
"""
import os, sys, glob

ANCHOS = {'rostros': 600, 'fachadas': 1200}   # ancho máximo en píxeles
CALIDAD = 82

AQUI = os.path.dirname(os.path.abspath(__file__))

def main():
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit('Falta Pillow. Instalalo con:  pip install pillow')

    total = 0
    for tipo, ancho in ANCHOS.items():
        carpeta = os.path.join(AQUI, 'assets', 'fotos', tipo)
        os.makedirs(carpeta, exist_ok=True)
        for origen in sorted(glob.glob(os.path.join(carpeta, '*'))):
            if not origen.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue
            base = os.path.splitext(os.path.basename(origen))[0].lower()
            destino = os.path.join(carpeta, base + '.jpg')

            im = Image.open(origen)
            im = ImageOps.exif_transpose(im)          # respeta la rotación de la cámara
            im = im.convert('RGB')
            if im.width > ancho:
                alto = round(im.height * ancho / im.width)
                im = im.resize((ancho, alto), Image.LANCZOS)
            im.save(destino, 'JPEG', quality=CALIDAD, optimize=True, progressive=True)

            if origen != destino:
                os.remove(origen)
            kb = os.path.getsize(destino) // 1024
            print(f'{tipo:9} {base:10} {im.width}x{im.height}  {kb} KB')
            total += 1

    print(f'\n{total} fotos listas. Ahora: python3 construir.py')

if __name__ == '__main__':
    main()
