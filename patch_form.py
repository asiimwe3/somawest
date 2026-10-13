import re

h = open('index.html').read()

# 1. form CSS
form_css = """
#addModal .sheet{max-width:560px}
.aform{padding:18px}
.aform h3{margin:0 0 2px;font-size:24px}
.aform .sub{color:#667;font-size:14px;margin-bottom:14px}
.aform label{display:block;font-weight:700;font-size:14px;margin:12px 0 6px}
.aform input,.aform select,.aform textarea{width:100%;box-sizing:border-box;padding:12px;border:1.5px solid #cbd5d0;border-radius:10px;font-size:16px;background:#fff;font-family:inherit}
.aform textarea{min-height:84px;resize:vertical}
.aform .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:640px){.aform .row{grid-template-columns:1fr}}
.aform .btn{margin-top:16px;width:100%;border:0;cursor:pointer;font-size:17px}
.aform .err{color:#b30f1a;font-weight:700;margin-top:10px;font-size:14px}
.aform .okmsg{color:#0b3d2e;font-weight:700;margin-top:10px;font-size:15px}
.aform small{color:#8a958f;font-size:12.5px;display:block;margin-top:10px}
"""
assert '</style>' in h
h = h.replace('</style>', form_css + '</style>', 1)

# 2. add form modal markup before the school modal
form_html = """
<div class="modal" id="addModal" onclick="if(event.target===this)closeAdd()">
  <div class="sheet">
    <form class="aform" id="addForm" onsubmit="submitSchool(event)">
      <h3>List your school on SomaWest</h3>
      <div class="sub">Fill this form and your school enters our review system. We verify the details, then it goes live on the platform. Listing is free at launch.</div>
      <label>School name *</label>
      <input name="schoolName" required maxlength="120" placeholder="e.g. Tooro High School">
      <label>District *</label>
      <select name="district" required>
        <option value="">Select district</option>
        <option>Bushenyi</option><option>Bundibugyo</option><option>Ibanda</option>
        <option>Kabarole</option><option>Kamwenge</option><option>Kasese</option>
        <option>Kiruhura</option><option>Kyenjojo</option><option>Mbarara</option>
        <option>Mitooma</option><option>Ntoroko</option><option>Ntungamo</option>
        <option>Rubirizi</option><option>Sheema</option><option>Other (Western Uganda)</option>
      </select>
      <div class="row">
        <div>
          <label>Town / location</label>
          <input name="location" maxlength="120" placeholder="e.g. 2 km off Kyenjojo road">
        </div>
        <div>
          <label>Founded (year)</label>
          <input name="founded" maxlength="10" inputmode="numeric" placeholder="e.g. 1998">
        </div>
      </div>
      <div class="row">
        <div>
          <label>Students</label>
          <select name="gender">
            <option value="">Select</option><option>Boys</option><option>Girls</option><option>Mixed</option>
          </select>
        </div>
        <div>
          <label>Housing</label>
          <select name="boarding">
            <option value="">Select</option><option>Boarding</option><option>Day</option><option>Day &amp; Boarding</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div>
          <label>Level</label>
          <select name="level">
            <option value="">Select</option><option>O level (S.1–S.4)</option><option>O &amp; A level</option><option>A level only</option>
          </select>
        </div>
        <div>
          <label>Fees info (optional)</label>
          <input name="fees" maxlength="200" placeholder="e.g. from UGX 350,000 per term">
        </div>
      </div>
      <label>Contact person</label>
      <input name="submittedBy" maxlength="120" placeholder="Name of head teacher / bursar / owner">
      <div class="row">
        <div>
          <label>Phone *</label>
          <input name="phone" required maxlength="25" inputmode="tel" placeholder="+256 7xx xxx xxx">
        </div>
        <div>
          <label>Email</label>
          <input name="email" type="email" maxlength="120" placeholder="school@email.com">
        </div>
      </div>
      <label>About the school</label>
      <textarea name="description" maxlength="1000" placeholder="Short description: what your school offers, achievements, facilities..."></textarea>
      <div class="err" id="addErr" hidden></div>
      <div class="okmsg" id="addOk" hidden></div>
      <button class="btn g" type="submit" id="addBtn">Submit school</button>
      <small>By submitting you confirm these details are correct to the best of your knowledge. SomaWest reviews every listing before it goes live.</small>
    </form>
  </div>
</div>

"""
anchor = '<div class="modal" id="modal"'
assert anchor in h
h = h.replace(anchor, form_html + anchor, 1)

# 3. header + list section buttons open the form
old_header_btn = '<a class="btn g" href="#list" style="padding:10px 16px">Add your school</a>'
assert old_header_btn in h
h = h.replace(old_header_btn, '<button class="btn g" onclick="openAdd()" style="padding:10px 16px">Add your school</button>')

old_list_btn = '<a class="btn" href="https://wa.me/256772002326?text=Hello%20SomaWest%2C%20I%20would%20like%20to%20list%20my%20school%20on%20the%20platform." target="_blank" rel="noopener">List your school</a>'
assert old_list_btn in h
h = h.replace(old_list_btn, '<button class="btn" onclick="openAdd()">Fill the listing form</button>')

# 4. form JS
form_js = """
function openAdd(){ document.getElementById('addModal').classList.add('open'); document.body.style.overflow='hidden'; }
function closeAdd(){ document.getElementById('addModal').classList.remove('open'); document.body.style.overflow=''; }
async function submitSchool(e){
  e.preventDefault();
  const f = e.target;
  const btn = document.getElementById('addBtn');
  const err = document.getElementById('addErr');
  const ok = document.getElementById('addOk');
  err.hidden = true; ok.hidden = true;
  const data = Object.fromEntries(new FormData(f).entries());
  btn.disabled = true; btn.textContent = 'Submitting...';
  try {
    const r = await fetch('https://superagent-c4c23880.base44.app/functions/somawestSubmitSchool', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    const j = await r.json().catch(() => ({}));
    if (r.ok && j.ok) {
      f.reset();
      ok.textContent = 'Thank you! Your school has been added to our review system. Our team verifies the details, then it appears on SomaWest. We may call you on the number provided.';
      ok.hidden = false;
      btn.textContent = 'Submit another school';
    } else {
      err.textContent = (j && j.error) ? j.error : 'Could not submit right now. Please try again.';
      err.hidden = false;
      btn.textContent = 'Submit school';
    }
  } catch (ex) {
    err.textContent = 'No connection. Please try again, or WhatsApp us on +256 772 002 326.';
    err.hidden = false;
    btn.textContent = 'Submit school';
  }
  btn.disabled = false;
}
"""
# insert before the closing script tag at end
h = h.rstrip()
assert h.endswith('</script>')
h = h[:-len('</script>')] + form_js + '\n</script>'

open('index.html','w').write(h)
print('all patches applied')
