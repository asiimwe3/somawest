h = open('index.html').read()

# ---- 1. claim checklist message ----
old = "const msg = 'Hello SomaWest, I represent ' + name + '. I would like to update and manage our school listing (fees, photos, contacts, term dates).';"
new = "const msg = 'Hello SomaWest, I represent ' + name + '. I want to manage our listing. Here is our updated info:\\n1) Fees per term\\n2) WhatsApp/phone contacts\\n3) Photos\\n4) Term dates\\n5) Admission requirements';"
assert old in h, 'claim msg not found'
h = h.replace(old, new, 1)

# ---- 2. share + full page links in BOTH modals ----
share_js = '''
function shareSchool(name, district, slug){
  const url = 'https://asiimwe3.github.io/somawest/school/' + (slug || slugFor(name, district)) + '.html';
  const msg = name + ' (' + district + ' district) is on SomaWest, the school finder for Western Uganda: ' + url;
  track(slugFor(name, district), name, district, 'share');
  window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
}
'''
h = h.replace('function claimSchool(name){', share_js + 'function claimSchool(name){', 1)

# featured modal: add share + full page before manage link
feat_anchor = '''<a class="btn o" onclick="claimSchool('${s.name.replace(/'/g,"\\'")}')" style="background:#fff;border:1.5px solid #0b3d2e;color:#0b3d2e">School owner? Manage listing</a>'''
feat_new = '''<a class="btn o" target="_blank" rel="noopener" href="school/${slugFor(s.name, s.district)}.html">Open full school page</a>
        <a class="btn o" onclick="shareSchool('${s.name.replace(/'/g,"\\'")}', '${s.district}')">Share on WhatsApp</a>
        ''' + feat_anchor
assert feat_anchor in h, 'feat anchor missing'
h = h.replace(feat_anchor, feat_new, 1)

# dir modal: add share + full page before manage link
dir_anchor = '''<a class="btn o" onclick="claimSchool('${s.n.replace(/'/g,"\\'")}')" style="background:#fff;border:1.5px solid #0b3d2e;color:#0b3d2e">School owner? Manage listing</a>'''
dir_new = '''<a class="btn o" target="_blank" rel="noopener" href="school/${slugFor(s.n, s.d)}.html">Open full school page</a>
        <a class="btn o" onclick="shareSchool('${s.n.replace(/'/g,"\\'")}', '${s.d}')">Share on WhatsApp</a>
        ''' + dir_anchor
assert dir_anchor in h, 'dir anchor missing'
h = h.replace(dir_anchor, dir_new, 1)

open('index.html','w').write(h)
print('patch6 done: claim checklist, share, page links')
