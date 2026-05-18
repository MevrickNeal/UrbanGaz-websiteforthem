# -*- coding: utf-8 -*-
"""Fix remaining garbled text + restore missing billing card + fix step 4 CSS."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

# ── 1. Restore Smart Billing feat-card if missing ────────────────────────────
if 'Smart Billing App' not in html:
    BILLING_CARD = '''
      <div class="feat-card glass reveal" data-delay="150">
        <div class="feat-icon" style="background: rgba(245,166,35,0.1)">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M14 3l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" stroke="#F5A623" stroke-width="2" stroke-linejoin="round"/></svg>
        </div>
        <h3>Smart Billing App</h3>
        <p>Monthly bills at government-approved BERC rates, delivered to your phone via SMS and the resident portal. Pay via bKash, Nagad, card or bank transfer.</p>
        <div class="feat-chip" style="background:rgba(245,166,35,0.1);color:#c8860a">Billing</div>
      </div>
'''
    # Insert after the Auto Switchover card closing div
    html = html.replace(
        '        <div class="feat-chip">Auto Switchover</div>\n      </div>',
        '        <div class="feat-chip">Auto Switchover</div>\n      </div>\n' + BILLING_CARD
    )
    print('Billing card restored.')
else:
    # Fix garbled prefix in existing card
    html = re.sub(
        r'(<h3>Smart Billing App</h3>\s*<p>)[^<]*(Our system|Monthly bills)',
        r'\g<1>Monthly bills at government-approved BERC rates, delivered to your phone via SMS and the resident portal. Pay via bKash, Nagad, card or bank transfer.</p>\n        <div class="feat-chip" style="background:rgba(245,166,35,0.1);color:#c8860a">Billing</div>\n      </div>\n\n      <div class="feat-card glass reveal" data-delay="150">\n        <div class="feat-icon" style="background: rgba(245,166,35,0.1)">\n          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path d="M14 3l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" stroke="#F5A623" stroke-width="2" stroke-linejoin="round"/></svg>\n        </div>\n        <h3>dummy',
        html, flags=re.DOTALL
    )
    print('Billing card garble fixed.')

# ── 2. Fix App showcase em-dash garble ───────────────────────────────────────
html = re.sub(
    r'delivered to your phone [^w]+with full payment gateway',
    'delivered to your phone \u2014 with full payment gateway',
    html
)

# ── 3. Fix MAESTRO product description em-dash garble ───────────────────────
html = re.sub(
    r'reserve manifold bank [^e]+ensuring zero interruption',
    'reserve manifold bank \u2014 ensuring zero interruption',
    html
)

# ── 4. Fix Step 4 CSS: ensure wt-marker last doesn't hide wt-body ──────────
# The issue might be the wt-row not having enough height for step 4
# Let's check if wt-line for step 4 might be display:none
html = html.replace(
    '<div class="wt-marker last"><span>04</span></div>\n        <div class="wt-line" style="display:none">',
    '<div class="wt-marker last"><span>04</span></div>\n        <div class="wt-line">'
)

# ── 5. Sweep any remaining ‚¬" ───────────────────────────────────────────────
n = html.count('\u201a\u00ac\u201d')
if n:
    html = html.replace('\u201a\u00ac\u201d', '\u2014')
    print(f'{n}x ‚¬" -> —')

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

# Verify
with open('index.html', 'rb') as f:
    check = f.read().decode('utf-8')

print('Smart Billing card:', 'Smart Billing App' in check)
print('Billing text clean:', 'government-approved BERC rates' in check)
print('MAESTRO dash clean:', 'reserve manifold bank \u2014 ensuring' in check)
print('Step 4 image:', '1765723868520.jpeg' in check)
print('Done.')
