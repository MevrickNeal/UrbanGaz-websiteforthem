# -*- coding: utf-8 -*-
"""Final clean-up: direct byte-level string replacements on index.html"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    raw = f.read().decode('utf-8')

html = raw

# ── EXACT string replacements (copy-paste from view_file output) ──────────────

replacements = [
    # Hero h1 second line (garbled span content)
    ('•₹€¹   €¡â€¡!', 'কোনো টেনশন নেই!'),
    # Step 3 wrong word
    ('প্রো দায়িত্ব', 'পুরো দায়িত্ব'),
    # Any remaining â€" → —
    ('â€"', '\u2014'),
    ('â€\x93', '\u2013'),
    # ‚¬â€ sequences (garbled em-dash variant)
    ('‚¬â€\x9d', '"'),
    ('‚¬â€\x9c', '"'),
    ('‚¬â€\x99', "'"),
    ('‚¬â€\x94', '\u2014'),
    ('‚¬â€\x93', '\u2013'),
    ('‚¬â€\x98', "'"),
    ('‚¬â€', '\u2014'),
    # CEO middot garbled (Ã‚ before ·)
    ('Ã‚·', '·'),
    ('Ã,·', '·'),
    # Degree sign
    ('Ã‚°', '°'),
    ('Ã,°', '°'),
    # Ã‚ by itself (spurious)
    ('Ã‚', ''),
    ('Ã,', ''),
    # ,-â€" sequences (CEO timeline)
    (',â€"', ' —'),
    (',â€\x94', ' —'),
    (',-â€"', ' —'),
    # Bullet/arrow garbled
    ('â€¢', '•'),
    ('â€º', '›'),
    ('â€¹', '‹'),
    # Left/right quotes
    ('â€œ', '"'),
    ('â€\x9d', '"'),
    ('â€˜', "'"),
    ('â€™', "'"),
    # Installation Bengali paragraph — replace the whole garbled block
    ('€š€¹â€" â€ â€¢ €¡ â€š â€¢â€¡Å" â€¢ €¢ â€¡Å¾"â€¡  €¡ â€¡€¡ â€"  â€¢"',
     'প্রতিটি সংযোগ আধুনিক মানের এবং লিকেজ মুক্ত।'),
    # Smart billing card Bengali title garble
    ('€š Å¡€¡ â€• Smart Billing', 'Smart Billing App'),
    ('€š Å¡€¡ â€" Smart Billing', 'Smart Billing App'),
    # Smart billing card Bengali description garble (the long block)
    ('â€¦Å¸â€¹€¹ Å¸ â€š  â€¡ â€"â€¢  €¡ €¹€¡  €¡ â€•  €š€¡ €º â€š', ''),
    # BERC ticker Bengali garble
    ('€š ,¬â€  €¡', ''),
    ('â€œâ€œ LPG €š ,¬â€  €¡', 'LPG'),
    # BERC badge garble
    ('€¡  ‚¬â€  â€¢  â€¢\'â€¢  LPG â€"â€¡ €š â€   â€¢ €¡ â€¦â‚¬ €š  â€¢', 'LPG Price — May 2026'),
    # Spec table dashes
    ('Coloured TFT ,¬â€  Instant Status', 'Coloured TFT — Instant Status'),
    ('OLED ,¬â€  Compact Principal Output', 'OLED — Compact Principal Output'),
    # CEO education separator
    (',-â€Ξ', ' — '),
    (',-â€', ' — '),
    (' ,â€"', ' — '),
    # Stray € and residual
    ('€¡', ''),
    ('€š', ''),
    ('€¹', ''),
    ('€¢', ''),
    ('€º', ''),
    ('Å¸', ''),
    ('Å¡', ''),
    ('Å"', ''),
    ('Å¾', ''),
    ('â€ ', ''),
    ('â€¦', '…'),
    ('â€', '"'),
]

count = 0
for bad, good in replacements:
    if bad in html:
        n = html.count(bad)
        html = html.replace(bad, good)
        print(f'  {n}x: {repr(bad[:30])} => {repr(good[:20])}')
        count += n

# Step 4 wt-line fix
html = html.replace('<div class="wt-line" style="display:none">', '<div class="wt-line">')

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print(f'\nTotal replacements: {count}')
print('index.html saved.')
