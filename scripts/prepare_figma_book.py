#!/usr/bin/env python3
"""Prepare a native Figma import batch from scene.json and the recorded library.

Usage: python scripts/prepare_figma_book.py --pages 1:4
The generated JavaScript goes to build/ and is executed by the Figma connector.
It creates native text, shapes and linked instances. It makes no network calls.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
MODIFIERS=('viewBox','color','rotation','hideOrbit','hidePoint','stretch')

def modified_svg(node):
    root=ET.parse(ROOT/node['asset']).getroot()
    if node.get('viewBox'):root.set('viewBox',node['viewBox'])
    if node.get('stretch'):root.set('preserveAspectRatio','none')
    root.set('width',str(node['w']));root.set('height',str(node['h']))
    for parent in list(root.iter()):
        for child in list(parent):
            if (node.get('hideOrbit') and child.get('id')=='orbita') or (node.get('hidePoint') and child.get('id')=='ponto-orbital'):
                parent.remove(child)
    for child in root.iter():
        if node.get('color'):
            for attr in ('fill','stroke'):
                if child.get(attr) not in (None,'none'):child.set(attr,node['color'])
    ET.register_namespace('','http://www.w3.org/2000/svg')
    return ET.tostring(root,encoding='unicode')

def prepare(scene,library,first,last,page_id=None,columns=4):
    brand=json.loads((ROOT/'tokens/brand.json').read_text())
    pages=[copy.deepcopy(p) for p in scene['pages'] if first<=p['number']<=last]
    if not pages:raise ValueError('No pages in requested range')
    all_masters={path:entry['componentId'] for path,entry in library['signatures'].items()}
    c=library['components']['components']
    all_masters.update({f'assets/icons/ui/{name}.svg':cid for name,cid in c['Icons'].items()})
    for variant in c['Button']['variants']:
        properties=dict(part.split('=') for part in variant['name'].split(', '))
        all_masters['Button/'+properties['Style']+'/'+properties['State']]=variant['id']
    used={};svgs={}
    def visit(n):
        if n.get('component'):
            key='Button/'+n['component']['Style']+'/'+n['component']['State'];used[key]=all_masters[key]
        elif n['type']=='svg':
            if n['asset'] in all_masters and not any(n.get(k) for k in MODIFIERS):
                n['componentKey']=n['asset'];used[n['asset']]=all_masters[n['asset']]
            else:
                value=modified_svg(n);key=hashlib.sha256(value.encode()).hexdigest()[:16]
                svgs[key]=value;n['svgKey']=key
        for child in n.get('children',[]):visit(child)
    for p in pages:
        p['canvasX']=200+((p['number']-1)%columns)*2080
        p['canvasY']=200+((p['number']-1)//columns)*1240
        for n in p['nodes']:visit(n)
    paths={};encoded={}
    for key,value in svgs.items():
        def token(match):
            path=match.group(1)
            if len(path)<80:return match.group(0)
            if path not in paths:paths[path]=f'__AB_PATH_{len(paths)}__'
            return 'd="'+paths[path]+'"'
        encoded[key]=re.sub(r'd="([^"]+)"',token,value)
    dictionary={token:path for path,token in paths.items()}
    for key,code in encoded.items():
        restored=re.sub(r'__AB_PATH_\d+__',lambda m:dictionary[m.group()],code)
        if restored!=svgs[key]:raise ValueError('Lossless path encoding failed')
    return {'pageId':page_id or library['foundations']['pages']['01 — Brandbook'],'library':library,'brand':brand,'masters':used,'svg':encoded,'svgPaths':dictionary,'pages':pages}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pages',default='1:4',help='Inclusive first:last range')
    parser.add_argument('--scene',type=Path,default=ROOT/'brandbook/scene.json')
    parser.add_argument('--library',type=Path,default=ROOT/'docs/figma-library.json')
    parser.add_argument('--page-id',default=None)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    first,last=map(int,args.pages.split(':'))
    if first<1 or last<first:parser.error('Invalid page range')
    payload=prepare(json.loads(args.scene.read_text()),json.loads(args.library.read_text()),first,last,args.page_id)
    # Keep only the used metadata; component geometry lives in Figma masters.
    payload['library']={'foundations':payload['library']['foundations'],'components':{'propertyKeys':payload['library']['components']['propertyKeys']}}
    out=(args.output or ROOT/'build'/f'figma-book-{first:02d}-{last:02d}.js').resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    code='const PAYLOAD='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n'+(ROOT/'scripts/figma_book.js').read_text()
    if len(code)>50000:raise ValueError(f'Batch exceeds the connector limit ({len(code)} characters). Use fewer pages.')
    out.write_text(code)
    print(json.dumps({'file':str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),'pages':len(payload['pages']),'characters':len(code),'bytes':out.stat().st_size,'linkedMasters':len(payload['masters']),'embeddedSvgVariants':len(payload['svg'])}))

if __name__=='__main__':main()
