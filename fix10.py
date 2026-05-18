# -*- coding: utf-8 -*-
"""Insert missing FEATURES and APP SHOWCASE sections into current HTML."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

FEATURES_AND_APP = '''
<!-- FEATURES -->
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
        <p>MAESTRO monitors the active manifold bank\u2019s LPG pressure. On detecting a pressure drop, it instantly activates the reserve manifold \u2014 guaranteeing uninterrupted gas supply without any manual intervention.</p>
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

<!-- APP SHOWCASE -->
<section id="app">
  <div class="container">
    <div class="app-layout">
      <!-- Phone mockup -->
      <div class="app-visual reveal">
        <div class="app-phone-wrap">
          <div class="app-phone-glow"></div>
          <img src="app_mockup.png" alt="Urban Gaz Smart Billing App" class="app-phone-img">
        </div>
        <div class="app-pay-badges">
          <span class="pay-badge">bKash</span>
          <span class="pay-badge">Nagad</span>
          <span class="pay-badge">Visa / MC</span>
          <span class="pay-badge">Bank Transfer</span>
        </div>
      </div>
      <!-- App content -->
      <div class="app-content reveal" data-delay="100">
        <p class="eyebrow">Resident Portal</p>
        <h2>Your Gas Bill, <span class="highlight">Your Phone</span></h2>
        <p class="app-desc">Monthly bills at government-approved BERC rates. Our team collects the meter reading each month and uploads it to the system \u2014 with full payment gateway support for bKash, Nagad, card, and bank transfer.</p>
        <div class="app-trust-row">
          <span class="trust-badge">\u2713 BERC Regulated Rates</span>
          <span class="trust-badge">\u2713 SSL Secured Portal</span>
          <span class="trust-badge">\u2713 Instant SMS Receipts</span>
        </div>
        <div class="app-steps">
          <div class="app-step">
            <div class="app-step-num">01</div>
            <div class="app-step-text">
              <strong>Reading Collection</strong>
              <span>UGL team visits monthly to collect meter readings</span>
            </div>
          </div>
          <div class="app-step">
            <div class="app-step-num">02</div>
            <div class="app-step-text">
              <strong>Bill Generated</strong>
              <span>System calculates your bill at official BERC rates</span>
            </div>
          </div>
          <div class="app-step">
            <div class="app-step-num">03</div>
            <div class="app-step-text">
              <strong>SMS &amp; Portal Notification</strong>
              <span>You receive your bill via SMS and the portal</span>
            </div>
          </div>
          <div class="app-step">
            <div class="app-step-num">04</div>
            <div class="app-step-text">
              <strong>Pay Anywhere</strong>
              <span>bKash, Nagad, card or bank transfer \u2014 your choice</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

'''

# Insert before <section id="coverage">
if 'id="coverage"' in html:
    html = html.replace('<section id="coverage">', FEATURES_AND_APP + '<section id="coverage">', 1)
    print('Features + App sections inserted before coverage.')
else:
    print('ERROR: coverage section not found!')

# Fix MAESTRO em-dash
html = re.sub(r'reserve manifold bank [^\w\u0900-\u09FF\u2014]+ensuring zero', 'reserve manifold bank \u2014 ensuring zero', html)

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

# Final verification
with open('index.html', 'rb') as f:
    c = f.read().decode('utf-8')

sections = ['features', 'app', 'coverage', 'product', 'ceo', 'workflow', 'installation', 'contact']
print('\n--- SECTIONS ---')
for s in sections:
    print(f'  {s}: {"OK" if f"id=\"{s}\"" in c else "MISSING"}')
print('Smart Billing:', 'Smart Billing App' in c)
print('App desc clean:', 'government-approved BERC rates' in c)
print('Step 4 image:', '1765723868520.jpeg' in c)
print('Total chars:', len(c))
