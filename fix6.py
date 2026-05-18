# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

# Fix 1: Installation Bengali paragraph — replace the entire <p> line (line 430)
html = re.sub(
    r'<p>\s*["\u201c\u201d\u2022\u00e2\u00c5\u00e2\u201a\u00ac\u2019\u20ac\u00ba\u2026\u00b9 ]{3,}[^<]*</p>(?=\s*<p class="en-sub">)',
    '<p>প্রতিটি সংযোগ আধুনিক মানের এবং লিকেজ মুক্ত। দক্ষ ইঞ্জিনিয়ারদের সরাসরি তত্ত্বাবধানে পাইপলাইন গ্রিড স্থাপন কাজ।</p>',
    html, flags=re.DOTALL
)

# Fix 2: Clean alt text on step 1 img
html = re.sub(
    r'(<img src="1765723874208\.jpeg" alt=")[^"]*(")',
    r'\g<1>Initial Contact — Step 1\g<2>',
    html
)

# Fix 3: Clean alt text on step 4 img  
html = re.sub(
    r'(<img src="1765723874223\.jpeg" alt=")[^"]*(")',
    r'\g<1>Service Acceptance — Step 4\g<2>',
    html
)

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

# Verify
with open('index.html', 'rb') as f:
    check = f.read().decode('utf-8')

print('Install Bengali:', 'প্রতিটি সংযোগ' in check)
print('Step1 alt clean:', 'Step 1' in check)
print('Step4 alt clean:', 'Step 4' in check)
print('Step3 image:', '1765723874683.jpeg' in check)
print('Done.')
