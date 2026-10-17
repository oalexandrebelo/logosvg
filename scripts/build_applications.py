#!/usr/bin/env python3
"""Build standalone AB application artwork and an accessible motion example.

Artwork is vector-native. Text uses the included Sora WOFF, while signatures
use the canonical outlined SVGs. Figma imports the same scene as native text.
"""
from __future__ import annotations
import base64, html, json
from pathlib import Path
import xml.etree.ElementTree as ET
import build_brandbook as b

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/applications'
INK,BLUE,WHITE,PAPER,LINE,MUTED,FOCUS=b.INK,b.BLUE,b.WHITE,b.PAPER,b.LINE,b.MUTED,b.FOCUS

def application(number,name,slug,width,height,nodes,fill=WHITE,physical=None):
    return dict(number=number,name=name,title=name,slug=slug,w=width,h=height,fill=fill,nodes=nodes,physical=physical)

def make_scenes():
    a=[]
    nav=dict(type='group',name='Navegação',x=1092,y=64,w=268,h=24,layout='HORIZONTAL',gap=32,children=[b.text('Projetos',0,0,80,16,INK,'Regular',24),b.text('Método',112,0,68,16,INK,'Regular',24),b.text('Sobre',212,0,56,16,INK,'Regular',24)])
    desktop=[b.svg('primary',80,38,144,86.4),nav,b.line(80,154,1360,154)]
    desktop += [b.stack([b.label('ESTRATÉGIA / DESIGN / IA',0,0,820,color=BLUE),b.text('Clareza para decidir.\nPrecisão para construir.',0,0,848,72,INK,'SemiBold',86,-1.5),b.text('Investigar, dar direção e transformar entendimento\nem experiências que possam evoluir.',0,0,810,24,MUTED,'Regular',38)],80,230,848,28,'Mensagem principal')]
    desktop += [b.panel([b.svg('trajectory',-86,82,520,312,color=BLUE),b.circle(212,368,28,INK)],984,240,376,410,PAPER,24),b.button('Conhecer o trabalho',80,652),b.line(80,772,1360,772)]
    for i,(title,body) in enumerate([('Estratégia','Perguntas, evidências e critérios.'),('Design','Decisões em forma utilizável.'),('Inteligência artificial','Exploração com revisão explícita.')]):
        desktop.append(b.stack([b.text(title,0,0,400,24,INK,'SemiBold',32),b.text(body,0,0,400,17,MUTED,'Regular',26)],80+i*436,822,400,12,'Área / '+title))
    a.append(application(1,'01 — Digital / Desktop','digital-desktop',1440,960,desktop))
    mobile=[b.svg('primary',24,22,96,57.6),b.text('Menu',304,39,62,14,INK,'SemiBold',20),b.line(24,104,366,104),b.label('ESTRATÉGIA / DESIGN / IA',24,143,342,BLUE),b.text('Clareza para\ndecidir.\nPrecisão para\nconstruir.',24,190,342,42,INK,'SemiBold',50,-1),b.text('Investigar, dar direção e transformar entendimento em experiências que possam evoluir.',24,424,342,18,MUTED,'Regular',28),b.button('Conhecer o trabalho',24,564),b.svg('primary',70,664,250,150)]
    a.append(application(2,'02 — Digital / Mobile','digital-mobile',390,844,mobile))
    deck=[b.svg('reverse',104,54,220,132),b.label('CADERNO DE DECISÕES',492,102,1050,LINE),b.text('Da pergunta\nà experiência.',104,310,1692,120,WHITE,'SemiBold',132,-3),b.line(104,774,1816,774,MUTED),b.text('Contexto observado. Critério explícito.\nDecisão de projeto. Resultado verificado.',108,838,1500,30,LINE,'Regular',46),b.label('AB / 01',1648,954,168,LINE)]
    a.append(application(3,'03 — Apresentação / Capa','presentation-cover',1920,1080,deck,INK))
    social=[b.svg('reverse',72,50,272,163.2),b.text('Uma boa decisão\ncomeça com uma\nboa pergunta.',72,322,936,96,WHITE,'SemiBold',112,-2),b.text('Inteligência em trajetória.',76,796,832,30,LINE,'Regular',42),b.circle(942,882,30,FOCUS),b.label('AB / ALEXANDRE BELO',76,968,900,LINE)]
    a.append(application(4,'04 — Social / Quadrado','social-square',1080,1080,social,INK))
    a.append(application(5,'05 — Social / Avatar contextual','avatar',512,512,[b.svg('micro',0,0,512,512)],'none'))
    a.append(application(6,'06 — Cartão / Frente 90 × 50 mm','business-card-front',900,500,[b.svg('reverse',90,34,720,432)],INK,{'width':'90mm','height':'50mm'}))
    card=[b.svg('primary',56,40,168,100.8),b.text('Alexandre Belo',266,62,578,48,INK,'SemiBold',60,-.7),b.text('ED&IA',268,136,530,32,MUTED,'Regular',44),b.line(60,242,840,242,LINE),b.text('Clareza para decidir.\nPrecisão para construir.',60,282,780,32,INK,'Regular',44),b.text('alexandrebelo.com.br',60,416,780,32,BLUE,'Regular',44)]
    a.append(application(7,'07 — Cartão / Verso 90 × 50 mm','business-card-back',900,500,card,WHITE,{'width':'90mm','height':'50mm'}))
    email=[b.svg('primary',0,34,210,126),b.line(242,20,242,180,BLUE,2),b.text('Alexandre Belo',272,28,520,32,INK,'SemiBold',44),b.text('ED&IA',274,82,518,18,MUTED,'Regular',28),b.text('alexandrebelo.com.br',274,130,518,18,BLUE,'Regular',28)]
    a.append(application(8,'08 — Comunicação / Assinatura','communication-signature',800,200,email))
    return a

