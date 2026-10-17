// AB component library template.
// Run scripts/prepare_figma_library.py to inject CONFIG, FOUNDATION, BRAND and ICON_SOURCE.
// Execute the generated build/figma-components.js through use_figma after loading its skills.
// This is a Figma async-function body, not a browser script or Node entry point.

// Original project helper. Uses only the public Figma Plugin API.
function makeVariantFamily(spec){
  const axes=Object.entries(spec.variantAxes);
  let tuples=[{}];
  for(const [axis,values] of axes){
    const next=[];
    for(const partial of tuples)for(const value of values)next.push({...partial,[axis]:value});
    tuples=next;
  }
  const variants=tuples.map(values=>{
    const component=track(figma.createComponent());
    component.name=axes.map(([axis])=>axis+'='+values[axis]).join(', ');
    spec.page.appendChild(component);
    component.layoutMode=spec.baseProps.layoutMode;
    component.resize(spec.baseProps.width,spec.baseProps.height);
    component.primaryAxisSizingMode='FIXED';component.counterAxisSizingMode='FIXED';
    component.fills=[];component.clipsContent=false;
    component.x=CONFIG.layout.masterX;component.y=CONFIG.layout.masterY;
    return component;
  });
  const componentSet=track(figma.combineAsVariants(variants,spec.page));
  componentSet.name=spec.name;componentSet.description=spec.description;
  componentSet.layoutMode='NONE';componentSet.fills=[];componentSet.clipsContent=false;
  return {componentSet,variants};
}

const page=await figma.getNodeByIdAsync(CONFIG.pageId);
if(!page || page.type!=='PAGE') throw new Error('A página 03 — Componentes não existe.');
await figma.setCurrentPageAsync(page);
if(page.children.length) throw new Error('A página já contém material; retomar pelos IDs existentes para evitar duplicações.');

const [loadedVariables,colorCollection,loadedStyles]=await Promise.all([
  Promise.all(Object.values(FOUNDATION.variables).map(id=>figma.variables.getVariableByIdAsync(id))),
  figma.variables.getVariableCollectionByIdAsync(FOUNDATION.collections['AB / Color'].id),
  Promise.all(Object.values(FOUNDATION.styles).map(id=>figma.getStyleByIdAsync(id)))
]);
if(loadedVariables.some(v=>!v)||loadedStyles.some(s=>!s)||!colorCollection) throw new Error('Foundations incompletas.');
const VARIABLE_CACHE=Object.fromEntries(loadedVariables.map(v=>[v.id,v]));
const V=Object.fromEntries(Object.entries(FOUNDATION.variables).map(([name,id])=>[name,VARIABLE_CACHE[id]]));
const STYLE_CACHE=Object.fromEntries(loadedStyles.map(s=>[s.name,s]));
const FONTS=[...new Map(loadedStyles.map(s=>[JSON.stringify(s.fontName),s.fontName])).values()];
await Promise.all(FONTS.map(f=>figma.loadFontAsync(f)));
await figma.loadFontAsync({family:'Inter',style:'Regular'});

