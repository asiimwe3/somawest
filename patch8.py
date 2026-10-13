g = open('gen_pages.py').read()

# ---- 1. JSON-LD schema + og:image in <head> ----
old_head = '''<link rel="canonical" href="{SITE}school/{slug}">
<style>{CSS}</style>'''
new_head = '''<link rel="canonical" href="{SITE}school/{slug}">
{ogimg}
<script type="application/ld+json">{jsonld}</script>
<style>{CSS}</style>'''
assert old_head in g
g = g.replace(old_head, new_head, 1)

# ---- 2. compute jsonld/ogimg in page_html ----
old_mapq = 'mapq = urllib.parse.quote(f"{name} {district} Uganda")\n    coordsline = f"Coordinates: {la}, {lo} · " if la and lo else ""'
new_mapq = old_mapq + '''
    geo = ""
    if la and lo:
        try:
            geo = f'"geo":{{"@type":"GeoCoordinates","latitude":{float(la)},"longitude":{float(lo)}}},'
        except (TypeError, ValueError):
            geo = ""
    jsonld = json.dumps({"@context":"https://schema.org","@type":"School","name":name,
        "url":f"{SITE}school/{slug}",
        "address":{"@type":"PostalAddress","addressRegion":f"{district}, Western Uganda","addressCountry":"UG"},
        "areaServed":district + " district, Western Uganda", **{"geo": {}}, })
    if geo:
        jsonld = jsonld[:-2] + "," + geo.rstrip(",") + "}"
    ogimg = f'<meta property="og:image" content="{feat["img"]}">' if feat and feat.get("img") else ""'''
assert old_mapq in g
g = g.replace(old_mapq, new_mapq, 1)

# ---- 3. rank badge on school page ----
old_track = 'track("view");'
new_track = '''track("view");
fetch("{API}").then(function(r){{return r.json()}}).then(function(d){{
  if(!d||!d.ok||!d.ranked)return;
  var me=d.ranked.findIndex(function(r){{return r.slug===SLUG}});
  if(me>-1){{var b=document.createElement("div");b.style.cssText="background:#d4a017;color:#1c1602;font-weight:800;border-radius:99px;display:inline-block;padding:8px 14px;font-size:14px;margin-top:8px";b.textContent="🏆 #"+(me+1)+" on SomaWest — popular with parents";var h1=document.querySelector("h1");h1.parentNode.insertBefore(b,h1.nextSibling);}}
}}).catch(function(){{}});'''
assert old_track in g
g = g.replace(old_track, new_track, 1)

open('gen_pages.py','w').write(g)
print('gen_pages patched')
