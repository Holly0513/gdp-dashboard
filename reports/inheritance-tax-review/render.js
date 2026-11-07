const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1,viewport:{width:794,height:1123}});
await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const o=await p.evaluate(()=>[...document.querySelectorAll('.content')].map((c,i)=>[i+2,c.scrollHeight-c.clientHeight]).filter(x=>x[1]>0));console.log('overflow',JSON.stringify(o));
await p.pdf({path:process.argv[3],format:'A4',printBackground:true,preferCSSPageSize:true});await b.close();})();
