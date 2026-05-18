# -*- coding: utf-8 -*-
import re

with open(r'index_backup.html', 'rb') as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
html = raw.decode('utf-8')

# Each replacement: (garbled_pattern, correct_text)
# We match on distinctive surrounding ASCII to avoid false positives
fixes = [
    # Hero h1
    (r'<h1>[^<]*?<br>', '<h1>গ্যাস নিয়ে আর<br>'),
    (r'<span class="highlight">[^<]*?টেনশন[^<]*?</span></h1>', '<span class="highlight">কোনো টেনশন নেই!</span></h1>'),
    # Hero badge
    (r'IoT-Connected [^<·\n]*?·[^<·\n]*?·[^<\n]*?Monitoring', 'IoT-Connected · GSM-Powered · 24/7 Supply Assurance'),
    # Eyebrow workflow
    (r'<p class="eyebrow">[^<]*?[^\x00-\x7F]+[^<]*?</p>\s*<h2>Professional', '<p class="eyebrow">সেবা গ্রহণ প্রক্রিয়া</p>\n    <h2>Professional'),
    # Step 1
    (r'<h4>[^<]*?[^\x00-\x7F]+[^<]*?</h4>\s*<p class="wt-sub">Initial Contact', '<h4>প্রাথমিক যোগাযোগ</h4>\n              <p class="wt-sub">Initial Contact'),
    (r'(<p class="wt-sub">Initial Contact</p>\s*<p>)[^<]*?[^\x00-\x7F]+[^<]*?(Our team)', r'\1যেকোন বাড়ি মালিক / ফ্ল্যাট মালিক সমিতি যোগাযোগ করুন আমাদের সাথে — ফোন, Facebook পেইজ বা ওয়েবসাইটে। \2'),
    # Step 2
    (r'<h4>[^<]*?[^\x00-\x7F]+[^<]*?</h4>\s*<p class="wt-sub">Site Survey', '<h4>সাইট সার্ভে</h4>\n              <p class="wt-sub">Site Survey'),
    # Step 3
    (r'<h4>[^<]*?[^\x00-\x7F]+[^<]*?</h4>\s*<p class="wt-sub">Full Installation', '<h4>পূর্ণাঙ্গ সেবা</h4>\n              <p class="wt-sub">Full Installation'),
    (r'(<p class="wt-sub">Full Installation</p>\s*<p>)[^<]*?[^\x00-\x7F]+[^<]*?(Live pipe)', r'\1গ্যাস পৌঁছে দেওয়া, নিয়মিত বিলিং এবং সার্বিক মেইনটেইন্যান্সের প্রো দায়িত্ব এখন আমাদের। \2'),
    # Step 4
    (r'<h4>[^<]*?[^\x00-\x7F]+[^<]*?</h4>\s*<p class="wt-sub">Service Acceptance', '<h4>সেবা স্বীকৃতি করুন</h4>\n              <p class="wt-sub">Service Acceptance'),
    (r'(<p class="wt-sub">Service Acceptance[^<]*?</p>\s*<p>)[^<]*?[^\x00-\x7F]+[^<]*?(Our team conducts)', r'\1আমাদের টিম চূড়ান্ত পরিদর্শন করে। আপনি সংযোগ পরীক্ষা করেন এবং আনুষ্ঠানিকভাবে সেবা গ্রহণের অনুমতি দেন। \2'),
    # Installation section
    (r'<p>[^<]*?[^\x00-\x7F]+[^<]*?পাইপলাইন গ্রিড[^<]*?</p>', '<p>প্রতিটি সংযোগ আধুনিক মানের এবং লিকেজ মুক্ত। দক্ষ ইঞ্জিনিয়ারদের সরাসরি তত্ত্বাবধানে পাইপলাইন গ্রিড স্থাপন কাজ।</p>'),
    # CEO section Bengali
    (r'<p>[^<]*?[^\x00-\x7F]+[^<]*?গ্রাহক[^<]*?</p>', '<p>আমাদের পেটেন্ট করা আইওটি সিস্টেম রিয়েল-টাইমে গ্যাসের চাপ পর্যবেক্ষণ করে, যা গ্রাহকদের জন্য ১০০% নিরাপদ এবং নিরবচ্ছিন্ন সেবা নিশ্চিত করে।</p>'),
    # App desc Bengali
    (r'(<p class="app-desc">)[^<]*?[^\x00-\x7F]+[^<]*?(Monthly bills)', r'\1আমাদের স্মার্ট বিলিং পোর্টাল আপনার গ্যাস বিল পরিচালনা সহজ করে দেয়। \2'),
    # Footer copyright
    (r'<p>[^<]*?[^\x00-\x7F]+[^<]*?2026 Urban Gaz', '<p>&copy; 2026 Urban Gaz'),
    # Coverage pills
    (r'<span class="pill active-pill">[^<]*?Dhaka', '<span class="pill active-pill">● Dhaka'),
    (r'<span class="pill expand-pill">[^<]*?Mymensingh', '<span class="pill expand-pill">◐ Mymensingh'),
    # Install badges
    (r'<span class="install-badge">[^<]*?LIVE PIPELINE', '<span class="install-badge">● LIVE PIPELINE'),
    (r'<span class="install-badge">[^<]*?METERED ARRAY', '<span class="install-badge">● METERED ARRAY'),
    # Check marks in install list
    (r'<li>[^<]*?Industrial-grade', '<li>✔ Industrial-grade'),
    (r'<li>[^<]*?Pressure-regulated', '<li>✔ Pressure-regulated'),
    (r'<li>[^<]*?IoT-ready', '<li>✔ IoT-ready'),
    (r'<li>[^<]*?Full leak-test', '<li>✔ Full leak-test'),
    # Contact select options
    (r'<option>[^<]*?Single Flat', '<option>Residential — Single Flat'),
    (r'<option>[^<]*?Building</option>', '<option>Residential — Building</option>'),
    # Submit button arrow
    (r'Submit Request [^<]*?</button>', 'Submit Request &rarr;</button>'),
    # Admin modal note
    (r'Operations Hub V8\.0 [^<]*?Authorized', 'Operations Hub V8.0 · Authorized'),
    # Meta description
    (r'(<meta name="description" content="Urban Gaz Limited )[^"]*(")', r'\1— Smart IoT gas distribution, expert engineering teams. Serving Dhaka & Mymensingh.\2'),
    # Hero badge remove garbled
    (r'IoT-Connected [^<\n]*?24/7[^<\n]*?(?=\s*</div>)', 'IoT-Connected · GSM-Powered · 24/7 Supply Assurance'),
]

count = 0
for pattern, replacement in fixes:
    new_html, n = re.subn(pattern, replacement, html, flags=re.DOTALL)
    if n:
        html = new_html
        count += n
        print(f'Fixed {n}x: {pattern[:50]}')

# Also remove any remaining garbled multi-byte sequences next to known good text
# Replace any run of garbled chars (non-ASCII high chars that look like Windows-1252 artifacts)
# Pattern: Ã followed by more Ã/Â sequences
html = re.sub(r'[ÃÂ]{1,2}[\x80-\xBF\u00A0-\u00FF]{1,3}(?:[ÃÂ][\x80-\xBF\u00A0-\u00FF]{1,3})*', '', html)

with open(r'index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print(f'\nTotal fixes: {count}')
print('Saved index.html')
