#!/usr/bin/env python3
"""Build the AB brandbook as editable scene data, SVG sheets, HTML and PDF.

The scene is shared by the PDF/SVG renderer and the native Figma importer.
Text remains text in the PDF and Figma; marks remain vector geometry.
Requires Pillow, fontTools and reportlab. No network requests are made.
"""
from __future__ import annotations
import argparse, base64, copy, hashlib, html, json, math, re
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.svgLib.path import parse_path
from fontTools.pens.basePen import BasePen
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'build'
W,H=1920,1080
INK='#070808'; BLUE='#065CFB'; WHITE='#FFFFFF'; PAPER='#F4F6FA'; LINE='#C6CDD9'; MUTED='#566176'; FOCUS='#72A4FF'; DARK='#141A25'
FONT_CACHE={}
SCENES=[]
class PDFPathPen(BasePen):
    """Adapt SVG Béziers to reportlab's canvas path without rasterization."""
    def __init__(self,canvas):
        super().__init__(None)
        self.path=canvas.beginPath()
    def _moveTo(self,p):self.path.moveTo(*p)
    def _lineTo(self,p):self.path.lineTo(*p)
    def _curveToOne(self,p1,p2,p3):self.path.curveTo(*p1,*p2,*p3)
    def _closePath(self):self.path.close()
    def _endPath(self):pass
LOGOS={k:f'assets/logo/ab-{k}.svg' for k in ['primary','reverse','black','white','compact','compact-reverse','alexandre-belo','edia','alexandre-belo-reverse','edia-reverse']}
LOGOS.update(micro='assets/icons/ab-micro.svg',microclear='assets/icons/ab-micro-transparent.svg',microreverse='assets/icons/ab-micro-reverse.svg',trajectory='assets/graphics/trajectory.svg',point='assets/graphics/focus-point.svg',legacy='archive/2025/logoazul.svg',original='brandbook/references/AB-NEW-original.svg')

def fonts():
    p=WORK/'fonts';p.mkdir(parents=True,exist_ok=True)
    weights=[('Regular',400),('Light',300),('SemiBold',600),('Bold',700)]
    source=ROOT/'assets/fonts/Sora-Variable.ttf'
    source_font=TTFont(source,recalcTimestamp=False)
    recipe={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'weights':weights,'preserve_timestamp':True,'recipe_version':2}
    signature=json.dumps(recipe,sort_keys=True,separators=(',',':'))
    stamp=p/'source.json'
    refresh=not stamp.exists() or stamp.read_text()!=signature
    if refresh:FONT_CACHE.clear()
    for style,weight in weights:
        path=p/f'Sora-{style}.ttf'
        if refresh or not path.exists():
            f=instantiateVariableFont(source_font,{'wght':weight},inplace=False,updateFontNames=True)
            f['head'].created=source_font['head'].created
            f['head'].modified=source_font['head'].modified
            f.recalcTimestamp=False
            f.save(path)
        pdfmetrics.registerFont(RLFont('Sora-'+style,str(path)))
    stamp.write_text(signature)

def font(size,style):
    key=(size,style)
    if key not in FONT_CACHE: FONT_CACHE[key]=ImageFont.truetype(str(WORK/'fonts'/f'Sora-{style}.ttf'),int(round(size*4)))
    return FONT_CACHE[key]

def wrap(value,width,size,style='Regular',tracking=0):
    lines=[]
    value=str(value).replace('→',' / ').replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    for paragraph in value.split('\n'):
        current=''
        for word in paragraph.split(' '):
            trial=(current+' '+word).strip()
            measured=font(size,style).getlength(trial)/4+max(0,len(trial)-1)*tracking
            if measured>width-5 and current: lines.append(current);current=word
            else: current=trial
        lines.append(current)
    return lines

def text(value,x,y,width,size=22,color=INK,style='Regular',line=None,tracking=0,name=None):
    line=line or round(size*1.45)
    lines=wrap(value,width,size,style,tracking)
    return dict(type='text',name=name or value.replace('\n',' ')[:64],x=x,y=y,w=width,h=len(lines)*line,text='\n'.join(lines),size=size,line=line,fill=color,style=style,tracking=tracking)

def rect(x,y,w,h,fill=PAPER,r=0,stroke=None,sw=1): return dict(type='rect',name='Superfície',x=x,y=y,w=w,h=h,fill=fill,radius=r,stroke=stroke,sw=sw)
def line(x,y,x2,y2,color=LINE,sw=1,dash=None): return dict(type='line',name='Eixo / separador',x=x,y=y,w=x2-x,h=y2-y,fill=color,sw=sw,dash=dash)
def circle(x,y,r,color=BLUE): return dict(type='circle',name='Ponto de foco',x=x-r,y=y-r,w=2*r,h=2*r,fill=color)
def svg(asset,x,y,w,h=None,viewbox=None,color=None,opacity=1):
    path=LOGOS.get(asset,asset); vb=ET.parse(ROOT/path).getroot().get('viewBox','0 0 100 100').split()
    h=h if h is not None else w*float(vb[3])/float(vb[2])
    return dict(type='svg',name=Path(path).stem,asset=path,x=x,y=y,w=w,h=h,viewBox=viewbox,color=color,opacity=opacity)

def stack(nodes,x,y,w,gap=24,name='Bloco editorial'):
    offset=0
    for n in nodes: n['x']=0;n['y']=offset;offset+=n['h']+gap
    return dict(type='group',name=name,x=x,y=y,w=w,h=max(0,offset-gap),layout='VERTICAL',gap=gap,children=nodes)

def label(value,x,y,w=1000,color=MUTED): return text(value,x,y,w,16,color,'SemiBold',24,1)

def button(value,x,y,state='Default'):
    """Native component specimen with a matching vector fallback for PDF/SVG."""
    bg='#004BD6' if state=='Hover' else PAPER if state=='Disabled' else BLUE
    parts=[rect(0,0,200,48,bg,8)]
    if state=='Focus':parts.append(rect(-3,-3,206,54,'none',7,BLUE,2))
    width=font(14,'SemiBold').getlength(value)/4
    caption=text(value,(200-width)/2,14,width+2,14,MUTED if state=='Disabled' else WHITE,'SemiBold',20)
    if state=='Disabled':caption['opacity']=.6
    parts.append(caption)
    return dict(type='group',name='Botão / '+state,x=x,y=y,w=200,h=48,children=parts,component={'family':'Button','Style':'Primary','State':state,'Label':value})

