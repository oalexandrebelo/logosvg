// AB signature library template.
// Run scripts/prepare_figma_library.py to inject CONFIG, FOUNDATION, BRAND, SOURCES and SOURCE_PATHS.
// Execute the generated build/figma-signatures.js through use_figma after loading its skills.
// Source SVG paths are reconstructed losslessly before native import.

const page=await figma.getNodeByIdAsync(CONFIG.pageId);
if(!page||page.type!=='PAGE')throw new Error('Página 02 — Assinaturas ausente.');
await figma.setCurrentPageAsync(page);
if(page.children.length)throw new Error('Página contém nós. Retomar pelos IDs antes de repetir para evitar duplicações.');
const [variables,styles]=await Promise.all([
 Promise.all(Object.values(FOUNDATION.variables).map(id=>figma.variables.getVariableByIdAsync(id))),
 Promise.all(Object.values(FOUNDATION.styles).map(id=>figma.getStyleByIdAsync(id)))
]);
if(variables.some(v=>!v)||styles.some(s=>!s))throw new Error('Foundations incompletas.');
const variableById=Object.fromEntries(variables.map(v=>[v.id,v]));
const V=Object.fromEntries(Object.entries(FOUNDATION.variables).map(([name,id])=>[name,variableById[id]]));
const ST=Object.fromEntries(styles.map(s=>[s.name,s]));
const fonts=[...new Map(styles.map(s=>[JSON.stringify(s.fontName),s.fontName])).values()];
await Promise.all(fonts.map(f=>figma.loadFontAsync(f)));
await figma.loadFontAsync({family:'Inter',style:'Regular'});
const created=new Set();
function track(n){created.add(n.id);return n;}
function subtree(n){return [n,...('children'in n?n.query('*').toArray():[])];}
function trackTree(n){for(const x of subtree(n))created.add(x.id);return n;}
function hex(c){return '#'+[c.r,c.g,c.b].map(x=>Math.round(x*255).toString(16).padStart(2,'0')).join('').toUpperCase();}
const primitiveByHex={};
for(const [key,v] of Object.entries(V)){
 if(key.startsWith('AB / Primitives/')){
  const val=Object.values(v.valuesByMode)[0];
  if(val&&typeof val==='object'&&'r'in val)primitiveByHex[hex(val)]=v;
 }
}
function paint(name){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',V['AB / Primitives/'+name]);}
function bind(n,prop,key){n.setBoundVariable(prop,V['AB / Geometry/'+key]);}
function pad(n,value){for(const key of ['paddingTop','paddingRight','paddingBottom','paddingLeft'])bind(n,key,'space/'+value);}
function auto(parent,name,direction,width=null,gap='4',padding='0'){
 const n=track(figma.createAutoLayout(direction));n.name=name;n.fills=[];n.clipsContent=false;parent.appendChild(n);
 pad(n,padding);bind(n,'itemSpacing','space/'+gap);
 if(width!==null){n.resize(width,1);n.layoutSizingHorizontal='FIXED';n.layoutSizingVertical='HUG';}
 else{n.layoutSizingHorizontal='HUG';n.layoutSizingVertical='HUG';}
 return n;
}
async function text(parent,name,chars,style='AB / Body',color='ink',width=null){
 const t=track(figma.createText());t.name=name;t.fontName=ST[style].fontName;
 await t.setTextStyleIdAsync(FOUNDATION.styles[style]);t.characters=chars;t.fills=[paint(color)];parent.appendChild(t);
 if(width!==null){t.textAutoResize='HEIGHT';t.resize(width,Math.max(1,t.height));t.layoutSizingHorizontal='FIXED';t.layoutSizingVertical='HUG';}
 else{t.textAutoResize='WIDTH_AND_HEIGHT';t.layoutSizingHorizontal='HUG';t.layoutSizingVertical='HUG';}
 return t;
}
function geometry(node){return JSON.stringify(subtree(node).map(n=>({id:n.id,width:n.width,height:n.height,relativeTransform:n.relativeTransform,paths:n.type==='VECTOR'?n.vectorPaths:undefined})));}
const masters={},map={},bindings=[];
for(let i=0;i<SOURCES.length;i++){
 const s=SOURCES[i];
 const c=track(figma.createComponent());c.name=s.name;
 c.description=s.usage+'\nFonte canônica: '+s.path+'\nViewBox: '+s.viewBox+'. Proporção original preservada; redimensionar proporcionalmente com Scale.\nCores vinculadas a AB / Primitives por HEX. SVG nativo editável, sem raster, sem dependência de fonte.\nSHA-256 da fonte: '+s.sha256;
 c.fills=[];c.clipsContent=false;c.resize(s.width,s.height);c.layoutMode='HORIZONTAL';c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';pad(c,'0');bind(c,'itemSpacing','space/0');bind(c,'cornerRadius','radius/none');
 page.appendChild(c);c.x=CONFIG.layout.masterX+(i%4)*1660;c.y=CONFIG.layout.masterY+Math.floor(i/4)*800;
 const original=s.svg.replace(/ d="@(\d+)@"/g,(_,i)=>' d="'+SOURCE_PATHS[Number(i)]+'"');
 const svg=original.replace('<svg ','<svg width="'+s.width+'" height="'+s.height+'" ');
 const a=trackTree(figma.createNodeFromSvg(svg));a.name='SVG / '+s.path.split('/').pop();
 if(Math.abs(a.width-s.width)>0.01||Math.abs(a.height-s.height)>0.01)throw new Error('Dimensão divergente no SVG '+s.path+': '+a.width+'×'+a.height);
 c.appendChild(a);a.x=0;a.y=0;a.clipsContent=false;a.fills=[];a.strokes=[];
 const before=geometry(a);let count=0;
 const used={};
 for(const n of subtree(a)){
  for(const field of ['fills','strokes']){
   if(field in n&&Array.isArray(n[field]))n[field]=n[field].map(p=>{
    if(p.type==='IMAGE')throw new Error('Raster inesperado: '+s.path);
    if(p.type!=='SOLID')return p;
    const color=hex(p.color),v=primitiveByHex[color];
    if(!v)throw new Error('Cor sem primitiva: '+color+' em '+s.path);
    count++;used[color]=v.id;
    return figma.variables.setBoundVariableForPaint(p,'color',v);
   });
  }
 }
 if(before!==geometry(a))throw new Error('Vínculo alterou geometria: '+s.path);
 if(subtree(a).some(n=>n.type==='TEXT'))throw new Error('SVG com dependência tipográfica: '+s.path);
 masters[s.path]=c;
 const typeCounts={};for(const n of subtree(a))typeCounts[n.type]=(typeCounts[n.type]||0)+1;
 map[s.path]={componentId:c.id,svgNodeId:a.id,width:c.width,height:c.height,viewBox:s.viewBox,name:c.name,usage:s.usage,sourceSha256:s.sha256,background:s.background,solidPaintBindings:count,primitiveBindings:used,nativeTypes:typeCounts,transparentComponent:c.fills.length===0,geometryPreserved:true};
 bindings.push({componentId:c.id,paints:count,colors:used});
}

const board=auto(page,'Assinaturas / revisão vetorial','VERTICAL',2056,'8','12');board.x=CONFIG.layout.reviewX;board.y=CONFIG.layout.reviewY;board.fills=[paint('white')];
const head=auto(board,'Introdução','VERTICAL',1960,'3');
await text(head,'Eyebrow','AB  /  SISTEMA DE ASSINATURAS','AB / Eyebrow','blue');
await text(head,'Title','Uma identidade.\nEscalas diferentes.','AB / Title','ink',1960);
await text(head,'Subtitle','14 assinaturas e 2 grafismos vetoriais. Componentes vinculados às cores da marca, com proporções e transparências preservadas.','AB / Body','muted',1580);
const grid=auto(board,'Catálogo / instâncias','VERTICAL',1960,'6');
const instanceMap={};const previewChecks=[];
for(let rowIndex=0;rowIndex<4;rowIndex++){
 const row=auto(grid,'Linha '+(rowIndex+1),'HORIZONTAL',1960,'6');
 for(const s of SOURCES.slice(rowIndex*4,rowIndex*4+4)){
  const card=auto(row,s.title,'VERTICAL',472,'3','4');card.fills=[paint('white')];card.strokes=[paint('line')];card.strokeWeight=1;card.strokeAlign='INSIDE';bind(card,'cornerRadius','radius/control');
  const preview=auto(card,'Aplicação / fundo '+s.background,'HORIZONTAL',440,'0');preview.resize(440,224);preview.layoutSizingHorizontal='FIXED';preview.layoutSizingVertical='FIXED';preview.primaryAxisSizingMode='FIXED';preview.counterAxisSizingMode='FIXED';preview.primaryAxisAlignItems='CENTER';preview.counterAxisAlignItems='CENTER';preview.fills=[paint(s.background)];bind(preview,'cornerRadius','radius/control');preview.clipsContent=false;
  const inst=trackTree(masters[s.path].createInstance());inst.name=s.title+' / amostra';preview.appendChild(inst);
  const scale=s.displayWidth?s.displayWidth/s.width:Math.min(416/s.width,200/s.height);
  inst.rescale(scale);instanceMap[s.path]=inst.id;
  const labelBlock=auto(card,'Identificação','VERTICAL',440,'1');
  await text(labelBlock,'Nome da versão',s.title,'AB / Subheading','ink',440);
  await text(labelBlock,'Uso e função',s.usage,'AB / Body','muted',440);
  const fileLabel=await text(labelBlock,'Arquivo canônico',s.path.split('/').pop(),'AB / Caption','blue',440);
  await text(labelBlock,'Fundo recomendado','Fundo: '+({paper:'claro',ink:'escuro',blue:'azul'}[s.background]),'AB / Label','muted',440);
  previewChecks.push({path:s.path,instanceId:inst.id,width:inst.width,height:inst.height,aspectError:Math.abs(inst.width/inst.height-s.width/s.height),fits:inst.width<=preview.width+0.01&&inst.height<=preview.height+0.01});
 }
 const height=Math.max(...row.children.map(c=>c.height));
 for(const c of row.children){c.resize(472,height);c.layoutSizingHorizontal='FIXED';c.layoutSizingVertical='FIXED';}
}
const footer=auto(board,'Regra de uso','HORIZONTAL',1960,'8','6');footer.fills=[paint('blue-soft')];bind(footer,'cornerRadius','radius/control');
await text(footer,'Microssímbolo','A·  /  ASSINATURA CONTEXTUAL','AB / Eyebrow','blue',420);
await text(footer,'Regra de identificação','O A· mantém a inicial de autoria e o ponto de foco. Use de 16 a 63 px quando a marca já estiver identificada. Na primeira apresentação, use AB ou a assinatura Alexandre Belo.','AB / Body','ink',1460);

const nodes=page.query('*').toArray();for(const n of nodes)created.add(n.id);
const types={},fontProof={},rasterNodes=[],wrongFonts=[],outside=[];
for(const n of nodes){
 types[n.type]=(types[n.type]||0)+1;
 if(n.type==='TEXT'){
  for(const seg of n.getStyledTextSegments(['fontName'])){
   const key=seg.fontName.family+' / '+seg.fontName.style;fontProof[key]=(fontProof[key]||0)+1;
   if(seg.fontName.family!==BRAND.typography.family)wrongFonts.push(n.id);
  }
 }
 for(const k of ['fills','strokes'])if(k in n&&Array.isArray(n[k])&&n[k].some(p=>p.type==='IMAGE'))rasterNodes.push(n.id);
}
for(const child of board.children){if(child.x<-.01||child.y<-.01||child.x+child.width>board.width+.01||child.y+child.height>board.height+.01)outside.push(child.id);}
const invalid=previewChecks.filter(x=>!x.fits||x.aspectError>.00001);
return {fileKey:CONFIG.fileKey,pageId:page.id,reviewFrameId:board.id,reviewWidth:board.width,reviewHeight:board.height,createdNodeIds:[...created],mutatedNodeIds:[],signatures:map,reviewInstances:instanceMap,counts:{masters:Object.keys(masters).length,nodes:nodes.length,types},fontProof,zeroRasters:rasterNodes.length===0,rasterNodes,wrongFonts,previewValidation:{checked:previewChecks.length,invalid},boardOverflowNodes:outside,validationPassed:wrongFonts.length===0&&rasterNodes.length===0&&invalid.length===0&&outside.length===0,canonicalRoot:'.'};
