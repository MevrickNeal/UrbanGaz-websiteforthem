# -*- coding: utf-8 -*-
"""Fix garbled characters using exact browser-visible strings as keys."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    raw = f.read()

# The file is UTF-8; read it as UTF-8
html = raw.decode('utf-8')

# ── Exact replacements based on what the browser renders ─────────────────────
# Pattern -> Correct text
fixes = [
    # em-dash variants (‚¬" is how — looks when double-mojibaked)
    ('\u201a\u00ac\u201d',          '\u2014'),   # ‚¬" -> —
    ('\u201a\u00ac\u2013',          '\u2013'),   # ‚¬" -> –  (en-dash variant)
    # Bullet circle  €" -> ●
    ('\u20ac\u201d',                '\u25cf'),   # €" -> ●
    # Gear symbol â„¢ -> ⚙
    ('\u00e2\u201e\u00a2',          '\u2699'),   # â„¢ -> ⚙
    # Career timeline arrows —œ -> →
    ('\u2014\u0153',                ' \u2192 '), # —œ -> →
    ('\u2014œ',                     ' \u2192 '),
    # Opening quote " alone -> "
    ('\u201c\n',                    '\u201c\n'),  # no-op if correct
    # BERC notice garbled block — replace entirely
    ('\u201a\u00ac\u201d \u2022 \u2022\u2019\u2022 LPG \u201c\u201d\u00e2 \u201c  \u2022 \u2026\u00e2\u201a\u00ac \u2022',
     'LPG \u2014 45kg Cylinder \u2014 BDT 4,898'),
    # Smart billing card garbled prefix  …₹ ""•
    ('\u2026\u20b9 \u201c\u201d\u2022 \u2022 ',  ''),
    # Spec table dashes
    ('TFT \u201a\u00ac\u201d Instant Status',     'TFT \u2014 Instant Status'),
    ('OLED \u201a\u00ac\u201d Compact',            'OLED \u2014 Compact'),
    # CEO name dash
    ('Khairul Alam \u201a\u00ac\u201d Founder',   'Khairul Alam \u2014 Founder'),
    ('KUET \u201a\u00ac\u201d BSc',               'KUET \u2014 BSc EEE, 2015'),
    ('CEO \u201a\u00ac\u201d Urban Gaz',          'CEO \u2014 Urban Gaz'),
    # Career history dashes
    ('Sales \u201a\u00ac\u201d Promita',          'Sales \u2014 Promita'),
    ('Gas Ltd\n',                                 'Gas Ltd\n'),
    # The quote char before the CEO quote
    ('\u201c\nFour years',                        '\u201c\nFour years'),
    # idea ‚¬" to solve
    ('idea \u201a\u00ac\u201d to solve',          'idea \u2014 to solve'),
    # Urban Gaz ‚¬" not just
    ('Urban Gaz \u201a\u00ac\u201d not just',     'Urban Gaz \u2014 not just'),
    # Apr 2019 —œ Dec 2021
    ('Apr 2019 \u2014\u0153 Dec',                 'Apr 2019 \u2192 Dec'),
    ('Jul 2023 \u2014\u0153 Present',             'Jul 2023 \u2192 Present'),
    ('Dec 2015 \u2014\u0153 Mar',                 'Dec 2015 \u2192 Mar'),
    # View Official BERC Order ‚¬" May 2026
    ('View Official BERC Order \u201a\u00ac\u201d May 2026',
     'View Official BERC Order \u2014 May 2026'),
    # ° degree sign garbled
    ('-30C to +70C',                              '-30\u00b0C to +70\u00b0C'),
    # Engineer Support gear icon garbled
    ('\u00e2\u201e\u00a2 24/7',                   '\u2699\ufe0f 24/7'),
    # Coverage pills € prefix
    ('\u20ac\u201d Live',                         '\u25cf Live'),
    ('\u20ac\u201d In Progress',                  '\u25cf In Progress'),
]

count = 0
for bad, good in fixes:
    if bad in html and bad != good:
        n = html.count(bad)
        html = html.replace(bad, good)
        print(f'  {n}x: {repr(bad[:35])} -> {repr(good[:25])}')
        count += n

# ── Also nuke any remaining ‚¬" sequences (all are em-dashes) ───────────────
import re
# This pattern matches the 3-char sequence ‚¬" wherever it appears
remaining = html.count('\u201a\u00ac\u201d')
if remaining:
    html = html.replace('\u201a\u00ac\u201d', '\u2014')
    print(f'  {remaining}x: remaining ‚¬" -> —')
    count += remaining

# Fix any remaining €" sequences (all are ●)
remaining2 = html.count('\u20ac\u201d')
if remaining2:
    html = html.replace('\u20ac\u201d', '\u25cf')
    print(f'  {remaining2}x: remaining €" -> ●')
    count += remaining2

# Fix remaining —œ (timeline arrow)
remaining3 = html.count('\u2014\u0153')
if remaining3:
    html = html.replace('\u2014\u0153', ' \u2192 ')
    print(f'  {remaining3}x: remaining —œ -> →')
    count += remaining3

# Fix â„¢ (gear)
remaining4 = html.count('\u00e2\u201e\u00a2')
if remaining4:
    html = html.replace('\u00e2\u201e\u00a2', '\u2699\ufe0f')
    print(f'  {remaining4}x: remaining â„¢ -> ⚙')
    count += remaining4

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print(f'\nTotal: {count} replacements. Saved.')
