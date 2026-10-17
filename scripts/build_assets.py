#!/usr/bin/env python3
"""Generate the AB distribution from the two editable optical masters.

Requires Python 3.11+, fontTools, and Inkscape for PNG exports.
The logo masters are authored vectors. This script never reconstructs their
letterforms from a font and never overwrites them.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
INK, BLUE, WHITE = '#070808', '#065CFB', '#FFFFFF'
NS = 'http://www.w3.org/2000/svg'

def recolor(source: str, replacements: dict[str, str], title: str) -> str:
    for before, after in replacements.items():
        source = source.replace(before, after)
    a, b = source.index('<title '), source.index('</title>')
    head = source[a:source.index('>', a)+1]
    return source[:a]+head+escape(title)+source[b:]

def inner(svg: str) -> str:
    return svg[svg.index('>')+1:svg.rindex('</svg>')]

def glyph_paths(text: str, font: TTFont, x: float, baseline: float, size: float) -> str:
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size/font['head'].unitsPerEm
    output = []
    for char in text:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        path = pen.getCommands()
        if path:
            output.append('<path d="'+path+'"/>')
        x += glyph.width*scale
    return ''.join(output)

def wrapper(content: str, title: str, vb: str, desc: str) -> str:
    return f'<svg xmlns="{NS}" viewBox="{vb}" fill="none" role="img" aria-labelledby="asset-title asset-desc"><title id="asset-title">{escape(title)}</title><desc id="asset-desc">{escape(desc)}</desc>{content}</svg>\n'

def build() -> None:
    logo = ROOT/'assets/logo'
    master = (logo/'ab-primary.svg').read_text()
    compact = (logo/'ab-compact.svg').read_text()
    variants = {
        'ab-reverse.svg': recolor(master, {INK:WHITE}, 'AB — assinatura reversa'),
        'ab-black.svg': recolor(master, {BLUE:INK}, 'AB — assinatura monocromática preta'),
        'ab-white.svg': recolor(master, {INK:WHITE, BLUE:WHITE}, 'AB — assinatura monocromática branca'),
        'ab-compact-reverse.svg': recolor(compact, {INK:WHITE}, 'AB — assinatura compacta reversa'),
    }
    for name, source in variants.items():
        (logo/name).write_text(source)
    font_path = ROOT/'assets/fonts/Sora-Variable.ttf'
    font = instantiateVariableFont(TTFont(font_path, recalcTimestamp=False), {'wght':600}, inplace=False, updateFontNames=True)
    small = instantiateVariableFont(TTFont(font_path, recalcTimestamp=False), {'wght':400}, inplace=False, updateFontNames=True)
    mark = inner(master)
    # Scaled copy is a derived lockup, not a change to the optical master.
    lettering = glyph_paths('Alexandre Belo', font, 730, 288, 82)
    descriptor = glyph_paths('ED&IA', small, 734, 361, 34)
    lockup = wrapper('<g id="ab-signature" transform="translate(0 90) scale(.7)">'+mark+'</g><g id="signature-name" fill="'+INK+'">'+lettering+'</g>', 'Alexandre Belo — assinatura horizontal', '0 0 1530 600', 'Monograma AB e nome Alexandre Belo em contornos Sora. Sem dependências de fonte.')
    edia = wrapper('<g id="ab-signature" transform="translate(0 90) scale(.7)">'+mark+'</g><g id="signature-name" fill="'+INK+'">'+lettering+'</g><g id="signature-descriptor" fill="'+INK+'">'+descriptor+'</g>', 'Alexandre Belo — ED e IA', '0 0 1530 600', 'Assinatura horizontal com o identificador literal ED&IA. Não define uma expansão jurídica da sigla.')
    # Imported master title/description IDs are internal and do not clash with wrapper IDs.
    for name, source in {'ab-alexandre-belo.svg':lockup, 'ab-edia.svg':edia}.items():
        (logo/name).write_text(source)
        (logo/name.replace('.svg','-reverse.svg')).write_text(recolor(source,{INK:WHITE}, 'AB — assinatura horizontal reversa'))
    woff = TTFont(font_path, recalcTimestamp=False)
    woff.flavor='woff'
    woff.save(ROOT/'assets/fonts/Sora-Variable.woff')
    graphics=ROOT/'assets/graphics'; graphics.mkdir(parents=True,exist_ok=True)
    root=ET.fromstring(master)
    orbit=root.find('{'+NS+'}g[@id="orbita"]')
    ET.register_namespace('',NS)
    (graphics/'trajectory.svg').write_text(wrapper(ET.tostring(orbit,encoding='unicode'), 'AB — trajetória gráfica', '0 0 1000 600', 'Elemento de apoio extraído da órbita do símbolo. Não substitui a assinatura.'))
    (graphics/'focus-point.svg').write_text(wrapper('<circle id="focus" cx="50" cy="50" r="22.25" fill="'+BLUE+'"/>','AB — ponto de foco','0 0 100 100','Elemento circular de apoio; diâmetro de 44,5 unidades.'))
    paths={
      'observe':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.2 15.2 5.3 5.3"/>',
      'direction':'<path d="M4 20 9 5l11-1-1 11-15 5Z"/><path d="m9 15 6-6"/><circle cx="12" cy="12" r="1"/>',
      'build':'<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 17h6m-3-3v6"/>',
      'learn':'<path d="M20 8a8 8 0 1 0 0 8M20 3v5h-5"/>',
      'arrow-right':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
      'check':'<path d="m4 12 5 5L20 6"/>',
      'close':'<path d="m6 6 12 12M18 6 6 18"/>',
      'focus':'<circle cx="12" cy="12" r="3"/><path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
    }
    ui=ROOT/'assets/icons/ui'; ui.mkdir(parents=True,exist_ok=True)
    for name,path in paths.items():
        svg=wrapper('<g id="icon-'+name+'" fill="none" stroke="'+INK+'" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'+path+'</g>', 'AB — ícone '+name,'0 0 24 24','Ícone funcional original sobre grade de 24 unidades, traço de 1,75 unidades.')
        (ui/(name+'.svg')).write_text(svg)

def render() -> None:
    target=ROOT/'assets/png';target.mkdir(parents=True,exist_ok=True)
    for name, widths in {'ab-primary':[192,512,1024,2048], 'ab-reverse':[512,1024], 'ab-black':[1024], 'ab-white':[1024], 'ab-compact':[64,96,128,192], 'ab-compact-reverse':[64,96,128,192]}.items():
        for width in widths:
            subprocess.run(['inkscape',str(ROOT/'assets/logo'/f'{name}.svg'),'--export-type=png',f'--export-width={width}',f'--export-filename={target/name}-{width}.png'],check=True,capture_output=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--png',action='store_true',help='Also render the transparent PNG distribution with Inkscape.')
    args=parser.parse_args()
    build()
    if args.png:
        render()
    print('AB derivatives generated from the editable masters.')
