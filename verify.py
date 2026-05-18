# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    t = f.read().decode('utf-8')

checks = [
    ('h1 Bengali', '\u0997\u09cd\u09af\u09be\u09b8'),
    ('Step1 header', '\u09aa\u09cd\u09b0\u09be\u09a5\u09ae\u09bf\u0995'),
    ('Seba word', '\u09b8\u09c7\u09ac\u09be'),
    ('App desc', '\u09b8\u09cd\u09ae\u09be\u09b0\u09cd\u099f'),
    ('Coverage pills', 'Dhaka (Active)'),
    ('Checkmarks', '\u2714'),
    ('Footer year', '2026 Urban Gaz'),
    ('Admin modal', 'Admin Access'),
    ('Contact form', 'Request a Connection'),
    ('MAESTRO product', 'MAESTRO'),
]

all_ok = True
for name, word in checks:
    status = 'OK' if word in t else 'MISSING'
    if status == 'MISSING':
        all_ok = False
    print(name + ': ' + status)

print('')
print('File size: ' + str(len(t)) + ' chars')
print('Overall: ' + ('CLEAN' if all_ok else 'NEEDS MORE FIXES'))
