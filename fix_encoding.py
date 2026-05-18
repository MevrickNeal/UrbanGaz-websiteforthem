import sys
sys.stdout.reconfigure(encoding='utf-8')

def fix_mojibake(s):
    result = bytearray()
    for c in s:
        o = ord(c)
        if o > 127:
            try:
                result.extend(c.encode('windows-1252'))
            except Exception:
                result.extend(c.encode('utf-8'))
        else:
            result.append(o)
    return result.decode('utf-8', errors='replace')

BENGALI_GAS = '\u0997\u09cd\u09af\u09be\u09b8'  # গ্যাস

with open(r'C:\Users\Lian Mollick\Desktop\CreditCardFraudRnD-main\frontend\index_backup.html', 'rb') as f:
    raw = f.read()

if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]

t = raw.decode('utf-8')
print('Initial Bengali:', BENGALI_GAS in t)

prev = t
for i in range(6):
    t2 = fix_mojibake(prev)
    found = BENGALI_GAS in t2
    print(f'Round {i+1}: found={found}')
    if found:
        prev = t2
        break
    prev = t2

print('FINAL h1 sample:', prev[prev.find('<h1'):prev.find('<h1')+80])

with open(r'C:\Users\Lian Mollick\Desktop\CreditCardFraudRnD-main\frontend\index.html', 'wb') as f:
    f.write(prev.encode('utf-8'))

print('Done.')