const created=new Set();
function track(n){created.add(n.id);return n;}
function allOf(n){return [n,...('children' in n?n.query('*').toArray():[])];}
function trackTree(n){for(const c of allOf(n))created.add(c.id);return n;}
function keyColor(name){return 'AB / Color/'+name;}
function keySpace(name){return 'AB / Geometry/space/'+name;}
function paint(name,opacity=1){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0},opacity},'color',V[keyColor(name)]);}
function bindFloat(n,field,key){n.setBoundVariable(field,V[key]);}
function radius(n,key='control'){bindFloat(n,'cornerRadius','AB / Geometry/radius/'+key);}
function padding(n,space){for(const k of ['paddingTop','paddingBottom','paddingLeft','paddingRight'])bindFloat(n,k,keySpace(space));}
function gap(n,space){bindFloat(n,'itemSpacing',keySpace(space));}
function fills(n,key,opacity=1){n.fills=key?[paint(key,opacity)]:[];}
function stroke(n,key,weight=1,opacity=1){n.strokes=key?[paint(key,opacity)]:[];n.strokeWeight=weight;n.strokeAlign='INSIDE';}
function auto(parent,name,direction='VERTICAL',width=null,space='4',pad='0'){
  const n=track(figma.createAutoLayout(direction));n.name=name;n.fills=[];n.clipsContent=false;
  parent.appendChild(n);padding(n,pad);gap(n,space);
  if(width!==null){n.resize(width,1);n.layoutSizingHorizontal='FIXED';n.layoutSizingVertical='HUG';}
  else{n.layoutSizingHorizontal='HUG';n.layoutSizingVertical='HUG';}
  return n;
}
async function text(parent,name,chars,style='AB / Body',color='fg',width=null){
  const n=track(figma.createText());n.name=name;n.fontName=STYLE_CACHE[style].fontName;
  await n.setTextStyleIdAsync(FOUNDATION.styles[style]);n.characters=chars;n.fills=[paint(color)];parent.appendChild(n);
  if(width!==null){n.textAutoResize='HEIGHT';n.resize(width,Math.max(n.height,1));n.layoutSizingHorizontal='FIXED';n.layoutSizingVertical='HUG';}
  else{n.textAutoResize='WIDTH_AND_HEIGHT';n.layoutSizingHorizontal='HUG';n.layoutSizingVertical='HUG';}
  return n;
}
function instance(parent,master,name,properties={},mode=null){
  const n=trackTree(master.createInstance());n.name=name;parent.appendChild(n);
  if(Object.keys(properties).length)n.setProperties(properties);
  if(mode)n.setExplicitVariableModeForCollection(colorCollection,FOUNDATION.collections['AB / Color'].modes[mode]);
  return n;
}
function focusRing(parent,width,height){
  const n=track(figma.createRectangle());n.name='Focus / ring';parent.appendChild(n);
  n.layoutPositioning='ABSOLUTE';n.resize(width+8,height+8);n.x=-4;n.y=-4;n.fills=[];n.strokes=[paint('focus')];n.strokeWeight=2;n.strokeAlign='INSIDE';radius(n);return n;
}
function bindVisualVector(node){
  for(const n of allOf(node)){
    if('fills' in n && Array.isArray(n.fills))n.fills=n.fills.map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',V[keyColor('fg')]):p);
    if('strokes' in n && Array.isArray(n.strokes))n.strokes=n.strokes.map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',V[keyColor('fg')]):p);
  }
}

// 1. Native SVG icon masters.
const icons={};
let iconIndex=0;
for(const [name,source] of Object.entries(ICON_SOURCE)){
  const comp=track(figma.createComponent());comp.name='AB/Icon/'+name;comp.description='Ícone AB nativo em grade de 24 px; fonte SVG em assets/icons/ui/'+name+'.svg. Cor vinculada a AB / Color/fg.';
  comp.layoutMode='HORIZONTAL';comp.resize(24,24);comp.primaryAxisSizingMode='FIXED';comp.counterAxisSizingMode='FIXED';comp.fills=[];comp.clipsContent=false;padding(comp,'0');gap(comp,'0');radius(comp,'none');
  page.appendChild(comp);
  const explicit=source.replace('<svg ','<svg width="24" height="24" ');
  const asset=trackTree(figma.createNodeFromSvg(explicit));asset.name='Vector / '+name;asset.resize(24,24);comp.appendChild(asset);bindVisualVector(asset);
  bindFloat(comp,'width','AB / Geometry/size/icon');bindFloat(comp,'height','AB / Geometry/size/icon');
  comp.x=CONFIG.layout.masterX+(iconIndex%4)*120;comp.y=CONFIG.layout.masterY+10+Math.floor(iconIndex/4)*120;icons[name]=comp;iconIndex++;
}

