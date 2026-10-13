h = open('index.html').read()

# ---- CSS for ranking section ----
h = h.replace('</style>', '''
#rankWrap{background:#0b3d2e;border-radius:18px;padding:18px;margin:18px 0 6px}
#rankWrap h2{color:#fff;font-size:20px;margin:0}
#rankWrap p{color:#cfe0d6;font-size:13px;margin:4px 0 12px}
.rank-row{display:flex;align-items:center;gap:12px;background:#fff;border-radius:12px;padding:10px 12px;margin:8px 0;text-decoration:none}
.rank-n{background:#d4a017;color:#1c1602;font-weight:800;border-radius:10px;min-width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:16px}
.rank-b{flex:1}.rank-b b{display:block;font-size:15px;color:#16211c}
.rank-b span{font-size:12px;color:#6b7a70}
.rank-m{font-size:12px;color:#6b7a70;text-align:right}
.rank-m b{color:#0b3d2e;font-size:14px}
</style>''', 1)

# ---- ranking section HTML above the tabs (inside main, before search bar section) ----
anchor = '<div class="res-head">'
rank_html = '''<div id="rankWrap">
  <h2>🏆 Top schools on SomaWest</h2>
  <p>Live ranking by parent activity — views, applications and shares. Like Booking.com's popularity index, it updates automatically.</p>
  <div id="rankList"><div style="color:#cfe0d6;font-size:14px">Loading ranking…</div></div>
</div>
'''
h = h.replace(anchor, rank_html + anchor, 1)

# ---- JS: fetch and render ranking ----
rank_js = '''
function renderRanking(){
  fetch(TRACK_API).then(r=>r.json()).then(d=>{
    const el=document.getElementById('rankList');
    if(!d.ok||!d.ranked||!d.ranked.length){el.innerHTML='<div style="color:#cfe0d6;font-size:14px">Ranking builds as parents browse — activity from real visitors decides the order.</div>';return;}
    el.innerHTML=d.ranked.slice(0,10).map((r,i)=>`<a class="rank-row" href="school/${r.slug}.html">
      <div class="rank-n">${i+1}</div>
      <div class="rank-b"><b>${r.name}</b><span>${r.district} district</span></div>
      <div class="rank-m"><b>${r.score}</b><br>score</div></a>`).join('');
  }).catch(()=>{document.getElementById('rankList').innerHTML='';});
}
renderRanking();
'''
h = h.replace('function slugFor(name,district){', rank_js + '\nfunction slugFor(name,district){', 1)

open('index.html','w').write(h)
print('patch7 done')
