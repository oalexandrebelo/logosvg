/* Native Figma scene importer.
 * scripts/prepare_figma_book.py supplies PAYLOAD from the canonical local files.
 * Requires the AB foundations and library described in docs/figma-library.json.
 * Execute through use_figma after loading figma-use and figma-generate-design.
 */
const F = PAYLOAD.library.foundations;
const C = PAYLOAD.library.components;
const created = new Set();
const frames = [];
const textMetrics = [];
const track = node => { created.add(node.id); return node; };
const trackTree = node => {
  track(node);
  if ('children' in node) for (const child of node.children) trackTree(child);
  return node;
};
const page = await figma.getNodeByIdAsync(PAYLOAD.pageId);
if (!page || page.type !== 'PAGE') throw new Error('Target page does not exist.');
await figma.setCurrentPageAsync(page);
for (const p of PAYLOAD.pages) {
  if (page.children.some(n => n.name === p.name)) {
    throw new Error('Existing artboard: '+p.name+'. Inspect before rebuilding.');
  }
}
for (const style of ['Light','Regular','SemiBold','Bold']) {
  await figma.loadFontAsync({family:'Sora',style});
}
const variables = {};
for (const [key,id] of Object.entries(F.variables)) {
  variables[key] = await figma.variables.getVariableByIdAsync(id);
}
const semanticCollection = await figma.variables.getVariableCollectionByIdAsync(F.collections['AB / Color'].id);
const byHex = {};
for (const [name,hex] of Object.entries(PAYLOAD.brand.palette)) {
  byHex[hex.toUpperCase()] = variables['AB / Primitives/'+name];
}
const byDimension = {};
for (const [kind,entries] of Object.entries(PAYLOAD.brand.dimensions)) {
  for (const [name,value] of Object.entries(entries)) {
    byDimension[kind+'/'+value] = variables['AB / Geometry/'+kind+'/'+name];
  }
}
const masters = {};
for (const [key,id] of Object.entries(PAYLOAD.masters)) {
  const m=await figma.getNodeByIdAsync(id);
  if (!m || m.type !== 'COMPONENT') throw new Error('Missing component '+key+' '+id);
  masters[key]=m;
}
const rgb = hex => ({r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255});
function paint(hex,opacity=1) {
  const p={type:'SOLID',color:rgb(hex),opacity};
  const variable=byHex[hex.toUpperCase()];
  return variable ? figma.variables.setBoundVariableForPaint(p,'color',variable) : p;
}
function fill(node,hex) { node.fills=hex && hex!=='none' ? [paint(hex)] : []; }
function bindDimension(node,field,kind,value) {
  const variable=byDimension[kind+'/'+value];
  if (variable) node.setBoundVariable(field,variable);
}
function radius(node,value) {
  node.cornerRadius=value;
  for (const field of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius']) {
    bindDimension(node,field,'radius',value);
  }
}
function place(node,parent,data,flow=false) {
  parent.appendChild(node);
  if (!flow) { node.x=data.x;node.y=data.y; }
  return node;
}
async function makeText(data,parent,flow) {
  const t=track(figma.createText());
  t.name=data.name;
  t.fontName={family:'Sora',style:data.style};
  const style=PAYLOAD.brand.typography.styles.find(s => s.style===data.style && s.size===data.size && s.line===data.line && s.tracking===data.tracking);
  if (style) await t.setTextStyleIdAsync(F.styles[style.name]);
  else {
    t.fontSize=data.size;
    t.lineHeight={unit:'PIXELS',value:data.line};
    t.letterSpacing={unit:'PIXELS',value:data.tracking};
  }
  t.characters=data.text;
  fill(t,data.fill);
  t.opacity=data.opacity ?? 1;
  t.textAutoResize='HEIGHT';
  t.resize(data.w,data.h);
  place(t,parent,data,flow);
  t.layoutSizingHorizontal=flow && parent.layoutMode==='VERTICAL'?'FILL':'FIXED';
  if (flow) t.layoutSizingVertical='HUG';
  textMetrics.push({id:t.id,name:t.name,expectedHeight:data.h,height:t.height,width:t.width});
  return t;
}
async function make(data,parent,flow=false) {
  if (data.type==='text') return await makeText(data,parent,flow);
  if (data.component) {
    const spec=data.component;
    const key='Button/'+spec.Style+'/'+spec.State;
    const node=trackTree(masters[key].createInstance());
    node.name=data.name;
    node.setProperties({[C.propertyKeys.button]:spec.Label});
    place(node,parent,data,flow);
    return node;
  }
  if (data.type==='group') {
    const isFlow=Boolean(data.layout);
    const node=track(isFlow ? figma.createAutoLayout(data.layout) : figma.createFrame());
    node.name=data.name;
    node.resize(data.w,data.h);
    fill(node,data.fill);
    node.clipsContent=Boolean(data.clip);
    radius(node,data.radius || 0);
    if (isFlow) {
      node.itemSpacing=data.gap;
      node.paddingLeft=0;node.paddingRight=0;node.paddingTop=0;node.paddingBottom=0;
      node.primaryAxisAlignItems='MIN';node.counterAxisAlignItems='MIN';
      bindDimension(node,'itemSpacing','space',data.gap);
      for (const field of ['paddingLeft','paddingRight','paddingTop','paddingBottom']) bindDimension(node,field,'space',0);
    }
    place(node,parent,data,flow);
    if (isFlow) {
      node.layoutSizingHorizontal='FIXED';node.layoutSizingVertical='HUG';
    }
    for (const child of data.children) await make(child,node,isFlow);
    return node;
  }
  if (data.type==='svg') {
    if (data.componentKey) {
      const master=masters[data.componentKey];
      const node=trackTree(master.createInstance());
      node.name=data.name;
      parent.appendChild(node);
      const s=Math.min(data.w/master.width,data.h/master.height);
      node.rescale(s);
      node.x=data.x+(data.w-node.width)/2;
      node.y=data.y+(data.h-node.height)/2;
      return node;
    }
    const source=PAYLOAD.svg[data.svgKey].replace(/__AB_PATH_\d+__/g,key=>PAYLOAD.svgPaths[key]);
    const node=trackTree(figma.createNodeFromSvg(source));
    node.name=data.name;
    node.clipsContent=true;
    node.resize(data.w,data.h);
    for (const child of [node,...node.findAll()]) {
      for (const property of ['fills','strokes']) {
        if (!(property in child) || !Array.isArray(child[property])) continue;
        child[property]=child[property].map(p => {
          if (p.type!=='SOLID') return p;
          const hex='#'+[p.color.r,p.color.g,p.color.b].map(v=>Math.round(v*255).toString(16).padStart(2,'0')).join('').toUpperCase();
          return byHex[hex] ? figma.variables.setBoundVariableForPaint(p,'color',byHex[hex]) : p;
        });
      }
    }
    if (data.rotation) {
      const wrapper=track(figma.createFrame());
      wrapper.name=data.name+' / rotação demonstrativa';
      wrapper.resize(data.w,data.h);wrapper.fills=[];wrapper.clipsContent=true;
      place(wrapper,parent,data,flow);wrapper.appendChild(node);
      const a=data.rotation*Math.PI/180,c=Math.cos(a),s=Math.sin(a),cx=data.w/2,cy=data.h/2;
      node.relativeTransform=[[c,-s,cx-c*cx+s*cy],[s,c,cy-s*cx-c*cy]];
      return wrapper;
    }
    place(node,parent,data,flow);
    return node;
  }
  if (data.type==='line') {
    const node=track(figma.createLine());node.name=data.name;
    const len=Math.hypot(data.w,data.h);
    if (!len) throw new Error('Zero length line');
    node.resize(len,0);node.strokes=[paint(data.fill)];node.strokeWeight=data.sw;
    node.dashPattern=data.dash || [];
    parent.appendChild(node);
    node.relativeTransform=[[data.w/len,-data.h/len,data.x],[data.h/len,data.w/len,data.y]];
    return node;
  }
  const node=track(data.type==='circle' ? figma.createEllipse() : figma.createRectangle());
  node.name=data.name;node.resize(data.w,data.h);fill(node,data.fill);
  if (data.type==='rect') radius(node,data.radius || 0);
  if (data.stroke) {node.strokes=[paint(data.stroke)];node.strokeWeight=data.sw;node.strokeAlign='CENTER';}
  else node.strokes=[];
  place(node,parent,data,flow);
  return node;
}
for (const data of PAYLOAD.pages) {
  const frame=track(figma.createFrame());
  frame.name=data.name;frame.resize(data.w,data.h);fill(frame,data.fill);
  frame.clipsContent=true;
  frame.placeholder=true;
  page.appendChild(frame);
  frame.x=data.canvasX;frame.y=data.canvasY;
  frame.setExplicitVariableModeForCollection(semanticCollection,F.collections['AB / Color'].modes[data.fill==='#070808'?'Dark':'Light']);
  for (const n of data.nodes) await make(n,frame);
  frame.placeholder=false;
  const all=frame.findAll();
  const types={};for (const n of all) types[n.type]=(types[n.type]||0)+1;
  const images=all.filter(n=>'fills' in n && Array.isArray(n.fills) && n.fills.some(p=>p.type==='IMAGE')).map(n=>n.id);
  frames.push({number:data.number,id:frame.id,name:frame.name,width:frame.width,height:frame.height,x:frame.x,y:frame.y,descendants:all.length,types,imageNodes:images});
}
const mismatches=textMetrics.filter(t=>Math.abs(t.height-t.expectedHeight)>1.1 || t.width<1);
return {createdNodeIds:[...created],mutatedNodeIds:[page.id],pageId:page.id,frames,textNodeCount:textMetrics.length,textHeightMismatches:mismatches,componentInstanceCount:frames.reduce((s,f)=>s+(f.types.INSTANCE||0),0),zeroRaster:frames.every(f=>!f.imageNodes.length)};
