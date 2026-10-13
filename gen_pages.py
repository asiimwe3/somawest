#!/usr/bin/env python3
"""Generate static SEO pages for every SomaWest school + sitemap."""
import json, re, html, os, urllib.parse

SITE = "https://asiimwe3.github.io/somawest/"
API = "https://superagent-c4c23880.base44.app/functions/somawestTrack"
DESK = "256772002326"

def slugify(name, district):
    s = re.sub(r"[^a-z0-9]+", "-", f"{name}-{district}".lower()).strip("-")
    return s[:90] or "school"

# load listings
src = open("schools-data.js").read()
m = re.search(r"const LISTINGS\s*=\s*(\[.*?\]);", src, re.S)
listings = json.loads(m.group(1))

# featured data from index.html (name, district, img, blurb, level, board, gender, founded, phone, site, loc)
idx = open("index.html").read()
featured = []
for blob in re.findall(r"\{id:\"[^\"]+\", name:\"([^\"]+)\"[^}]*?\}", idx[idx.index("const SCHOOLS"):idx.index("];", idx.index("const SCHOOLS"))]):
    pass
# simpler: parse each school line
sblock = idx[idx.index("const SCHOOLS"):idx.index("\n];", idx.index("const SCHOOLS"))]
for line in re.findall(r"\{id:.*?\}", sblock):
    def g(k):
        mm = re.search(k + r':"([^"]*)"', line)
        return mm.group(1) if mm else ""
    featured.append({
        "name": g("name"), "district": g("district"), "loc": g("loc"), "gender": g("gender"),
        "board": g("board"), "level": g("level"), "founded": g("founded"), "phone": g("phone"),
        "img": g("img"), "blurb": g("blurb"), "site": g("site")
    })

used = {}
pages = []  # (slug, name, district, level, featured?)

def reg_slug(name, district):
    s = slugify(name, district)
    if s in used:
        used[s] += 1
        s = f"{s}-{used[s]}"
    else:
        used[s] = 0
    return s

CSS = """
*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f5f6f4;color:#16211c;line-size:16px}
.hd{position:sticky;top:0;background:#0b3d2e;color:#fff;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;z-index:9}
.hd b{font-size:20px}.hd span{font-size:12px;letter-spacing:1px;color:#d4a017;display:block}
.wrap{max-width:760px;margin:0 auto;padding:16px}
h1{font-size:26px;line-height:1.2;margin:14px 0 6px}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 14px}
.badges i{background:#e8e5da;border-radius:99px;padding:6px 12px;font-style:normal;font-weight:600;font-size:13px;color:#2b3a32}
.badges i.gold{background:#d4a017;color:#1c1602}
.photo{width:100%;border-radius:14px;max-height:300px;object-fit:cover}
.card{background:#fff;border:1px solid #e2e0d5;border-radius:14px;padding:16px;margin:14px 0}
.map{width:100%;height:280px;border:0;border-radius:14px;margin:8px 0}
label{display:block;font-weight:600;font-size:14px;margin:10px 0 4px}
input,select{width:100%;padding:12px;border:1.5px solid #cfd4cc;border-radius:10px;font-size:16px;background:#fff}
.btn{display:inline-block;width:100%;margin-top:14px;background:#0b3d2e;color:#fff;border:0;border-radius:12px;padding:14px;font-size:17px;font-weight:700;text-align:center;text-decoration:none}
.btn.gold{background:#d4a017;color:#1c1602}
.btn.ghost{background:#fff;color:#0b3d2e;border:2px solid #0b3d2e}
.small{font-size:13px;color:#6b7a70;margin-top:6px}
h2{font-size:19px;margin:6px 0}
.ft{background:#0b3d2e;color:#cfe0d6;padding:22px 16px;text-align:center;font-size:14px;margin-top:24px}
.ft a{color:#d4a017}
"""

def esc(s): return html.escape(str(s), quote=True)

def page_html(slug, name, district, level, la, lo, feat=None):
    title = f"{esc(name)} — {esc(level)} in {esc(district)}, Western Uganda | SomaWest"
    desc = f"{esc(name)} in {esc(district)} district, Western Uganda. Location on map, admission requirements and how to apply — via SomaWest, the school finder for Western Uganda."
    name_j = json.dumps(name)
    dist_j = json.dumps(district)
    photo = f'<img class="photo" src="{feat["img"]}" alt="{esc(name)}">' if feat and feat.get("img") else ""
    blurb = f'<p style="margin-top:10px">{esc(feat["blurb"])}</p>' if feat and feat.get("blurb") else ""
    fb = ""
    if feat:
        bits = []
        if feat.get("gender"): bits.append(f'<i>{esc(feat["gender"])}</i>')
        if feat.get("board") and feat["board"] != "—": bits.append(f'<i class="gold">{esc(feat["board"])}</i>')
        if feat.get("founded"): bits.append(f'<i>Est. {esc(feat["founded"])}</i>')
        if feat.get("phone"): bits.append(f'<i>{esc(feat["phone"])}</i>')
        fb = "".join(bits)
    mapq = urllib.parse.quote(f"{name} {district} Uganda")
    wa_share = urllib.parse.quote(f"{name} ({level}, {district} district) is on SomaWest — the school finder for Western Uganda: {SITE}school/{slug}")
    claim_msg = urllib.parse.quote(f"Hello SomaWest, I represent {name} in {district} district. I want to manage our listing. Here is our updated info: 1) fees per term, 2) WhatsApp/phone contacts, 3) photos, 4) term dates, 5) admission requirements.")
    levelsel = "selected" if level == "Secondary" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{esc(name)} | SomaWest">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="../favicon.png">
