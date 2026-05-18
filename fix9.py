# -*- coding: utf-8 -*-
"""Definitive fix: rebuild features section + fix last 2 garbled em-dashes."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

FEATURES_SECTION = '''<!-- \u2022\u2022\u2022 FEATURES \u2022\u2022\u2022 -->
<section id="features">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Core Capabilities</p>
      <h2>Patented IoT <span class="highlight">Integration</span></h2>
      <p class="section-sub">Our patented MAESTRO Switchover Device continuously monitors your active LPG manifold bank. The moment pressure drops, it automatically switches to the reserve manifold &mdash; ensuring zero interruption to gas supply across every flat in the building, 24 hours a day.</p>
    </div>
    <div class="features-grid">

      <div class="feat-card glass reveal" data-delay="0">
        <div class="feat-icon" style="background: rgba(232,78,27,0.1)">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M4 20l6-8 5 4 5-10 4 6" stroke="#E84E1B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="8" r="3" fill="#E84E1B" opacity=".3"/></svg>
        </div>
        <h3>Pressure-Sensing Switchover</h3>
        <p>MAESTRO continuously monitors the active manifold bank\u2019s LPG pressure. On detecting a pressure drop, it instantly activates the reserve manifold \u2014 guaranteeing uninterrupted gas supply to all residents without any manual intervention.</p>
        <div class="feat-chip">Auto Switchover</div>
      </div>

      <div class="feat-card glass reveal" data-delay="150">
        <div class="feat-icon" style="background: rgba(245,166,35,0.1)">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M14 3l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" stroke="#F5A623" stroke-width="2" stroke-linejoin="round"/></svg>
        </div>
        <h3>Smart Billing App</h3>
        <p>Monthly bills at government-approved BERC rates, delivered to your phone via SMS and the resident portal. Pay via bKash, Nagad, card or bank transfer.</p>
        <div class="feat-chip" style="background:rgba(245,166,35,0.1);color:#c8860a">Billing</div>
      </div>

      <div class="feat-card glass reveal" data-delay="200">
        <div class="feat-icon" style="background: rgba(232,78,27,0.1)">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M14 4C8.477 4 4 8.477 4 14s4.477 10 10 10 10-4.477 10-10S19.523 4 14 4z" stroke="#E84E1B" stroke-width="2"/><path d="M14 4s-4 4-4 10 4 10 4 10M14 4s4 4 4 10-4 10-4 10M4 14h20" stroke="#E84E1B" stroke-width="2"/></svg>
        </div>
        <h3>Cloud Connected</h3>
        <p>Real-time data synced to our cloud infrastructure. Accessible via your resident portal or the UGL mobile app anytime, anywhere.</p>
        <div class="feat-chip">Cloud</div>
      </div>

      <div class="feat-card glass reveal" data-delay="250">
        <div class="feat-icon" style="background: rgba(30,110,140,0.1)">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="3" y="3" width="9" height="9" rx="1.5" stroke="#1E6E8C" stroke-width="2"/><rect x="16" y="3" width="9" height="9" rx="1.5" stroke="#1E6E8C" stroke-width="2"/><rect x="3" y="16" width="9" height="9" rx="1.5" stroke="#1E6E8C" stroke-width="2"/><rect x="16" y="16" width="9" height="9" rx="1.5" stroke="#1E6E8C" stroke-width="2"/></svg>
        </div>
        <h3>Multi-Zone Management</h3>
        <p>Manage multiple buildings, franchises, and flat units from one dashboard. Hierarchical access for district managers, engineers, and billing staff.</p>
        <div class="feat-chip" style="background:rgba(30,110,140,0.1);color:#1E6E8C">Management</div>
      </div>

    </div>
  </div>
</section>

'''

# Insert features section before <section id="app">
if 'id="features"' not in html:
    html = re.sub(r'(<section id="app">)', FEATURES_SECTION + r'\1', html)
    print('Features section inserted.')
else:
    print('Features section already present.')

# Fix App showcase em-dash
html = re.sub(r'delivered to your phone [^\w]+with full payment', 'delivered to your phone \u2014 with full payment', html)

# Fix MAESTRO em-dash in product section
html = re.sub(r'reserve manifold bank [^\w]+ensuring zero', 'reserve manifold bank \u2014 ensuring zero', html)

# Final sweep: any remaining ‚¬"
n = html.count('\u201a\u00ac\u201d')
if n:
    html = html.replace('\u201a\u00ac\u201d', '\u2014')
    print(f'{n}x ‚¬" -> —')

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

# Final checks
with open('index.html', 'rb') as f:
    c = f.read().decode('utf-8')

checks = [
    ('Features section',    'id="features"'),
    ('Smart Billing card',  'Smart Billing App'),
    ('Billing text',        'government-approved BERC rates'),
    ('App section',         'id="app"'),
    ('MAESTRO section',     'id="product"'),
    ('Workflow section',    'id="workflow"'),
    ('Step 4 image',        '1765723868520.jpeg'),
    ('Contact section',     'id="contact"'),
    ('Footer',              '<footer>'),
]
print('\n--- VERIFICATION ---')
all_ok = True
for name, key in checks:
    ok = key in c
    print(f'  {name}: {"OK" if ok else "MISSING"}')
    if not ok: all_ok = False
print('\nOverall:', 'PASS' if all_ok else 'FAIL')