// 2. Button family with explicit orthogonal variant axes.
const btn=await makeVariantFamily({name:'AB/Button',description:'Botão de 48 px, raio de 8 px e label editável. Style: Primary/Secondary/Ghost. State: Default/Hover/Focus/Disabled. Os modos Light/Dark são herdados do contexto pelas variáveis semânticas.',variantAxes:{Style:['Primary','Secondary','Ghost'],State:['Default','Hover','Focus','Disabled']},baseProps:{width:200,height:48,layoutMode:'HORIZONTAL',fills:[]},page});
trackTree(btn.componentSet);btn.componentSet.x=CONFIG.layout.masterX;btn.componentSet.y=CONFIG.layout.masterY+320;btn.componentSet.fills=[];btn.componentSet.clipsContent=false;
const btnLabel=btn.componentSet.addComponentProperty('Label','TEXT','Continuar');
const buttonBy={};
for(const c of btn.variants){
  const props=Object.fromEntries(c.name.split(', ').map(s=>s.split('=')));const style=props.Style,state=props.State;
  c.description='Botão '+style+' / '+state+'. Estado de referência visual; não contém navegação de aplicativo.';
  c.clipsContent=false;c.primaryAxisAlignItems='CENTER';c.counterAxisAlignItems='CENTER';
  padding(c,'3');bindFloat(c,'paddingLeft',keySpace('4'));bindFloat(c,'paddingRight',keySpace('4'));gap(c,'2');radius(c);
  let bg=style==='Primary'?(state==='Hover'?'accent-hover':'accent'):(state==='Hover'?'selection':style==='Secondary'?'bg':null);
  let fg=style==='Primary'?'on-accent':'fg';
  if(state==='Disabled'){bg=style==='Ghost'?null:'surface';fg='muted';}
  fills(c,bg);stroke(c,style==='Secondary'?'border':null,1,state==='Disabled'?.35:1);
  const label=await text(c,'Label','Continuar','AB / Label',fg);label.componentPropertyReferences={characters:btnLabel};
  if(state==='Disabled')label.opacity=.6;
  if(state==='Focus')focusRing(c,200,48);
  c.resize(200,48);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';bindFloat(c,'height','AB / Geometry/size/control');buttonBy[style+'/'+state]=c;
}
// Reposition after combination (native variants do not auto-grid).
btn.variants.forEach((c,i)=>{c.x=40+(i%4)*248;c.y=40+Math.floor(i/4)*96;});btn.componentSet.resize(1040,320);

// 3. Badge atoms: semantic status, visible text and dot.
const badge=await makeVariantFamily({name:'AB/Badge',description:'Indicador textual de status. A palavra continua explícita em todos os modos; a cor e o ponto reforçam a informação. Label editável.',variantAxes:{Tone:['Neutral','Accent','Success','Error']},baseProps:{width:160,height:32,layoutMode:'HORIZONTAL',fills:[]},page});
trackTree(badge.componentSet);badge.componentSet.x=CONFIG.layout.masterX;badge.componentSet.y=CONFIG.layout.masterY+760;badge.componentSet.fills=[];
const badgeLabel=badge.componentSet.addComponentProperty('Label','TEXT','Planejado');
const badgeBy={};
for(const c of badge.variants){
  const tone=c.name.split('=')[1],color=tone==='Accent'?'on-accent':tone==='Success'?'success':tone==='Error'?'error':'fg';
  c.primaryAxisAlignItems='CENTER';c.counterAxisAlignItems='CENTER';padding(c,'1');bindFloat(c,'paddingLeft',keySpace('3'));bindFloat(c,'paddingRight',keySpace('3'));gap(c,'2');radius(c);
  fills(c,tone==='Accent'?'accent':'surface');stroke(c,tone==='Success'?'success':tone==='Error'?'error':null,1,.5);
  const dot=track(figma.createEllipse());dot.name='Status / dot';dot.resize(6,6);dot.fills=[paint(color)];c.appendChild(dot);
  const t=await text(c,'Label','Planejado','AB / Label',color);t.componentPropertyReferences={characters:badgeLabel};c.resize(160,32);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';badgeBy[tone]=c;
}
badge.variants.forEach((c,i)=>{c.x=40+i*208;c.y=40;});badge.componentSet.resize(880,112);