def panel(nodes,x,y,w,h,bg=PAPER,r=24): return dict(type='group',name='Painel demonstrativo',x=x,y=y,w=w,h=h,fill=bg,radius=r,clip=True,children=nodes)

def sample(mark,x,y,w=530,h=332,bg=PAPER,caption=None):
    children=[svg(mark,28,20,w-56,min(h-64,(w-56)*.6))]
    if caption: children.append(label(caption,28,h-48,w-56,WHITE if bg==BLUE else LINE if bg==INK else MUTED))
    return panel(children,x,y,w,h,bg)

def sheet(copy_item,title=None,dark=False):
    fg=WHITE if dark else INK;sub=LINE if dark else MUTED
    n=copy_item['number']
    page=dict(number=n,title=copy_item['title'],name=f'{n:02d} — {copy_item["title"]}',w=W,h=H,fill=INK if dark else WHITE,nodes=[])
    nodes=page['nodes']
    nodes += [label('AB / ALEXANDRE BELO',104,62,900,fg),label(f'SISTEMA DE IDENTIDADE  /  {n:02d}',1424,62,392,sub),line(104,116,1816,116,DARK if dark else LINE)]
    t=text(title or copy_item['title'],0,0,512,64,fg,'SemiBold',72,-1.5)
    b=text(copy_item['body'],0,0,512,22,sub,'Regular',34)
    k=label(copy_item['kicker'].upper(),0,0,512,FOCUS if dark else BLUE)
    block=stack([k,t,b],104,174,512,28,'Orientação / '+str(n))
    if block['h']>740:
        b=text(copy_item['body'],0,0,512,20,sub,'Regular',32)
        block=stack([k,t,b],104,174,512,24,'Orientação / '+str(n))
    if block['h']>752: raise ValueError(f'Editorial overflow page {n}: {block["h"]}')
    nodes.append(block)
    nodes += [line(104,950,1816,950,DARK if dark else LINE),text(copy_item['notes'],104,972,1550,16,sub,'Regular',24),label(f'{n:02d} / 32',1680,988,140,sub)]
    SCENES.append(page)
    return nodes

def add_tile(nodes,x,y,w,h,num,title,body,icon=None,bg=PAPER):
    heading=text(title,32,78,w-64,32,INK,'SemiBold',40)
    parts=[label(num,32,26,w-64,BLUE),heading,text(body,32,78+heading['h']+20,w-64,20,MUTED,'Regular',30)]
    if icon: parts.append(svg(f'assets/icons/ui/{icon}.svg',w-68,26,32,32))
    nodes.append(panel(parts,x,y,w,h,bg))

def asset_svg(n):
    root=ET.parse(ROOT/n['asset']).getroot()
    if n.get('viewBox'): root.set('viewBox',n['viewBox'])
    if n.get('stretch'): root.set('preserveAspectRatio','none')
    if n.get('color'):
        for element in root.iter():
            if element.get('fill') not in (None,'none'):element.set('fill',n['color'])
            if element.get('stroke') not in (None,'none'):element.set('stroke',n['color'])
    return root

