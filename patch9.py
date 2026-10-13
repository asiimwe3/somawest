g = open('gen_pages.py').read()

# remove the broken geo surgery block
old = '''    geo = ""
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
        jsonld = jsonld[:-2] + "," + geo.rstrip(",") + "}"'''
new = '''    schema = {"@context":"https://schema.org","@type":"School","name":name,
        "url":f"{SITE}school/{slug}",
        "address":{"@type":"PostalAddress","addressRegion":f"{district}, Western Uganda","addressCountry":"UG"},
        "areaServed":district + " district, Western Uganda"}
    try:
        if la != "" and lo != "":
            schema["geo"] = {"@type":"GeoCoordinates","latitude":float(la),"longitude":float(lo)}
    except (TypeError, ValueError):
        pass
    jsonld = json.dumps(schema)'''
assert old in g
g = g.replace(old, new, 1)
open('gen_pages.py','w').write(g)
print('patched')