// 4. Input family: visible label + 48 px control + helper.
const inp=await makeVariantFamily({name:'AB/Input',description:'Campo com label, controle de 48 px e auxílio. State: Default/Focus/Error/Disabled. Label, Value e Hint são propriedades TEXT. Os estados demonstram a aparência do componente; não simulam coleta de dados.',variantAxes:{State:['Default','Focus','Error','Disabled']},baseProps:{width:264,height:106,layoutMode:'VERTICAL',fills:[]},page});
trackTree(inp.componentSet);inp.componentSet.x=CONFIG.layout.masterX;inp.componentSet.y=CONFIG.layout.masterY+980;inp.componentSet.fills=[];
const inputKeys={Label:inp.componentSet.addComponentProperty('Label','TEXT','Nome'),Value:inp.componentSet.addComponentProperty('Value','TEXT','Alexandre Belo'),Hint:inp.componentSet.addComponentProperty('Hint','TEXT','Nome para identificação.')};
const inputBy={};
for(const c of inp.variants){
  const state=c.name.split('=')[1];padding(c,'0');gap(c,'2');c.primaryAxisAlignItems='MIN';c.counterAxisAlignItems='MIN';fills(c,null);c.clipsContent=false;
  const label=await text(c,'Label','Nome','AB / Label',state==='Disabled'?'muted':'fg',264);label.componentPropertyReferences={characters:inputKeys.Label};
  const control=auto(c,'Control','HORIZONTAL',264,'2','3');control.resize(264,48);control.layoutSizingHorizontal='FIXED';control.layoutSizingVertical='FIXED';control.primaryAxisAlignItems='MIN';control.counterAxisAlignItems='CENTER';bindFloat(control,'paddingLeft',keySpace('4'));bindFloat(control,'paddingRight',keySpace('4'));radius(control);fills(control,state==='Disabled'?'surface':'bg');stroke(control,state==='Error'?'error':state==='Focus'?'focus':'border',state==='Focus'||state==='Error'?2:1,state==='Disabled'?.35:1);bindFloat(control,'height','AB / Geometry/size/control');
  const value=await text(control,'Value','Alexandre Belo','AB / Body',state==='Disabled'?'muted':'fg',232);value.componentPropertyReferences={characters:inputKeys.Value};
  if(state==='Disabled')value.opacity=.6;
  if(state==='Focus')focusRing(control,264,48);
  const hint=await text(c,'Hint','Nome para identificação.','AB / Caption',state==='Error'?'error':'muted',264);hint.componentPropertyReferences={characters:inputKeys.Hint};
  c.resize(264,106);c.primaryAxisSizingMode='AUTO';c.counterAxisSizingMode='FIXED';inputBy[state]=c;
}
inp.variants.forEach((c,i)=>{c.x=40+i*312;c.y=40;});inp.componentSet.resize(1320,186);

// 5. Card organism from native icon, badge and button instances.
const card=track(figma.createComponent());card.name='AB/Card';card.description='Card editorial de 440 px, com ícone AB, status, título, corpo e ação. Título e corpo editáveis; os elementos internos são instâncias dos respectivos masters. Raio de 24 px, padding e gaps vinculados.';
card.layoutMode='VERTICAL';card.resize(440,1);card.primaryAxisSizingMode='AUTO';card.counterAxisSizingMode='FIXED';card.primaryAxisAlignItems='MIN';card.counterAxisAlignItems='MIN';card.clipsContent=false;page.appendChild(card);padding(card,'6');gap(card,'4');radius(card,'card');fills(card,'surface');stroke(card,'border',1,.32);
const cardKeys={Title:card.addComponentProperty('Title','TEXT','Inteligência em trajetória'),Body:card.addComponentProperty('Body','TEXT','Observe, conecte evidências e avance com uma decisão clara.')};
const cardTop=auto(card,'Header','HORIZONTAL',392,'4','0');cardTop.primaryAxisAlignItems='SPACE_BETWEEN';cardTop.counterAxisAlignItems='CENTER';instance(cardTop,icons.focus,'Icon / focus');instance(cardTop,badgeBy.Accent,'Badge / context',{[badgeLabel]:'Em trajetória'});
const cardTitle=await text(card,'Title','Inteligência em trajetória','AB / Subheading','fg',392);cardTitle.componentPropertyReferences={characters:cardKeys.Title};
const cardBody=await text(card,'Body','Observe, conecte evidências e avance com uma decisão clara.','AB / Body','muted',392);cardBody.componentPropertyReferences={characters:cardKeys.Body};
const cardAction=instance(card,buttonBy['Primary/Default'],'Action',{[btnLabel]:'Explorar abordagem'});cardAction.resize(392,48);cardAction.layoutSizingHorizontal='FILL';
card.x=CONFIG.layout.masterX;card.y=CONFIG.layout.masterY+1300;

