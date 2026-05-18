# -*- coding: utf-8 -*-
"""Fix all remaining mojibake and UI issues in index.html"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

orig_len = len(html)

# ── 1. Fix common mojibake sequences ─────────────────────────────────────────
mojibake = [
    # em-dash variants
    ('\u00e2\u20ac\u201c', '\u2014'),   # â€" → —
    ('\u00e2\u20ac\u0090', '\u2014'),
    ('\u00e2\u20ac\u009c', '\u201c'),   # â€œ → "
    ('\u00e2\u20ac\u009d', '\u201d'),   # â€ → "
    ('\u00e2\u20ac\u2122', '\u2019'),   # â€™ → '
    ('\u00e2\u20ac\u02dc', '\u2018'),   # â€˜ → '
    ('\u00e2\u20ac\u00a2', '\u2022'),   # â€¢ → •
    ('\u00e2\u20ac\u00b9', '\u20b9'),   # ₹
    # Non-breaking space artifacts
    ('\u00c3\u00a2\u00e2\u201a\u00ac\u00e2\u20ac\u2122', "'"),
    # Degree sign
    ('\u00c3\u201a', ''),              # Ã‚ → remove (spurious byte)
    # Bullet arrow variants
    ('\u00e2\u20ac\u00ba', '\u203a'),
    ('\u00e2\u20ac\u00b9', '\u2039'),
    # Three-quarter em (,â€" sequences seen in CEO section)
    (',\u00c2\u00a0\u00e2\u20ac\u201c', ' — '),
    (' ,-\u00e2\u20ac\u0090', ' — '),
    (' ,-\u00e2\u20ac\u201c', ' — '),
    ('\u00e2\u20ac\u0093', '\u2013'),   # – en-dash
    # Stray Â before symbols
    ('\u00c2\u00b7', '·'),
    ('\u00c2\u00a0', '\u00a0'),
    ('\u00c2\u00b0', '°'),
    ('\u00c2\u00b1', '±'),
    ('\u00c2\u00b3', '³'),
    ('\u00c3\u2026', '…'),
    # Arrow
    ('\u00e2\u2020\u2019', '→'),
    ('\u00e2\u2020\u2014', '←'),
]

for bad, good in mojibake:
    if bad in html:
        count = html.count(bad)
        html = html.replace(bad, good)
        print(f'Replaced {count}x: {repr(bad)} → {repr(good)}')

# ── 2. Targeted text corrections ─────────────────────────────────────────────
text_fixes = [
    # Wrong Bengali word in step 3
    ('প্রো দায়িত্ব', 'পুরো দায়িত্ব'),
    # Smart billing card title — strip garbled prefix, keep clean English
    ('মূল্য যাচাই করুন · Smart Billing', 'Smart Billing App'),
    # App desc em-dash
    # App desc em-dash fix handled by mojibake list above
    # Hero h1 in case still garbled
    ('কোনো টেনশন', 'কোনো টেনশন'),  # no-op if correct
    # BERC ticker — replace any garbled BERC text with clean version
    # Step 4 — fix the body visibility (wt-line display:none → remove it so grid works)
    ('<div class="wt-line" style="display:none"></div>', '<div class="wt-line"></div>'),
    # Spec table degree signs
    ('-30°C to +70°C', '-30°C to +70°C'),  # ensure clean
    ('±0.5%', '±0.5%'),
]

for bad, good in text_fixes:
    if bad in html and bad != good:
        count = html.count(bad)
        html = html.replace(bad, good)
        print(f'Text fix {count}x: {bad[:40]}')

# ── 3. Fix garbled BERC ticker completely ─────────────────────────────────────
html = re.sub(
    r'<div class="price-ticker[^"]*"[^>]*>.*?</div>',
    '''<div class="price-ticker">
  <div class="ticker-track">
    <span>📋 BERC Official Order — May 2026 &nbsp;·&nbsp; 45kg LPG Cylinder: <strong>BDT 4,898</strong> &nbsp;·&nbsp; Effective: 1 May 2026 &nbsp;·&nbsp; Source: bangladesh-energy-regulatory-commission.org &nbsp;·&nbsp; 📋 BERC Official Order — May 2026 &nbsp;·&nbsp; 45kg LPG Cylinder: <strong>BDT 4,898</strong> &nbsp;·&nbsp; Effective: 1 May 2026</span>
  </div>
</div>''',
    html, flags=re.DOTALL
)

# ── 4. Fix Smart Billing feat-card (garbled Bengali + wrong title) ─────────────
html = re.sub(
    r'(<div class="feat-card glass reveal" data-delay="150">.*?<h3>)[^<]*(Smart Billing App|Smart Billing)[^<]*(</h3>)',
    r'\g<1>Smart Billing App\g<3>',
    html, flags=re.DOTALL
)

# Remove garbled Bengali paragraph inside that card (the one with all the ????? chars)
html = re.sub(
    r'(<div class="feat-card glass reveal" data-delay="150">.*?<h3>Smart Billing App</h3>\s*<p>)[^<]*[^\x00-\x7F\u0980-\u09FF]{20,}[^<]*(</p>)',
    r'\g<1>Monthly bills at government-approved BERC rates, delivered to your phone via SMS and Portal.\g<2>',
    html, flags=re.DOTALL
)

# ── 5. Fix CEO section garbled separators ─────────────────────────────────────
html = re.sub(r',\s*-+â€[^<]{0,10}(?=\s)', ' — ', html)
html = re.sub(r',\s*â€[^<]{0,5}(?=\s)', ' — ', html)

# ── 6. Fix any remaining  Ã‚ sequences ────────────────────────────────────────
html = re.sub(r'\u00c3\u201a\u00c2', '', html)
html = re.sub(r'\u00c3\u201a', '', html)

# ── 7. Fix remaining stray UTF-8 artifacts in visible text ────────────────────
# Any sequence of 3+ garbled chars between ASCII words
html = re.sub(r'(?<=[a-zA-Z\s])[^\x00-\x7F\u0980-\u09FF\u2000-\u206F\u00A9\u00AE\u2014\u2013\u00B0\u00B1\u00B7\u2022\u201C\u201D\u2019\u2018\u20B9\u2192\u2190\u00A0]{3,}(?=[a-zA-Z\s])', ' ', html)

# ── 8. Final write ────────────────────────────────────────────────────────────
with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print(f'\nOriginal: {orig_len} | Fixed: {len(html)}')
print('Done.')
