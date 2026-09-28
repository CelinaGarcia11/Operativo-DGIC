# Operativo — Dirección de Delitos contra la Propiedad

Índice de los 57 objetivos ALFA: domicilio, información relevante, comisionado a
cargo, recursos asignados y acceso al mapa.

> **Uso interno.** Contiene domicilios a allanar y datos de personas
> investigadas. El repositorio debe ser **privado**. Ver *Acceso* al final.

## Archivos

| Archivo | Qué es |
|---|---|
| `datos.json` | **Los datos.** Es lo único que se toca para actualizar información. |
| `index.html` | La página armada. **Se regenera sola**, no editar a mano. |
| `styles.css` | Colores, tipografías y diseño. |
| `app.js` | Buscador, navegación y mostrar una ficha por vez. |
| `assets/escudo.png` | El escudo, recortado en círculo. |
| `assets/fotos/fachadas/` | Foto del frente de cada domicilio: `alfa29.jpg`. |
| `assets/fotos/croquis/` | Croquis ilustrativo de cada objetivo: `alfa29.jpg`. |
| `preparar_fotos.py` | Achica y comprime las fotos nuevas. |
| `construir.py` | Regenera `index.html` y el archivo único de `dist/`. |
| `vercel.json` | Cabeceras: pide a los buscadores que no indexen el sitio. |
| `robots.txt` | Lo mismo, para los rastreadores que lo respetan. |
| `dist/` | El archivo único para mandar por WhatsApp. |

## Trabajar localmente

Abrir la carpeta en VS Code. Para ver la página, extensión **Live Server**:
clic derecho sobre `index.html` → *Open with Live Server*.

## Actualizar los datos

1. Editar `datos.json`.
2. En la terminal, parado en esta carpeta:

       python3 construir.py

3. `git add . && git commit -m "actualiza objetivos" && git push`
   Vercel publica solo en menos de un minuto.

El archivo para WhatsApp queda además en `dist/`.

## Descripción del frente

Cada ficha muestra la descripción del frente de la vivienda, tomada del apartado
*Referencias* de los croquis. Están cargadas 50 de 57; **faltan ALFA 24, 25, 26,
27, 53, 54 y 57**, que no tienen croquis armado. Para sumarlas, agregar el campo
`referencias` en `datos.json` y volver a construir.

### Campos de cada objetivo

    {
      "n": 29,                                   // número de ALFA
      "objetivo": "Orona Iván Alexis",
      "domicilio": "Nueva Zelanda N° 424, ...",
      "info": "...",                             // vacío = la fila no aparece
      "comisionado": "Guzman Florencia",
      "recursos": "MOVIL IDENTIFICABLE",         // se separa por "/" y "-"
      "referencias": "Vivienda construida de ...", // descripción del frente
      "lat": -31.28986,
      "lon": -64.31196,
      "mapa": "https://www.google.com/maps/..."  // pin de Google Maps
    }

Las coordenadas salen del KML `1 - ALFA 01 a 57 - OBJETIVOS.kml`.
El mapa del operativo (My Maps) se configura en `construir.py`, en `MID_MYMAPS`.

## Imágenes (frente del domicilio y croquis)

1. Copiar la imagen a la carpeta que corresponda, con el número de ALFA como nombre:
   `assets/fotos/fachadas/alfa29.jpg` o `assets/fotos/croquis/alfa29.jpg`.
   Sirve `.jpg`, `.jpeg`, `.png` o `.webp`.
2. `pip install pillow` (una sola vez).
3. `python3 preparar_fotos.py` — las achica a 1200 px y las comprime.
4. `python3 construir.py`.

No hace falta cargarlas todas: la ficha muestra cada imagen si el archivo existe y
la omite si no. En la web se ve a lo ancho de la ficha y se abre en grande al tocarla;
en el archivo de `dist/` va embebida como miniatura de 460 px. Para que ese archivo
salga liviano, sin fotos: `EMBEBER_FOTOS = False` al principio de `construir.py`.

Los originales de los sobres están extraídos, uno por objetivo, en
`Escritorio/OPERATIVO/FOTOS PARA LA PAGINA/ALFA <n>/`.

## Publicar en Vercel

1. Subir el repositorio a GitHub **como privado**.
2. En Vercel: *Add New → Project*, importar el repositorio.
3. Framework Preset: **Other**. Sin build command, sin output directory:
   es un sitio estático y `index.html` está en la raíz.
4. *Deploy*.

Cada `git push` vuelve a publicar.

## Cómo funciona la página

Las 57 fichas están escritas dentro del HTML, no generadas al vuelo. Por eso:

- **Con JavaScript**: buscador, botones Anterior/Siguiente, flechas del teclado,
  y una ficha por vez.
- **Sin JavaScript** (visor de documentos de WhatsApp en iPhone): se ven el índice
  y las 57 fichas seguidas, y los números del índice saltan a cada una.

Si se cambia para generar las fichas con JavaScript, deja de verse en el visor de
WhatsApp del iPhone. Es a propósito.

Cada ficha enlaza a dos mapas: el **pin** de Google Maps (abre la app y arranca la
navegación) y el **mapa del operativo** en My Maps, centrado en ese objetivo. El
segundo solo abre para quien tenga acceso a ese mapa.

## Acceso

`vercel.json` y `robots.txt` piden a los buscadores que no indexen el sitio, pero
**eso no es control de acceso**: cualquiera con la dirección entra.

Para que cada comisionado vea solo su objetivo hace falta que el servidor verifique
quién es. Opciones, de menor a mayor trabajo:

- **Deployment Protection** de Vercel (contraseña para todo el sitio). Es de plan
  pago y da una sola clave compartida: limita quién entra, no qué ve cada uno.
- **Función serverless** que reciba un token por comisionado y devuelva únicamente
  su ficha, con los datos fuera de la carpeta pública. Es la primera opción que de
  verdad separa lo que ve cada uno.
- **Identidad institucional** (el usuario de la fuerza). Lo correcto si esto se
  vuelve un sistema y no un operativo puntual.

Poner una clave en el HTML **no sirve**: los datos viajan en el archivo y se leen
desde el código fuente.