// 6. Review wrapper. All controls below are linked instances; masters stay outside.
const review=auto(page,'AB / Components — Review','HORIZONTAL',null,'12','0');review.x=CONFIG.layout.reviewX;review.y=CONFIG.layout.reviewY;review.counterAxisAlignItems='MIN';review.clipsContent=false;
const panels={};
const states=['Default','Hover','Focus','Disabled'];
const inputStates=['Default','Focus','Error','Disabled'];
const labels={Neutral:'Planejado',Accent:'Em andamento',Success:'Concluído',Error:'Revisar'};
async function section(parent,name,caption){
  const n=auto(parent,name,'VERTICAL',1184,'4','0');
  const h=auto(n,'Heading','HORIZONTAL',1184,'4','0');h.primaryAxisAlignItems='SPACE_BETWEEN';h.counterAxisAlignItems='CENTER';
  await text(h,'Title',name,'AB / Subheading','fg');await text(h,'Metadata',caption,'AB / Caption','muted');return n;
}
for(const mode of ['Light','Dark']){
  const panel=auto(review,'Review / '+mode,'VERTICAL',1280,'8','12');panel.setExplicitVariableModeForCollection(colorCollection,FOUNDATION.collections['AB / Color'].modes[mode]);fills(panel,'bg');stroke(panel,'border',1,.18);panels[mode]=panel.id;
  const head=auto(panel,'Intro','VERTICAL',1184,'2','0');await text(head,'Eyebrow','AB / INTERFACE','AB / Eyebrow','focus');await text(head,'Title','Componentes / '+(mode==='Light'?'Claro':'Escuro'),'AB / Heading','fg');await text(head,'Subtitle','Sora · controles de 48 px · cores, espaçamentos e raios vinculados','AB / Body','muted',1184);

  const buttons=await section(panel,'01 / Botões','3 estilos × 4 estados');
  const columns=auto(buttons,'State labels','HORIZONTAL',null,'6','0');const empty=auto(columns,'Style column','VERTICAL',152,'0','0');empty.resize(152,20);empty.layoutSizingVertical='FIXED';
  for(const state of states){const col=auto(columns,'Column / '+state,'VERTICAL',200,'0','0');await text(col,'State',state,'AB / Label','muted');}
  for(const style of ['Primary','Secondary','Ghost']){
    const row=auto(buttons,'Style / '+style,'HORIZONTAL',null,'6','0');row.counterAxisAlignItems='CENTER';const lbl=auto(row,'Style label','VERTICAL',152,'0','0');await text(lbl,'Label',style,'AB / Label','fg');
    for(const state of states)instance(row,buttonBy[style+'/'+state],style+' / '+state,{[btnLabel]:'Continuar'},mode);
  }

  const inputs=await section(panel,'02 / Campos','label + controle + auxílio');const inputRow=auto(inputs,'Input states','HORIZONTAL',null,'6','0');inputRow.counterAxisAlignItems='MIN';
  for(const state of inputStates){
    const cell=auto(inputRow,'Cell / '+state,'VERTICAL',264,'3','0');await text(cell,'State',state,'AB / Label','muted');
    const props={[inputKeys.Label]:'Nome',[inputKeys.Value]:state==='Error'?'Informe seu nome':'Alexandre Belo',[inputKeys.Hint]:state==='Error'?'Preencha o campo para continuar.':state==='Disabled'?'Campo indisponível.':'Nome para identificação.'};
    instance(cell,inputBy[state],'Input / '+state,props,mode);
  }

  const badges=await section(panel,'03 / Status','informação sempre explícita');const badgeRow=auto(badges,'Badge states','HORIZONTAL',null,'6','0');
  for(const tone of ['Neutral','Accent','Success','Error']){
    const cell=auto(badgeRow,'Cell / '+tone,'VERTICAL',264,'3','0');await text(cell,'Tone',tone,'AB / Label','muted');instance(cell,badgeBy[tone],'Badge / '+tone,{[badgeLabel]:labels[tone]},mode);
  }

  const bottom=auto(panel,'04 + 05 / Molecule and icons','HORIZONTAL',null,'12','0');bottom.counterAxisAlignItems='MIN';
  const cardSection=auto(bottom,'04 / Card','VERTICAL',440,'4','0');await text(cardSection,'Heading','04 / Card','AB / Subheading','fg');instance(cardSection,card,'Card / example',{},mode);
  const iconSection=auto(bottom,'05 / Ícones','VERTICAL',656,'4','0');await text(iconSection,'Heading','05 / Ícones','AB / Subheading','fg');const gallery=auto(iconSection,'Gallery','VERTICAL',656,'4','0');
  const order=['observe','focus','direction','build','learn','check','arrow-right','close'];
  for(let rowIndex=0;rowIndex<2;rowIndex++){
    const row=auto(gallery,'Icon row '+(rowIndex+1),'HORIZONTAL',null,'4','0');
    for(const name of order.slice(rowIndex*4,rowIndex*4+4)){
      const cell=auto(row,'Icon / '+name,'VERTICAL',152,'3','4');cell.counterAxisAlignItems='CENTER';radius(cell);fills(cell,'surface');instance(cell,icons[name],name,{},mode);await text(cell,'Name',name,'AB / Label','muted');
    }
  }
  await text(panel,'Footer','29 masters reutilizáveis · dois modos · estados visuais de referência','AB / Caption','muted',1184);
}

