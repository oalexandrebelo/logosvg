// Run in Figma Plugin API through use_figma with CONFIG injected from
// tokens/brand.tokens.json. This source creates the AB foundations once.
// Collection and alias helpers follow the figma-generate-library skill.
const createdNodeIds=[];
const mutatedNodeIds=[];
const collections={}, variables={}, styles={}, pages={};
const existing=await figma.variables.getLocalVariableCollectionsAsync();
if(existing.some(c=>c.name.startsWith('AB / '))) throw new Error('AB foundations already exist. Read the state ledger before updating.');
await Promise.all(['Regular','Light','SemiBold','Bold'].map(style=>figma.loadFontAsync({family:'Sora',style})));
for(const definition of CONFIG.collections) {
  const collection=figma.variables.createVariableCollection(definition.name);
  collection.renameMode(collection.modes[0].modeId,definition.modes[0]);
  const modeIds={[definition.modes[0]]:collection.modes[0].modeId};
  for(const name of definition.modes.slice(1)) modeIds[name]=collection.addMode(name);
  collections[definition.name]={id:collection.id,modes:modeIds};
  for(const token of definition.tokens) {
    const variable=figma.variables.createVariable(token.name,collection,token.type);
    variable.scopes=token.scopes;
    variable.setVariableCodeSyntax('WEB',`var(${token.css})`);
    for(const [mode,raw] of Object.entries(token.values)) {
      let value=raw;
      if(raw && typeof raw==='object' && raw.alias) {
        if(!variables[raw.alias]) throw new Error('Missing primitive '+raw.alias);
        value={type:'VARIABLE_ALIAS',id:variables[raw.alias]};
      } else if(token.type==='COLOR') {
        value={r:parseInt(raw.slice(1,3),16)/255,g:parseInt(raw.slice(3,5),16)/255,b:parseInt(raw.slice(5,7),16)/255,a:1};
      }
      variable.setValueForMode(modeIds[mode],value);
    }
    variables[definition.name+'/'+token.name]=variable.id;
  }
}
for(const def of CONFIG.textStyles) {
  const style=figma.createTextStyle();
  style.name=def.name;
  style.fontName={family:'Sora',style:def.style};
  style.fontSize=def.size;
  style.lineHeight={unit:'PIXELS',value:def.line};
  style.letterSpacing={unit:'PIXELS',value:def.tracking};
  styles[def.name]=style.id;
}
const names=['01 — Brandbook','02 — Assinaturas','03 — Componentes','04 — Aplicações'];
for(let i=0;i<names.length;i++) {
  const page=i===0?figma.currentPage:figma.createPage();
  page.name=names[i];
  page.backgrounds=[{type:'SOLID',color:{r:.83,g:.85,b:.88}}];
  pages[names[i]]=page.id;
  if(i===0) mutatedNodeIds.push(page.id); else createdNodeIds.push(page.id);
}
return {createdNodeIds,mutatedNodeIds,collections,variables,styles,pages,counts:{collections:Object.keys(collections).length,variables:Object.keys(variables).length,styles:Object.keys(styles).length,pages:Object.keys(pages).length}};
