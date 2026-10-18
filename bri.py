from pathlib import Path
import re

src = Path("/mnt/data/Código pegado: html")
html = src.read_text(encoding="utf-8")

# Elegante borde floral en SVG, incrustado como data URI para no depender de imágenes externas.
svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 520">
<defs>
  <radialGradient id="p" cx="35%" cy="30%"><stop stop-color="#f8dcff"/><stop offset=".45" stop-color="#c66be0"/><stop offset="1" stop-color="#743b91"/></radialGradient>
  <linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#7f9c72"/><stop offset=".55" stop-color="#496244"/><stop offset="1" stop-color="#293c29"/></linearGradient>
  <filter id="shadow"><feDropShadow dx="1" dy="3" stdDeviation="3" flood-opacity=".25"/></filter>
</defs>
<!-- tallos -->
<path d="M18 500 C35 405 78 350 130 290 C175 238 206 185 235 112" fill="none" stroke="#506744" stroke-width="7" stroke-linecap="round"/>
<path d="M95 450 C150 394 185 342 202 270 C215 214 250 160 305 125" fill="none" stroke="#5d754d" stroke-width="5"/>
<!-- hojas -->
<g fill="url(#leaf)" filter="url(#shadow)">
 <path d="M61 393 C20 384 11 349 17 330 C49 331 72 350 61 393Z"/>
 <path d="M113 337 C72 324 66 291 78 274 C110 281 128 305 113 337Z"/>
 <path d="M159 278 C126 259 130 229 147 217 C174 230 182 253 159 278Z"/>
 <path d="M202 226 C178 198 190 173 208 166 C230 186 230 207 202 226Z"/>
 <path d="M118 405 C149 374 181 379 193 397 C174 419 145 423 118 405Z"/>
</g>
<!-- rosa principal -->
<g transform="translate(15 15)" filter="url(#shadow)">
 <circle cx="86" cy="92" r="63" fill="url(#p)" opacity=".9"/>
 <g fill="none" stroke="#8a4b9d" stroke-width="7" stroke-linecap="round">
  <path d="M47 93 C48 56 88 44 111 68 C132 91 115 124 85 126 C55 128 35 108 47 78 C59 48 96 44 117 64"/>
  <path d="M59 103 C53 78 71 61 91 66 C113 72 114 97 97 107 C80 117 61 110 59 90 C57 71 77 60 94 69"/>
  <path d="M72 95 C67 82 76 72 87 74 C100 76 102 88 94 95 C86 103 74 101 72 91"/>
 </g>
</g>
<!-- flores pequeñas -->
<g transform="translate(215 65)" fill="url(#p)" stroke="#8a4b9d" stroke-width="2">
 <circle cx="20" cy="20" r="12"/><circle cx="42" cy="20" r="12"/><circle cx="31" cy="40" r="12"/><circle cx="31" cy="20" r="7" fill="#f5d46e"/>
</g>
<g transform="translate(310 115) scale(.72)" fill="url(#p)" stroke="#8a4b9d" stroke-width="2">
 <circle cx="20" cy="20" r="12"/><circle cx="42" cy="20" r="12"/><circle cx="31" cy="40" r="12"/><circle cx="31" cy="20" r="7" fill="#f5d46e"/>
</g>
</svg>'''

import base64
svg64 = base64.b64encode(svg.encode()).decode()

floral_css = f"""
/* ===== Borde floral lila y dorado ===== */
.book-page {{
  border: 1px solid rgba(226,184,87,.58);
  background:
    linear-gradient(rgba(255,253,250,.965),rgba(255,253,250,.965)),
    #fffdfa;
  box-shadow:
    0 10px 30px rgba(0,0,0,.08),
    inset 0 0 0 7px rgba(226,184,87,.10),
    inset 0 0 0 9px rgba(255,255,255,.95);
}}
.book-page::before,
.book-page::after {{
  content:"";
  position:absolute;
  z-index:1;
  pointer-events:none;
  width:185px;
  height:185px;
  background-image:url("data:image/svg+xml;base64,{svg64}");
  background-repeat:no-repeat;
  background-size:contain;
  opacity:.98;
  filter:saturate(1.05) contrast(1.02) drop-shadow(0 4px 5px rgba(66,28,77,.16));
}}
.book-page::before {{ top:-4px; left:-4px; }}
.book-page::after {{ bottom:-4px; right:-4px; transform:rotate(180deg); }}

.double-page .book-page:nth-child(2)::before {{
  transform:scaleX(-1);
  left:auto;
  right:-4px;
}}
.double-page .book-page:nth-child(2)::after {{
  transform:scale(-1);
  left:-4px;
  right:auto;
}}

.page-inner {{ z-index:2; }}

@media(max-width:720px){{
  .book-page::before,.book-page::after {{
    width:135px;
    height:135px;
  }}
  .book-page {{
    padding:clamp(2rem,5vw,3rem);
  }}
}}
"""

# Insertar los estilos justo después de la regla existente de .book-page.
needle = '.book-page{position:relative;overflow:hidden;background:#fffdfa;border-radius:1rem;padding:clamp(2.5rem,5vw,4.5rem);box-shadow:0 10px 30px rgba(0,0,0,0.08)}'
if needle in html and '/* ===== Borde floral lila y dorado ===== */' not in html:
    html = html.replace(needle, needle + floral_css)

# También agregamos un detalle floral muy sutil al fondo de la portada.
cover_css = """
/* Flores decorativas de la portada */
.book-cover::before,.book-cover::after{
  content:"❀";
  position:absolute;
  color:rgba(255,242,194,.78);
  font-size:4.5rem;
  line-height:1;
  text-shadow:0 3px 10px rgba(54,24,68,.25);
  z-index:1;
}
.book-cover::before{top:24px;left:38px;transform:rotate(-18deg)}
.book-cover::after{bottom:24px;right:28px;transform:rotate(22deg)}
"""
if '/* Flores decorativas de la portada */' not in html:
    html = html.replace('    .cover-content{position:relative;', cover_css + '    .cover-content{position:relative;')

out = Path("/mnt/data/invitacion_xv_borde_flores_lilas.html")
out.write_text(html, encoding="utf-8")
print(f"Archivo actualizado: {out}")
print("Se agregó un borde floral lila con rosas, hojas, flores pequeñas y detalles dorados, adaptado también a móvil.")