def compose():
    copies=json.loads((ROOT/'brandbook/copy.json').read_text())
    X=696;DW=1120
    titles={2:'Como usar\no sistema',3:'Entender.\nDecidir.\nConstruir.',4:'Princípios\nem prática',5:'Inteligência\nem trajetória',6:'Anatomia\nda assinatura',7:'Evoluir com\ncontinuidade',8:'O vazio também\né desenho',9:'Construção\nmensurável',10:'Principal\ne reversa',11:'Uma autoria.\nDuas assinaturas.',12:'Uma cor.\nMesma presença.',13:'Espaço para\nreconhecer',14:'Uma família.\nTrês escalas.',15:'A marca\ne o fundo',16:'O que rompe\no sistema',17:'Cor com\nfunção',18:'Contraste\nverificado',19:'Sora.\nClara e precisa.',20:'Hierarquia\nsem ruído',21:'A estrutura\ndá liberdade',22:'A trajetória\nfora da marca',23:'Ícones\ne ilustração',24:'Movimento\ncom direção',25:'Precisão\ntambém na voz',26:'Da identidade\nà interface',27:'Presença\ndigital',28:'Pensamento\nbem apresentado',29:'Uma ideia\npor publicação',30:'Assinar com\nclareza',31:'Arquivos\ne manutenção',32:'Fontes\ne decisões'}
    # 01 / Opening: an editorial cover with the genuine vector, not a raster.
    c=copies[0];p=dict(number=1,title=c['title'],name='01 — Inteligência em trajetória',w=W,h=H,fill=INK,nodes=[]);SCENES.append(p);a=p['nodes']
    a += [label('AB / ALEXANDRE BELO',104,66,900,WHITE),label('BRANDBOOK / 2026',1440,66,400,LINE),line(104,122,1816,122,DARK),text('Inteligência\nem trajetória.',104,258,850,112,WHITE,'SemiBold',124,-3),text('Clareza para decidir.\nPrecisão para construir.',110,620,700,30,LINE,'Regular',44),svg('reverse',950,294,840,504),line(104,944,1816,944,DARK),label('IDENTIDADE VISUAL E VERBAL',104,979,800,LINE),label('VERSÃO 1.0 / 32 PRANCHAS',1370,979,470,LINE)]
    for c in copies[1:]:
        n=c['number'];dark=n in (5,22,24)
        a=sheet(c,titles.get(n),dark);fg=WHITE if dark else INK;sub=LINE if dark else MUTED
        if n==2:
            for i,(mark,title,body) in enumerate([('primary','Principal','96 px ou mais\nPrimeira apresentação'),('compact','Compacta','64 a 95 px\nCompensação óptica'),('micro','Micro A·','16 a 63 px\nIdentidade já reconhecida')]):
                yy=186+i*242
                a.append(panel([svg(mark,26,24,240,144 if mark!='micro' else 144),text(title,320,34,730,32,INK,'SemiBold',40),text(body,320,94,730,22,MUTED,'Regular',34)],X,yy,DW,218))
        elif n==3:
            for i,(title,desc) in enumerate([('Direção','Estratégia: formular a pergunta e definir o critério.'),('Forma','Design: organizar a experiência e tornar a decisão utilizável.'),('Capacidade','IA: ampliar exploração e execução com revisão explícita.')]):
                y=188+i*237;a += [label(f'0{i+1}',X,y,100,BLUE),text(title,X+96,y-10,1010,58,INK,'SemiBold',68,-1),text(desc,X+98,y+78,948,26,MUTED,'Regular',40),line(X,y+195,1816,y+195)]
        elif n==4:
            for i,v in enumerate([('01','Evidência','Começar pelo contexto; distinguir dado, hipótese e opinião.','observe'),('02','Clareza','Explicitar o problema, a escolha e o que ela muda.','direction'),('03','Precisão','Fazer a forma e a implementação sustentarem a intenção.','build'),('04','Aprendizado','Observar o uso e rever a decisão com novos sinais.','learn')]):
                add_tile(a,X+(i%2)*576,188+(i//2)*360,544,330,*v)
        elif n==5:
            a += [svg('reverse',X+14,174,1092,655),label('AUTORIA',X+50,830,260,WHITE),label('TRAJETÓRIA',X+407,830,350,FOCUS),label('FOCO',X+900,830,200,WHITE),line(X+98,795,X+98,738,LINE),line(X+483,795,X+483,692,LINE),line(X+994,795,X+994,459,LINE)]
        elif n==6:
            master=ET.parse(ROOT/LOGOS['primary']).getroot();ns='{http://www.w3.org/2000/svg}'
            for gid,name in [('monograma','anatomy-letters'),('orbita','anatomy-orbit')]:
                g=master.find(ns+'g[@id="'+gid+'"]');rr=ET.Element(ns+'svg',{'viewBox':'0 0 1000 600'});rr.append(copy.deepcopy(g));ET.ElementTree(rr).write(ROOT/f'assets/graphics/{name}.svg',encoding='unicode')
            a += [sample('assets/graphics/anatomy-letters.svg',X,188,544,348,caption='01 / AB — AUTORIA'),sample('assets/graphics/anatomy-orbit.svg',X+576,188,544,348,caption='02 / TRAJETÓRIA — CONEXÃO'),svg('primary',X+260,548,560,336),label('03 / O PONTO ESTABELECE FOCO',X+240,900,800,BLUE)]
        elif n==7:
            a += [sample('original',X,188,544,412,caption='ORIGINAL / FIGMA'),sample('primary',X+576,188,544,412,caption='REFINADA / SVG'),text('ALVB  →  AB  →  AB + trajetória',X+32,670,1050,40,INK,'SemiBold',54,-.5),text('A síntese das iniciais está documentada na identidade histórica. A intervenção atual organiza curvas, vazios, cor e enquadramento.',X+32,758,1034,24,MUTED,'Regular',38)]
            a[-4]['children'][0]['viewBox']='2.5 40 200 120'
        elif n==8:
            for i,(title,vb) in enumerate([('Diagonal / passagem','290 330 240 145'),('B / cintura','620 255 210 150'),('Ponto / separação','790 102 190 155')]):
                yy=183+i*244
                a.append(panel([svg('original',18,24,300,160,' '.join(str(v) for v in [float(vb.split()[0])/5+2.5,float(vb.split()[1])/5+40,float(vb.split()[2])/5,float(vb.split()[3])/5])),svg('primary',342,24,300,160,vb),label('ANTES',30,184,260),label('DEPOIS',354,184,260,BLUE),text(title,696,42,375,26,INK,'SemiBold',36)],X,yy,DW,224))
        elif n==9:
            bx=X+40;by=228;s=1.04
            a.append(svg('primary',bx,by,1040,624))
            for yy in (50,550):a.append(line(bx,by+yy*s,bx+1000*s,by+yy*s,LINE,1,[5,5]))
            for xx in (47.5,487.002,569.004,952.25):a.append(line(bx+xx*s,by,bx+xx*s,by+600*s,LINE,1,[5,5]))
            a += [label('ALTURA VISÍVEL: 500 U',bx+15,868,630),label('PONTO: Ø 44,5 U',bx+710,184,360,BLUE),line(bx+930*s-34,by+169*s,bx+930*s+34,by+169*s,BLUE,1),line(bx+930*s,by+169*s-34,bx+930*s,by+169*s+34,BLUE,1)]
        elif n==10:
            a += [sample('primary',X,188,DW,342,WHITE,'PRINCIPAL / BRANCO'),sample('reverse',X,560,DW,342,INK,'REVERSA / PRETO')]
            for box in a[-2:]: box['children'][0].update(x=315,y=14,w=500,h=300)
        elif n==11:
            a += [panel([svg('alexandre-belo',42,-4,1030,348),label('NOME / ASSINATURA INSTITUCIONAL',40,324,1000)],X,188,DW,348),panel([svg('edia',42,-4,1030,348),label('ED&IA / IDENTIFICADOR LITERAL',40,324,1000)],X,568,DW,348)]
        elif n==12:
            for i,(mark,bg,cap) in enumerate([('black',WHITE,'PRETO / FUNDO BRANCO'),('white',INK,'BRANCO / FUNDO PRETO'),('white',BLUE,'BRANCO / FUNDO AZUL'),('black',PAPER,'PRETO / FUNDO CLARO')]):a.append(sample(mark,X+(i%2)*576,188+(i//2)*364,544,336,bg,cap))
        elif n==13:
            bx=X+50;by=278;s=1
            a += [rect(bx-2.5,by,1004.75,600,'#EAF1FF',0,BLUE,1),svg('primary',bx,by,1000,600),rect(bx+47.5,by+50,904.75,500,'none',0,MUTED,1),label('x = 50 u',bx+370,194,400,BLUE),label('PROTEÇÃO CONTADA A PARTIR DO DESENHO VISÍVEL',X,895,DW,MUTED)]
            a += [line(bx+47.5,by-24,bx+47.5,by+52,BLUE,2),line(bx-2.5,by-24,bx-2.5,by+12,BLUE,2),line(bx-2.5,by-18,bx+47.5,by-18,BLUE,2)]
        elif n==14:
            a += [rect(X,188,DW,724,PAPER,24),text('Tamanhos reais em pixels da prancha',X+42,216,1020,26,INK,'SemiBold',36)]
            for i,(mark,size,title) in enumerate([('primary',192,'192 px / principal'),('primary',96,'96 px / principal'),('compact',80,'80 px / compacta'),('compact',64,'64 px / compacta')]):
                yy=300+i*138;a += [svg(mark,X+52,yy,size,size*.6),text(title,X+394,yy+18,630,22,INK,'Regular',34),line(X+40,yy+117,X+1080,yy+117)]
            for i,size in enumerate((16,24,32)):
                a += [svg('micro',X+740+i*104,805,size,size),label(str(size),X+732+i*104,854,90)]
        elif n==15:
            for i,(mark,bg,cap) in enumerate([('primary',WHITE,'01 / CLARO'),('reverse',INK,'02 / ESCURO'),('white',BLUE,'03 / ACENTO'),('black',PAPER,'04 / NEUTRO')]):a.append(sample(mark,X+(i%2)*576,188+(i//2)*364,544,336,bg,cap))
        elif n==16:
            labels=['01 / Não deformar','02 / Não recolorir','03 / Não girar','04 / Não cortar','05 / Não remover o ponto','06 / Não eliminar a proteção']
            for i,title in enumerate(labels):
                sx=X+(i%3)*384;sy=184+(i//3)*366;mark=svg('primary',26,46,292,175)
                if i==0:mark.update(w=308,h=112,y=78,stretch=True)
                if i==1:mark['color']='#B42318'
                if i==2:mark['rotation']=18
                if i==3:mark['viewBox']='170 130 520 310'
                if i==4:mark['hidePoint']=True
                if i==5:mark.update(x=-10,w=384,h=230,y=28)
                a.append(panel([mark,text('×',26,240,42,38,'#B42318','Regular',46),text(title,72,250,266,17,INK,'SemiBold',25)],sx,sy,352,334,PAPER))
        elif n==17:
            for i,(name,hexa) in enumerate([('Ink',INK),('Blue',BLUE),('White',WHITE)]):
                col=WHITE if i<2 else INK;x=X+i*384
                a.append(panel([text(name,30,34,290,38,col,'SemiBold',48),text(hexa,30,298,290,28,col,'Regular',38),label('RGB '+ ' / '.join(str(int(hexa[z:z+2],16)) for z in (1,3,5)),30,356,300,col)],x,188,352,418,hexa))
            for i,(name,hexa) in enumerate([('Paper',PAPER),('Line',LINE),('Muted',MUTED),('Focus',FOCUS)]):
                xx=X+i*288;a += [rect(xx,650,256,150,hexa,12),label(name.upper(),xx,818,256),text(hexa,xx,854,256,22,INK,'Regular',32)]
        elif n==18:
            rows=[('Branco / preto',WHITE,INK,'20,05:1','Texto normal AA'),('Branco / azul',WHITE,BLUE,'5,34:1','Texto normal AA'),('Azul / preto',BLUE,INK,'3,75:1','Apenas texto grande'),('Azul claro / preto',FOCUS,INK,'8,09:1','Texto normal AA'),('Muted / branco',MUTED,WHITE,'6,24:1','Texto normal AA')]
            for i,(name,fg2,bg,ratio,status) in enumerate(rows):
                yy=186+i*144;a += [rect(X,yy,160,112,bg,12,LINE if bg==WHITE else None),text('Aa',X+33,yy+24,100,42,fg2,'SemiBold',56),text(name,X+196,yy+6,514,24,INK,'SemiBold',34),text(status,X+196,yy+57,514,19,MUTED,'Regular',30),text(ratio,X+800,yy+24,320,38,INK,'SemiBold',50)]
        elif n==19:
            a.append(panel([text('Aa',56,30,950,244,WHITE,'SemiBold',270,-5),text('ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789  @&?!  á é í ó ú  ç',60,348,1000,40,WHITE,'Regular',66),line(60,586,1060,586,MUTED),label('LIGHT   REGULAR   SEMIBOLD   BOLD',60,630,1020,LINE)],X,188,DW,716,INK))
        elif n==20:
            ramps=[('Display','120 / 128','Direção.',120,128,'SemiBold',190,184),('Título','64 / 72','Clareza para decidir.',64,72,'SemiBold',394,128),('Subtítulo','24 / 32','Precisão para construir.',24,32,'SemiBold',542,96),('Corpo','16 / 24','O conteúdo define a hierarquia.',16,24,'Regular',658,88),('Rótulo','14 / 20','PRÓXIMA DECISÃO',14,20,'SemiBold',766,88)]
            for name,metric,value,sz,lh,st,yy,rh in ramps:
                a += [label(name.upper(),X,yy+10,240),text(metric,X,yy+48,240,18,MUTED,'Regular',28),text(value,X+264,yy+6,DW-264,sz,INK,st,lh,-1.5 if sz>24 else 0),line(X,yy+rh,1816,yy+rh)]
        elif n==21:
            a.append(rect(X,188,DW,632,PAPER,24));gx=X+60;gy=258;gw=1000;scale=gw/1920
            a.append(rect(gx,gy,gw,gw*1080/1920,WHITE,0,LINE))
            for i in range(12):
                xx=gx+(104+i*(120.6666667+24))*scale;a.append(rect(xx,gy+104*scale,120.6666667*scale,(1080-208)*scale,'#EAF1FF',0))
            a += [text('12 colunas',X+60,190,570,32,INK,'SemiBold',42),text('Prancha: 1920 × 1080\nMargem: 104 u  ·  Gutter: 24 u\nColuna: 120,667 u',X+60,840,1030,22,MUTED,'Regular',32)]
        elif n==22:
            a += [panel([svg('trajectory',-228,-70,1260,756,color=FOCUS),text('Conectar\né criar direção.',44,44,700,68,WHITE,'SemiBold',78,-1),label('UM GESTO DOMINANTE POR COMPOSIÇÃO',44,593,1000,LINE)],X,188,DW,716,DARK)]
        elif n==23:
            for i,(icon,title) in enumerate([('observe','Observar'),('direction','Orientar'),('build','Construir'),('learn','Aprender'),('arrow-right','Avançar'),('check','Confirmar'),('close','Fechar'),('focus','Focar')]):
                xx=X+(i%4)*288;yy=188+(i//4)*258
                a.append(panel([svg(f'assets/icons/ui/{icon}.svg',80,44,96,96),text(title,24,166,208,20,INK,'Regular',30)],xx,yy,256,226,PAPER))
            a += [text('24 u / traço 1,75 u / terminais redondos',X,748,DW,26,INK,'SemiBold',40),text('Símbolos funcionais mantêm uma linguagem própria.\nO ícone A· identifica a marca; o conjunto acima orienta ações.',X,812,DW,22,MUTED,'Regular',34)]
        elif n==24:
            for i,(cap,ms) in enumerate([('ESTRUTURA','0 ms'),('PERCURSO','200 ms'),('FOCO','600 ms')]):
                mark=svg('reverse',18,124,316,190)
                if i==0:mark.update(asset='assets/graphics/monogram-solid.svg',color=WHITE)
                if i==1:mark['hidePoint']=True
                a.append(panel([label(cap,24,26,304,LINE),mark,text(ms,24,482,300,28,WHITE,'SemiBold',40)],X+i*384,188,352,580,DARK))
            a += [text('Uma entrada. Sem loop. Marca estável ao final.',X,808,DW,26,WHITE,'SemiBold',38),text('Redução de movimento: assinatura completa desde o primeiro estado.',X,865,DW,21,LINE,'Regular',32)]
        elif n==25:
            for i,(cap,title,body) in enumerate([('EVITAR','“Revolucionamos tudo.”','Abstração e promessa sem escopo.'),('PREFERIR','“Definimos o problema.”','Indica uma ação verificável.'),('EVITAR','“IA resolve qualquer desafio.”','Atribui infalibilidade ao meio.'),('PREFERIR','“IA amplia a exploração.”','Nomeia a capacidade e exige revisão.')]):
                add_tile(a,X+(i%2)*576,188+(i//2)*354,544,324,cap,title,body,None,WHITE if i%2==0 else PAPER)
        elif n==26:
            parts=[label('OBJETIVO DA INVESTIGAÇÃO',40,30,1020),text('Qual pergunta precisa de clareza?',40,78,1020,36,INK,'SemiBold',46),rect(40,166,1040,72,WHITE,8,MUTED,1.5),text('Compreender a dificuldade principal da jornada',62,185,980,22,INK,'Regular',32),text('Descreva o problema observado antes de escolher a solução.',40,260,1020,18,MUTED,'Regular',28),rect(40,344,376,66,BLUE,8),text('Iniciar descoberta',68,364,320,20,WHITE,'SemiBold',28),rect(444,344,326,66,WHITE,8,MUTED),text('Revisar contexto',472,364,282,20,INK,'SemiBold',28),line(40,458,1080,458,LINE)]
            for i,state in enumerate(('Default','Hover','Focus','Disabled')):
                parts.extend([label(state.upper(),40+i*276,482,220),button('Continuar',40+i*276,526,state)])
            parts.append(text('Componentes nativos na página 03 do Figma.\nHTML funcional de referência em examples/ui-kit.html.',40,618,1020,20,MUTED,'Regular',30))
            a.append(panel(parts,X,188,DW,716,PAPER))
        elif n==27:
            a.append(panel([rect(0,0,1120,62,PAPER,24),circle(28,30,5,MUTED),circle(48,30,5,LINE),circle(68,30,5,LINE),text('alexandrebelo.com.br',126,18,650,16,MUTED,'Regular',24),svg('primary',40,88,120,72),text('Projetos     Método     Sobre',672,112,410,17,INK,'Regular',26),line(40,182,1080,182),label('ESTRATÉGIA / DESIGN / IA',44,226,960,BLUE),text('Clareza para decidir.\nPrecisão para construir.',40,285,970,62,INK,'SemiBold',76,-1.5),text('Investigar, dar direção e transformar entendimento\nem experiências que possam evoluir.',44,483,940,24,MUTED,'Regular',38),rect(44,608,258,58,BLUE,8),text('Conhecer o trabalho',64,625,224,17,WHITE,'SemiBold',26)],X,188,DW,716,WHITE,24))
        elif n==28:
            a.append(panel([svg('reverse',38,26,170,102),label('CADERNO DE DECISÕES',286,52,740,LINE),text('Da pergunta\nà experiência.',46,184,976,84,WHITE,'SemiBold',96,-2),line(48,444,1072,444,MUTED),text('01 / Contexto observado\n02 / Hipótese e critério\n03 / Decisão de projeto\n04 / Resultado verificado',52,491,985,26,LINE,'Regular',45)],X,188,DW,716,INK))
        elif n==29:
            a.append(panel([svg('reverse',30,24,160,96),text('Uma boa decisão\ncomeça com uma\nboa pergunta.',34,175,468,48,WHITE,'SemiBold',60,-1),circle(468,470,24,FOCUS),label('AB / INTELIGÊNCIA EM TRAJETÓRIA',34,503,470,LINE)],X,188,544,544,INK,0))
            a.append(panel([svg('micro',108,48,264,264),text('A· / avatar',34,353,412,28,INK,'SemiBold',40),text('A marca completa permanece\nna bio, na capa ou no primeiro\ncontato institucional.',34,410,430,20,MUTED,'Regular',30)],X+576,188,544,544,PAPER))
            a += [text('Quadrado / 1080 × 1080',X,784,550,22,INK,'SemiBold',34),text('Área crítica livre de bordas e recortes do canal.\nFrase única, autoria legível e um ponto de foco.',X,839,DW,22,MUTED,'Regular',34)]
        elif n==30:
            a.append(panel([svg('reverse',38,30,360,216),text('Alexandre Belo',42,338,520,32,WHITE,'SemiBold',42),text('ED&IA\nalexandrebelo.com.br',504,346,326,20,LINE,'Regular',32)],X+128,178,864,480,INK,0))
            a += [svg('primary',X+14,684,190,114),text('Alexandre Belo',X+250,682,840,32,INK,'SemiBold',44),text('ED&IA\nalexandrebelo.com.br',X+252,742,810,22,MUTED,'Regular',34),line(X+222,684,X+222,826,BLUE,2),label('CARTÃO / ASSINATURA DE COMUNICAÇÃO',X,882,DW)]
        elif n==31:
            rows=[('assets/logo/','Assinaturas e matrizes ópticas'),('assets/icons/','Micro A·, favicon e ícones de UI'),('tokens/','Paleta, dimensões, tipo e CSS'),('brandbook/','PDF, HTML, texto e pranchas SVG'),('scripts/','Derivação e verificação de integridade'),('archive/2025/','Originais históricos preservados')]
            for i,(folder,role) in enumerate(rows):
                yy=190+i*116;a += [text(folder,X,yy,1090,30,INK,'SemiBold',42),text(role,X,yy+49,1090,21,MUTED,'Regular',32),line(X,yy+96,1816,yy+96)]
        elif n==32:
            a += [text('Referências consultadas',X,186,DW,36,INK,'SemiBold',48),svg('primary',X+844,158,264,158)]
            bibliography=[('01 / Identidade AB e base editorial','https://www.figma.com/design/3N86ok3o9IExvWUgxWi33h'),('02 / WOOW - referência visual fornecida','https://www.awwwards.com/inspiration/ui-kit-woow'),('03 / Método de refinamento SVG','https://github.com/neonwatty/logo-designer-skill'),('04 / Sora - SIL Open Font License 1.1','https://github.com/google/fonts/tree/main/ofl/sora'),('05 / Contraste - W3C WCAG 2.2, SC 1.4.3','https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html'),('06 / Arquivos e distribuição da identidade','https://github.com/oalexandrebelo/logosvg')]
            for i,(title,url) in enumerate(bibliography):
                yy=322+i*94;a += [text(title,X,yy,DW,22,INK,'SemiBold',32),text(url,X,yy+38,DW,17,MUTED,'Regular',26)]
    # Human-readable source citations on the pages where evidence is used.
    sources={7:'Fonte visual: Figma AB, nodes 1:2591 e 1:11711. Comparação normalizada por altura visível.',9:'Medidas do SVG refinado. Os eixos documentam relações reais; não representam uma grade geradora histórica.',18:'Fonte: W3C, WCAG 2.2, SC 1.4.3. Razões calculadas em sRGB; o teste usa valores não arredondados.',32:'Referências e créditos completos: brandbook.md, seção 32. Método: neonwatty/logo-designer-skill; referência editorial: Figma UI Magic.'}
    for p in SCENES:
        if p['number'] in sources:
            for i,node in enumerate(p['nodes']):
                if node['type']=='text' and node['x']==104 and node['y']==972:
                    p['nodes'][i]=text(sources[p['number']],104,972,1550,16,MUTED,'Regular',24)
                    break

def svg_node(n,prefix='n'):
    x,y=n['x'],n['y'];typ=n['type'];e=html.escape
    if typ=='text':
        spans=''.join(f'<tspan x="{x}" y="{y+.84*n["size"]+(n["line"]-n["size"])/2+i*n["line"]}">{e(t)}</tspan>' for i,t in enumerate(n['text'].split('\n')))
        weight={'Light':300,'Regular':400,'SemiBold':600,'Bold':700}[n['style']]
        return f'<text font-family="Sora" font-size="{n["size"]}" font-weight="{weight}" letter-spacing="{n["tracking"]}" fill="{n["fill"]}" fill-opacity="{n.get("opacity",1)}">{spans}</text>'
    if typ=='rect': return f'<rect x="{x}" y="{y}" width="{n["w"]}" height="{n["h"]}" rx="{n["radius"]}" fill="{n["fill"]}"'+(f' stroke="{n["stroke"]}" stroke-width="{n["sw"]}"' if n.get('stroke') else '')+'/>'
    if typ=='circle': return f'<circle cx="{x+n["w"]/2}" cy="{y+n["h"]/2}" r="{n["w"]/2}" fill="{n["fill"]}"/>'
    if typ=='line':return f'<path d="M{x} {y}l{n["w"]} {n["h"]}" fill="none" stroke="{n["fill"]}" stroke-width="{n["sw"]}"'+(f' stroke-dasharray="{" ".join(map(str,n["dash"]))}"' if n.get('dash') else '')+'/>'
    if typ=='group':
        bg=svg_node(rect(0,0,n['w'],n['h'],n['fill'],n.get('radius',0)),prefix) if n.get('fill') else ''
        content=''.join(svg_node(c,prefix+'-'+str(i)) for i,c in enumerate(n['children']))
        if n.get('clip'):
            content=f'<defs><clipPath id="{prefix}-clip"><rect width="{n["w"]}" height="{n["h"]}" rx="{n.get("radius",0)}"/></clipPath></defs><g clip-path="url(#{prefix}-clip)">{content}</g>'
        return f'<g transform="translate({x} {y})">'+bg+content+'</g>'
    if typ=='svg':
        root=asset_svg(n);ids={el.get('id'):prefix+'-'+el.get('id') for el in root.iter() if el.get('id')}
        for el in list(root.iter()):
            if n.get('hideOrbit') and el.get('id')=='orbita':root.remove(el);continue
            if n.get('hidePoint') and el.get('id')=='ponto-orbital':el.set('visibility','hidden')
            for key,value in list(el.attrib.items()):
                if key=='id':el.set(key,ids[value])
                elif key=='aria-labelledby':el.set(key,' '.join(ids.get(v,v) for v in value.split()))
                else:
                    for before,after in ids.items():value=value.replace('url(#'+before+')','url(#'+after+')')
                    el.set(key,value)
        root.set('x',str(x));root.set('y',str(y));root.set('width',str(n['w']));root.set('height',str(n['h']));root.set('opacity',str(n.get('opacity',1)))
        code=ET.tostring(root,encoding='unicode')
        if n.get('rotation'):code=f'<g transform="rotate({n["rotation"]} {x+n["w"]/2} {y+n["h"]/2})">{code}</g>'
        return code
    raise ValueError(typ)

def color(c):return tuple(int(c[i:i+2],16)/255 for i in (1,3,5))
def pdf_svg(c,node):
    root=asset_svg(node)
    c.saveState();c.translate(node['x'],node['y'])
    clip=c.beginPath();clip.rect(0,0,node['w'],node['h']);c.clipPath(clip,stroke=0,fill=0)
    vb=list(map(float,root.get('viewBox','0 0 100 100').split()));sx=node['w']/vb[2];sy=node['h']/vb[3]
    if not node.get('stretch'):sx=sy=min(sx,sy)
    c.translate((node['w']-vb[2]*sx)/2,(node['h']-vb[3]*sy)/2);c.scale(sx,sy);c.translate(-vb[0],-vb[1])
    def draw(el,inherit):
        tag=el.tag.split('}')[-1]
        if tag in ('title','desc','defs','style','metadata'):return
        if node.get('hideOrbit') and el.get('id')=='orbita':return
        if node.get('hidePoint') and el.get('id')=='ponto-orbital':return
        attrs={**inherit,**el.attrib};c.saveState()
        for name,args in re.findall(r'(matrix|translate|scale|rotate)\(([^)]*)\)',el.get('transform','')):
            vals=[float(v) for v in re.split(r'[,\s]+',args.strip())]
            if name=='matrix':c.transform(*vals)
            if name=='translate':c.translate(vals[0],vals[1] if len(vals)>1 else 0)
            if name=='scale':c.scale(vals[0],vals[1] if len(vals)>1 else vals[0])
            if name=='rotate':
                if len(vals)>2:c.translate(vals[1],vals[2]);c.rotate(vals[0]);c.translate(-vals[1],-vals[2])
                else:c.rotate(vals[0])
        fill=attrs.get('fill','#000000');stroke=attrs.get('stroke','none')
        if fill!='none':c.setFillColorRGB(*color(fill));c.setFillAlpha(float(attrs.get('fill-opacity',1))*node.get('opacity',1))
        if stroke!='none':c.setStrokeColorRGB(*color(stroke));c.setLineWidth(float(attrs.get('stroke-width',1)));c.setLineCap(1 if attrs.get('stroke-linecap')=='round' else 0);c.setLineJoin(1 if attrs.get('stroke-linejoin')=='round' else 0)
        if tag=='path':
            pen=PDFPathPen(c);parse_path(el.get('d',''),pen);c.drawPath(pen.path,fill=int(fill!='none'),stroke=int(stroke!='none'),fillMode=0 if attrs.get('fill-rule')=='evenodd' else 1)
        if tag=='circle':c.circle(float(el.get('cx',0)),float(el.get('cy',0)),float(el.get('r',0)),stroke=int(stroke!='none'),fill=int(fill!='none'))
        if tag=='rect':c.roundRect(float(el.get('x',0)),float(el.get('y',0)),float(el.get('width',0)),float(el.get('height',0)),float(el.get('rx',0)),stroke=int(stroke!='none'),fill=int(fill!='none'))
        for child in el:draw(child,attrs)
        c.restoreState()
    if node.get('rotation'):
        cx=vb[0]+vb[2]/2;cy=vb[1]+vb[3]/2;c.translate(cx,cy);c.rotate(node['rotation']);c.translate(-cx,-cy)
    draw(root,{});c.restoreState()

def pdf_node(c,n):
    t=n['type'];x,y=n['x'],n['y'];c.saveState()
    if t=='group':
        c.translate(x,y)
        if n.get('fill'):pdf_node(c,rect(0,0,n['w'],n['h'],n['fill'],n.get('radius',0)))
        if n.get('clip'):
            clip=c.beginPath();clip.rect(0,0,n['w'],n['h']);c.clipPath(clip,stroke=0,fill=0)
        for child in n['children']:pdf_node(c,child)
    elif t=='svg':pdf_svg(c,n)
    elif t=='text':
        c.translate(x,y);c.scale(1,-1);c.setFillColorRGB(*color(n['fill']));c.setFillAlpha(n.get('opacity',1))
        for i,txt in enumerate(n['text'].split('\n')):
            ob=c.beginText(0,-(.84*n['size']+(n['line']-n['size'])/2+i*n['line']));ob.setFont('Sora-'+n['style'],n['size']);ob.setCharSpace(n['tracking']);ob.textOut(txt);c.drawText(ob)
    elif t=='line':
        c.setStrokeColorRGB(*color(n['fill']));c.setLineWidth(n['sw']);c.setDash(n.get('dash') or []);c.line(x,y,x+n['w'],y+n['h'])
    else:
        if n['fill']!='none':c.setFillColorRGB(*color(n['fill']))
        stroke=n.get('stroke');sw=n.get('sw',1)
        if stroke:c.setStrokeColorRGB(*color(stroke));c.setLineWidth(sw)
        if t=='rect':c.roundRect(x,y,n['w'],n['h'],n.get('radius',0),stroke=int(bool(stroke)),fill=int(n['fill']!='none'))
        if t=='circle':c.circle(x+n['w']/2,y+n['h']/2,n['w']/2,stroke=0,fill=1)
    c.restoreState()

def export(pdf=True):
    pages=ROOT/'brandbook/pages';pages.mkdir(parents=True,exist_ok=True)
    ET.register_namespace('','http://www.w3.org/2000/svg')
    encoded=base64.b64encode((ROOT/'assets/fonts/Sora-Variable.woff').read_bytes()).decode()
    for p in SCENES:
        title=html.escape(p['name']);style=f'<style>@font-face{{font-family:Sora;src:url(data:font/woff;base64,{encoded}) format("woff");font-weight:100 800}}</style>'
        contents=''.join(svg_node(n,f'p{p["number"]}-{i}') for i,n in enumerate(p['nodes']))
        out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="page-title"><title id="page-title">{title}</title><defs>{style}</defs><rect width="{W}" height="{H}" fill="{p["fill"]}"/>{contents}</svg>'
        (pages/f'{p["number"]:02d}.svg').write_text(out)
    (ROOT/'brandbook/scene.json').write_text(json.dumps({'schema':'ab-brandbook-scene/1','width':W,'height':H,'pages':SCENES},ensure_ascii=False,indent=2)+'\n')
    if pdf:
        c=canvas.Canvas(str(ROOT/'brandbook/AB-Brandbook.pdf'),pagesize=(W,H),pageCompression=1,invariant=1)
        c.setTitle('AB — Inteligência em trajetória | Brandbook 1.0');c.setAuthor('Alexandre Belo');c.setSubject('Sistema de identidade, construção vetorial e aplicações AB')
        for p in SCENES:
            c.bookmarkPage(f'p{p["number"]}');c.addOutlineEntry(p['name'],f'p{p["number"]}',0)
            c.saveState();c.translate(0,H);c.scale(1,-1);c.setFillColorRGB(*color(p['fill']));c.rect(0,0,W,H,stroke=0,fill=1)
            for n in p['nodes']:pdf_node(c,n)
            c.restoreState();c.showPage()
        c.save()
    copies=json.loads((ROOT/'brandbook/copy.json').read_text())
    nav=''.join(f'<a href="#p{p["number"]}">{p["number"]:02d} {html.escape(p["title"])}</a>' for p in SCENES)
    articles=''.join(f'<article id="p{p["number"]}" data-search="{html.escape((p["title"]+" "+cp["body"]).lower(),quote=True)}"><h2>{p["number"]:02d} · {html.escape(p["title"])}</h2><img src="pages/{p["number"]:02d}.svg" width="1920" height="1080" alt="Prancha {p["number"]:02d}: {html.escape(p["title"],quote=True)}" loading="lazy"><details><summary>Ler a orientação em texto</summary><p>{html.escape(cp["body"])}</p><p>{html.escape(cp["notes"])}</p></details></article>' for p,cp in zip(SCENES,copies))
    document='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AB · Inteligência em trajetória</title><link rel="stylesheet" href="../tokens/brand.css"><style>*{box-sizing:border-box}body{margin:0;background:#F4F6FA;color:#070808;font:16px/1.6 Sora,system-ui,sans-serif}header{background:#070808;color:white;padding:40px 5vw}header h1{font-size:clamp(32px,4vw,64px);letter-spacing:-.04em;margin:8px 0}header p{color:#C6CDD9}a{color:inherit;text-underline-offset:4px}.downloads{display:flex;flex-wrap:wrap;gap:16px}.downloads a{padding:10px 18px;border:1px solid #566176;border-radius:8px;text-decoration:none}.downloads a:first-child{background:#065CFB;border-color:#065CFB}.layout{display:grid;grid-template-columns:280px minmax(0,1fr);gap:32px;max-width:1800px;margin:auto;padding:36px}aside{align-self:start;position:sticky;top:24px;max-height:90vh;overflow:auto}label{display:block;font-weight:600}input{font:inherit;width:100%;border:1px solid #566176;border-radius:8px;padding:12px;margin:8px 0 20px;background:white;color:#070808}nav a{display:block;padding:8px 10px;font-size:13px;text-decoration:none;border-left:2px solid transparent}nav a:hover{border-color:#065CFB;background:#EAF1FF}article{scroll-margin-top:24px;margin-bottom:40px}article h2{font-size:20px;font-weight:600}article img{display:block;width:100%;height:auto;background:white;border:1px solid #C6CDD9}details{background:white;padding:18px 24px}summary{cursor:pointer;color:#566176}details p{max-width:80ch}a:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid #065CFB;outline-offset:4px}[hidden]{display:none!important}footer{padding:32px 5vw;border-top:1px solid #C6CDD9}@media(max-width:900px){.layout{display:block;padding:20px}aside{position:static;max-height:none}nav{max-height:230px;overflow:auto;margin-bottom:30px}header{padding:28px 20px}}@media print{header,aside,details,footer,article h2{display:none}.layout{display:block;padding:0}article{margin:0;break-after:page}article img{border:0}@page{size:landscape;margin:0}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style><header><p>AB / ALEXANDRE BELO / 1.0</p><h1>Inteligência em trajetória.</h1><p>Clareza para decidir. Precisão para construir.</p><div class="downloads"><a href="AB-Brandbook.pdf" download>Baixar brandbook PDF</a><a href="../assets/logo/ab-primary.svg" download>Baixar logo SVG</a><a href="https://www.figma.com/design/VTETqqBjYKD3bNACqqwS0A">Abrir Figma editável</a><a href="brandbook.md">Ler o manual completo</a></div></header><div class="layout"><aside><label for="search">Encontrar uma orientação</label><input id="search" type="search" placeholder="Cor, proteção, tipografia…"><nav aria-label="Pranchas do brandbook">NAV</nav></aside><main>ARTICLES<p id="empty" hidden>Nenhuma prancha encontrada. Tente outra palavra.</p></main></div><footer>AB · Sistema de identidade 1.0 · Fonte vetorial e regras mantidas no repositório de marca. <a href="../docs/design-rationale.md">Fundamentação completa</a></footer><script>const search=document.querySelector('#search');const pages=[...document.querySelectorAll('article')];search.addEventListener('input',()=>{const q=search.value.trim().toLocaleLowerCase('pt-BR');let count=0;for(const page of pages){const show=!q||page.dataset.search.includes(q);page.hidden=!show;if(show)count++;}document.querySelector('#empty').hidden=count>0;});</script></html>'''
    (ROOT/'brandbook/index.html').write_text(document.replace('NAV',nav).replace('ARTICLES',articles))
    print(f'Built {len(SCENES)} sheets; PDF={pdf}; shared editable scene saved.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--no-pdf',action='store_true');args=parser.parse_args()
    fonts();compose();export(not args.no_pdf)