// Native structure, style and token evidence (no screenshot/flattened UI in the file).
const nodes=page.query('*').toArray();for(const n of nodes)created.add(n.id);
const texts=nodes.filter(n=>n.type==='TEXT');
const wrongFonts=texts.filter(n=>n.fontName.family!==BRAND.typography.family).map(n=>({id:n.id,font:n.fontName}));
if(wrongFonts.length)throw new Error('Fonte divergente da Sora: '+JSON.stringify(wrongFonts));
const boundNodes=nodes.filter(n=>n.boundVariables && Object.keys(n.boundVariables).length);
const fields={};for(const n of boundNodes)for(const f of Object.keys(n.boundVariables))fields[f]=(fields[f]||0)+1;
const imageNodes=nodes.filter(n=>'fills' in n && Array.isArray(n.fills)&&n.fills.some(p=>p.type==='IMAGE')).map(n=>({id:n.id,name:n.name,type:n.type,width:n.width,height:n.height}));
if(imageNodes.length)throw new Error('Foi encontrada imagem raster inesperada.');
const reviewNodes=review.query('*').toArray(),types={};for(const n of reviewNodes)types[n.type]=(types[n.type]||0)+1;
const styleCounts={};for(const n of texts){const k=n.textStyleId;styleCounts[k]=(styleCounts[k]||0)+1;}
function familyData(f){return {id:f.componentSet.id,name:f.componentSet.name,properties:f.componentSet.componentPropertyDefinitions,variants:f.variants.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height}))};}
const sample=buttonBy['Primary/Focus'];
return {fileKey:CONFIG.fileKey,createdNodeIds:[...created],mutatedNodeIds:[page.id],pageId:page.id,components:{Button:familyData(btn),Input:familyData(inp),Badge:familyData(badge),Card:{id:card.id,name:card.name,width:card.width,height:card.height,properties:card.componentPropertyDefinitions},Icons:Object.fromEntries(Object.entries(icons).map(([name,c])=>[name,c.id]))},propertyKeys:{button:btnLabel,input:inputKeys,badge:badgeLabel,card:cardKeys},review:{id:review.id,width:review.width,height:review.height,panels,descendantCount:reviewNodes.length,typeCounts:types,imageFilledNodes:imageNodes},fontProof:{family:BRAND.typography.family,textNodeCount:texts.length,wrongFonts,styleCounts},bindingProof:{boundNodeCount:boundNodes.length,fields,sampleButton:{id:sample.id,boundVariables:sample.boundVariables,fills:sample.fills},modeCollectionId:colorCollection.id,modes:FOUNDATION.collections['AB / Color'].modes},counts:{componentSets:3,masters:29,buttons:12,inputs:4,badges:4,cards:1,icons:8,nodes:nodes.length}};
