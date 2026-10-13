h = open('index.html').read()

# ---- 1. CSS ----
h = h.replace('</style>', '''
#nearBtn{border:2px solid #0b3d2e;background:#fff;color:#0b3d2e;font-weight:700}
.share-row{display:flex;gap:10px;margin-top:10px}
.share-row a{flex:1;text-align:center;padding:12px;border-radius:12px;background:#fff;border:2px solid #0b3d2e;color:#0b3d2e;font-weight:700;text-decoration:none}
.tile .km{font-weight:700;color:#0b3d2e}
</style>''', 1)

# ---- 2. Near me button in tabs row ----
h = h.replace('</div>\n<div class="res-head">', '''</div>
<div style="padding:0 0 12px"><button id="nearBtn" class="tab" onclick="nearMe()">📍 Schools near me</button></div>
<div class="res-head">''', 1)

# ---- 3. JS additions ----
addition = '''
// ---------- near me + slugs + tracking + share ----------
const TRACK_API='https://superagent-c4c23880.base44.app/functions/somawestTrack';
function slugifyBase(s){s=(s||'').toLowerCase();s=s.replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');return (s||'school').slice(0,90);}
const SLUGS={};{const used={};const reg=(n,d)=>{let b=slugifyBase(n+'-'+d);if(used[b]){used[b]++;b=b+'-'+used[b];}else used[b]=0;return b;};SCHOOLS.forEach(s=>SLUGS[s.name+'|'+s.district]=reg(s.name,s.district));LISTINGS.forEach(s=>SLUGS[s.n+'|'+s.d]=reg(s.n,s.d));}
function slugFor(name,district){return SLUGS[name+'|'+district]||slugifyBase(name+'-'+district);}
function track(slug,name,district,ev){try{fetch(TRACK_API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({slug:slug,name:name,district:district,event:ev})}).catch(function(){});}catch(e){}}
function nearMe(){
  if(!navigator.geolocation){alert('Location not available on this device.');return;}
  document.getElementById('nearBtn').textContent='📍 Locating…';
  navigator.geolocation.getCurrentPosition(function(p){
    const la=p.coords.latitude,lo=p.coords.longitude;
    const dist=(a,b,c,d)=>{const R=6371,dLa=(c-a)*Math.PI/180,dLo=(d-b)*Math.PI/180;const x=Math.sin(dLa/2)*Math.sin(dLa/2)+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(dLo/2)*Math.sin(dLo/2);return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x));};
    state.near={la,lo,dist};
    document.getElementById('nearBtn').textContent='📍 Nearest first (tap to clear)';
    render();
  },function(){document.getElementById('nearBtn').textContent='📍 Schools near me';alert('Could not get your location. Check that location is allowed.');},{timeout:9000});
}
'''
h = h.replace('function applySchool(name, district){', addition + '\nfunction applySchool(name, district){', 1)

# near clear toggle
h = h.replace("document.getElementById('nearBtn').textContent='📍 Nearest first (tap to clear)';",
"document.getElementById('nearBtn').textContent='📍 Nearest first (tap to clear)';document.getElementById('nearBtn').onclick=clearNear;", 1)
addition2 = '''
function clearNear(){state.near=null;document.getElementById('nearBtn').textContent='📍 Schools near me';document.getElementById('nearBtn').onclick=nearMe;render();}
'''
h = h.replace('function applySchool(name, district){', addition2 + 'function applySchool(name, district){', 1)

# ---- 4. render(): distance sorting ----
h = h.replace("const dirMatch=LISTINGS.filter(matchDir);",
"let dirMatch=LISTINGS.filter(matchDir);if(state.near){dirMatch=dirMatch.slice().sort((a,b)=>state.near.dist(state.near.la,state.near.lo,a.la,a.lo)-state.near.dist(state.near.la,state.near.lo,b.la,b.lo));}", 1)

# ---- 5. tile shows km when near ----
h = h.replace("<b>${s.n}</b>",
"<b>${s.n}</b>${state.near?`<div class='km'>${state.near.dist(state.near.la,state.near.lo,s.la,s.lo).toFixed(1)} km away</div>`:''}", 1)

# ---- 6. track view on modals ----
h = h.replace("function openModal(id){\n  const s=SCHOOLS.find(x=>x.id===id);",
"function openModal(id){\n  const s=SCHOOLS.find(x=>x.id===id);\n  track(slugFor(s.name,s.district),s.name,s.district,'view');", 1)
h = h.replace("function openDir(i){\n  const s=LISTINGS[i];",
"function openDir(i){\n  const s=LISTINGS[i];\n  track(slugFor(s.n,s.d),s.n,s.d,'view');", 1)

# ---- 7. claim checklist message ----
old_claim = "const m=encodeURIComponent(`Hello SomaWest, I represent ${name} in ${district||'Western Uganda'}. I would like to update and manage our school listing.`);"
new_claim = "const m=encodeURIComponent(`Hello SomaWest, I represent ${name} in ${district||'Western Uganda'}. I want to manage our listing. Here is our updated info:\\n1) Fees per term\\n2) WhatsApp/phone contacts\\n3) Photos\\n4) Term dates\\n5) Admission requirements`);"
if old_claim in h: h = h.replace(old_claim, new_claim); print('claim msg patched')

# ---- 8. share + page link in dir modal acts ----
old_acts = '<a class="btn o" target="_blank" rel="noopener" href="https://wa.me/?text='
if old_acts in h:
    print('share already present')
else:
    h = h.replace('''<div class="acts">
        <a class="btn g" target="_blank" rel="noopener" href="https://wa.me/256772002326?text=${encodeURIComponent(`APPLICATION via SomaWest\\n\\nSchool: ${s.n} (${s.d} district)\\nStudent: ${st}....`}''', 'XX-NOPE', 1)

open('index.html','w').write(h)
print('patch5 core done')
