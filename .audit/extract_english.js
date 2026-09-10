const fs=require('fs');
const vm=require('vm');
const html=fs.readFileSync('index.html','utf8');

function extractAssignedObjects(src){
  const out=[];
  const re=/(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*\{/g;
  let m;
  while((m=re.exec(src))){
    const name=m[1], start=src.indexOf('{',m.index), n=src.length;
    let depth=0, quote=null, esc=false, tplDepth=0, end=-1;
    for(let i=start;i<n;i++){
      const c=src[i], p=src[i-1];
      if(quote){
        if(esc){esc=false;continue;}
        if(c==='\\'){esc=true;continue;}
        if(quote==='`' && c==='$' && src[i+1]==='{'){ tplDepth++; i++; depth++; continue; }
        if(c===quote && tplDepth===0){quote=null;continue;}
        if(quote==='`' && c==='}' && tplDepth>0){ tplDepth--; depth--; continue; }
        continue;
      }
      if(c==='"'||c==="'"||c==='`'){quote=c;continue;}
      if(c==='{') depth++;
      else if(c==='}') {depth--; if(depth===0){end=i+1;break;}}
    }
    if(end<0) continue;
    const objText=src.slice(start,end);
    try{
      const val=vm.runInNewContext('('+objText+')',{}, {timeout:1000});
      if(val && typeof val==='object' && val.en && typeof val.en==='object') out.push({name,val:val.en});
    }catch(e){}
  }
  return out;
}

const objs=extractAssignedObjects(html);
console.log('=== ENGLISH CONTENT OBJECTS ===');
for(const {name,val} of objs){
  console.log('\n### '+name);
  console.log(JSON.stringify(val,null,2));
}

console.log('\n=== STATIC CYRILLIC TEXT IN HTML ===');
const body=html.match(/<body[\s\S]*?<\/body>/i)?.[0]||html;
const noScripts=body.replace(/<script[\s\S]*?<\/script>/gi,'').replace(/<style[\s\S]*?<\/style>/gi,'');
const text=noScripts.replace(/<[^>]+>/g,'\n').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/\n\s*\n/g,'\n');
for(const line of text.split('\n').map(s=>s.trim()).filter(Boolean)){
  if(/[А-Яа-яЁёҮүӨөҢң]/.test(line)) console.log(line);
}

console.log('\n=== ENGLISH FALLBACK TEXT SAMPLE ===');
for(const line of text.split('\n').map(s=>s.trim()).filter(Boolean)){
  if(/[A-Za-z]/.test(line) && !/[А-Яа-яЁёҮүӨөҢң]/.test(line)) console.log(line);
}