<link rel="canonical" href="{SITE}school/{slug}">
<style>{CSS}</style>
</head>
<body>
<div class="hd"><div><b>SomaWest</b><span>SCHOOL FINDER · WESTERN UGANDA</span></div><a href="../" style="color:#d4a017;font-weight:600;text-decoration:none">All schools</a></div>
<div class="wrap">
<h1>{esc(name)}</h1>
<div class="badges"><i>{esc(level)}</i><i>{esc(district)} district</i>{fb}</div>
{photo}{blurb}
<div class="card">
<h2>Location</h2>
<p class="small">Map position of the school (OpenStreetMap data):</p>
<iframe class="map" loading="lazy" src="https://www.google.com/maps?q={mapq}&output=embed"></iframe>
<p class="small">Coordinates: {la}, {lo} · <a href="https://www.google.com/maps/search/{mapq}" target="_blank" rel="noopener">Open in Google Maps</a></p>
</div>
<div class="card" id="apply">
<h2>Apply for admission</h2>
<label>Student name</label><input id="st" placeholder="Full name of the student">
<label>Class applying for</label><select id="cl"><option value="">Choose class/level</option><option>Nursery</option><option>Primary</option><option selected>S.1</option><option>S.2</option><option>S.3</option><option>S.4</option><option>S.5</option><option>S.6</option></select>
<label>Previous school (if any)</label><input id="ps" placeholder="Last school attended">
<label>Parent / guardian name</label><input id="pn" placeholder="Your name">
<label>Phone (WhatsApp)</label><input id="pp" placeholder="e.g. 0772 000 000">
<button class="btn" onclick="sendApply()">Send application on WhatsApp</button>
<p class="small">Opens WhatsApp with your application — no account needed. SomaWest admissions desk follows up with the school.</p>
</div>
<a class="btn ghost" href="https://wa.me/?text={wa_share}" target="_blank" rel="noopener" onclick="track('share')">Share this school on WhatsApp</a>
<a class="btn ghost" href="https://wa.me/{DESK}?text={claim_msg}" target="_blank" rel="noopener">School owner? Manage this listing</a>
</div>
<div class="ft">Part of <a href="../">SomaWest</a> — every school in Western Uganda.<br>School data © OpenStreetMap contributors · Platform by Derycode</div>
<script>
const SLUG={json.dumps(slug)},NAME={name_j},DIST={dist_j};
function track(ev){{fetch("{API}",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{slug:SLUG,name:NAME,district:DIST,event:ev}})}}).catch(function(){{}});}}
track("view");
function sendApply(){{
  var st=document.getElementById("st").value,cl=document.getElementById("cl").value,ps=document.getElementById("ps").value,pn=document.getElementById("pn").value,pp=document.getElementById("pp").value;
  if(!st||!pp){{alert("Please fill the student name and guardian phone.");return;}}
  var msg="APPLICATION via SomaWest\\n\\nSchool: "+NAME+" ("+DIST+" district)\\nStudent: "+st+"\\nClass applying for: "+(cl||"not stated")+"\\nPrevious school: "+(ps||"none")+"\\nGuardian: "+(pn||"—")+"\\nPhone: "+pp;
  track("apply");
  window.open("https://wa.me/{DESK}?text="+encodeURIComponent(msg),"_blank");
}}
</script>
</body>
</html>"""

os.makedirs("school", exist_ok=True)

# featured pages
for f in featured:
    slug = reg_slug(f["name"], f["district"])
    lv = f.get("level") or "School"
    pages.append((slug, f["name"], f["district"], lv))
    open(f"school/{slug}.html", "w").write(page_html(slug, f["name"], f["district"], lv, "", "", feat=f))

# directory pages
for s in listings:
    slug = reg_slug(s["n"], s["d"])
    lv = s.get("lv") or "School"
    pages.append((slug, s["n"], s["d"], lv))
    open(f"school/{slug}.html", "w").write(page_html(slug, s["n"], s["d"], lv, s.get("la"), s.get("lo")))

# sitemap
with open("sitemap.xml", "w") as sm:
    sm.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    sm.write(f"  <url><loc>{SITE}</loc><priority>1.0</priority></url>\n")
    for slug, name, d, lv in pages:
        sm.write(f"  <url><loc>{SITE}school/{slug}.html</loc><priority>0.6</priority></url>\n")
    sm.write("</urlset>\n")

open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")

print("pages:", len(pages), "featured:", len(featured))