def export_artwork(scenes):
    OUT.mkdir(parents=True,exist_ok=True)
    encoded=base64.b64encode((ROOT/'assets/fonts/Sora-Variable.woff').read_bytes()).decode()
    for p in scenes:
        physical=p['physical'] or {'width':str(p['w']),'height':str(p['h'])}
        style=f'<style>@font-face{{font-family:Sora;src:url(data:font/woff;base64,{encoded}) format("woff");font-weight:100 800}}</style>'
        bg='' if p['fill']=='none' else f'<rect width="{p["w"]}" height="{p["h"]}" fill="{p["fill"]}"/>'
        content=''.join(b.svg_node(n,f'app-{p["number"]}-{i}') for i,n in enumerate(p['nodes']))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{physical["width"]}" height="{physical["height"]}" viewBox="0 0 {p["w"]} {p["h"]}" role="img" aria-labelledby="application-title"><title id="application-title">{html.escape(p["name"])}</title><defs>{style}</defs>{bg}{content}</svg>\n'
        (OUT/(p['slug']+'.svg')).write_text(svg)
    (OUT/'scene.json').write_text(json.dumps({'schema':'ab-brandbook-scene/1','pages':scenes},ensure_ascii=False,indent=2)+'\n')

def motion():
    ET.register_namespace('','http://www.w3.org/2000/svg')
    ns='{http://www.w3.org/2000/svg}'
    canonical=ET.parse(ROOT/'assets/logo/ab-reverse.svg').getroot()
    solid=ET.parse(ROOT/'assets/graphics/monogram-solid.svg').getroot()
    for el in solid.iter():
        if el.get('fill') not in (None,'none'):el.set('fill',WHITE)
    for g in canonical.findall(ns+'g'):
        if g.get('id')=='monograma':letters=ET.tostring(g,encoding='unicode')
        if g.get('id')=='orbita':
            point=g.find(ns+'circle');g.remove(point);orbit=ET.tostring(g,encoding='unicode');dot=ET.tostring(point,encoding='unicode')
    structure=''.join(ET.tostring(el,encoding='unicode') for el in solid if el.tag.split('}')[-1] not in ('title','desc'))
    graphic=f'<svg viewBox="0 0 1000 600" role="img" aria-labelledby="motion-title"><title id="motion-title">AB — inteligência em trajetória</title><g class="structure">{structure}</g><g class="letters">{letters}</g><g class="orbit">{orbit}</g><g class="point">{dot}</g></svg>'
    document='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AB · Movimento da assinatura</title><link rel="stylesheet" href="../tokens/brand.css"><style>*{box-sizing:border-box}body{margin:0;background:#070808;color:#fff;font:16px/1.5 Sora,system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:48px 24px}h1{font-size:clamp(28px,5vw,56px);font-weight:600;letter-spacing:-.04em;margin:0 0 12px}p{color:#C6CDD9;max-width:72ch}svg{display:block;width:100%;height:auto;overflow:visible}button{font:600 14px/20px Sora,system-ui,sans-serif;color:#fff;background:#065CFB;border:0;border-radius:8px;padding:14px 20px;min-height:48px;cursor:pointer}button:hover{background:#004BD6}button:focus-visible{outline:3px solid #72A4FF;outline-offset:4px}button:disabled{color:#C6CDD9;background:#141A25;cursor:default}.controls{display:flex;align-items:center;gap:24px;flex-wrap:wrap}label{display:flex;gap:10px;align-items:center}input{width:20px;height:20px;accent-color:#065CFB}.structure{opacity:0}.letters,.orbit,.point{opacity:1}.playing .structure{animation:structure 200ms cubic-bezier(.22,1,.36,1) both}.playing .letters,.playing .orbit{animation:reveal 200ms cubic-bezier(.22,1,.36,1) both}.playing .point{transform-origin:930px 169px;animation:focus 600ms cubic-bezier(.22,1,.36,1) both}@keyframes structure{from{opacity:1}to{opacity:0}}@keyframes reveal{from{opacity:0}to{opacity:1}}@keyframes focus{0%,66.6667%{opacity:0;transform:scale(.8)}100%{opacity:1;transform:scale(1)}}.static .structure{opacity:0!important;animation:none!important}.static .letters,.static .orbit,.static .point{opacity:1!important;transform:none!important;animation:none!important}@media(prefers-reduced-motion:reduce){.structure{opacity:0!important;animation:none!important}.letters,.orbit,.point{opacity:1!important;transform:none!important;animation:none!important}}</style><main><h1>Movimento com direção.</h1><p>Uma entrada de 600 ms. Aos 200 ms, estrutura e trajetória estão visíveis; o ponto conclui a assinatura aos 600 ms. A marca permanece estável ao final.</p><div id="stage">GRAPHIC</div><div class="controls"><button type="button" id="replay">Repetir entrada</button><label><input type="checkbox" id="static">Mostrar assinatura estática</label></div><p id="status" role="status" aria-live="polite">A animação respeita a preferência de redução de movimento do sistema.</p><p><a href="../assets/logo/ab-reverse.svg" download style="color:#72A4FF">Baixar a assinatura final em SVG</a> · <a href="../brandbook/index.html" style="color:#72A4FF">Consultar o brandbook</a></p></main><script>const stage=document.querySelector('#stage'),replay=document.querySelector('#replay'),control=document.querySelector('#static'),status=document.querySelector('#status'),preference=matchMedia('(prefers-reduced-motion: reduce)');function update(){const reduced=preference.matches||control.checked;stage.classList.toggle('static',reduced);replay.disabled=reduced;status.textContent=reduced?'Assinatura completa estática. Movimento desativado.':'Entrada única de 600 ms, sem repetição automática.';if(reduced)stage.classList.remove('playing')}function play(){update();if(replay.disabled)return;stage.classList.remove('playing');void stage.offsetWidth;stage.classList.add('playing')}control.addEventListener('change',update);preference.addEventListener('change',update);replay.addEventListener('click',play);play();</script></html>'''
    (ROOT/'examples/logo-motion.html').write_text(document.replace('GRAPHIC',graphic))

if __name__=='__main__':
    ET.register_namespace('','http://www.w3.org/2000/svg')
    b.fonts();scenes=make_scenes();export_artwork(scenes);motion()
    print(f'Built {len(scenes)} vector applications and the 600 ms motion example.')
