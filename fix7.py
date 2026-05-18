# -*- coding: utf-8 -*-
"""Fix step image assignments + step titles/descriptions + all remaining garbled text."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'rb') as f:
    html = f.read().decode('utf-8')

# ── 1. Fix the entire workflow-timeline section ───────────────────────────────
# Replace whole section with correct content
OLD_WORKFLOW = re.search(
    r'<div class="workflow-timeline">.*?</div>\s*</div>\s*</div>\s*</section>',
    html, flags=re.DOTALL
)

NEW_WORKFLOW = '''<div class="workflow-timeline">

      <div class="wt-item reveal" data-delay="0">
        <div class="wt-marker"><span>01</span></div>
        <div class="wt-line"></div>
        <div class="wt-body glass">
          <div class="wt-row">
            <img src="1765723874208.jpeg" alt="Initial Contact" class="wt-img">
            <div class="wt-text">
              <h4>প্রাথমিক যোগাযোগ</h4>
              <p class="wt-sub">Initial Contact</p>
              <p>যেকোন বাড়ি মালিক / ফ্ল্যাট মালিক সমিতি যোগাযোগ করুন আমাদের সাথে — ফোন, Facebook পেইজ বা ওয়েবসাইটে। Our team will arrange an initial consultation and site visit date.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="wt-item reveal" data-delay="100">
        <div class="wt-marker"><span>02</span></div>
        <div class="wt-line"></div>
        <div class="wt-body glass">
          <div class="wt-row">
            <img src="1765723874683.jpeg" alt="Site Survey" class="wt-img">
            <div class="wt-text">
              <h4>মূল্যায়ন ও যাচাইকরণ</h4>
              <p class="wt-sub">Site Survey &amp; Feasibility</p>
              <p>আমাদের ইঞ্জিনিয়ার দল আপনার প্রাঙ্গণে পেশাদার মূল্যায়ন করেন। Technical team evaluates the pipeline grid for safety, pressure capacity, and smart-meter readiness.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="wt-item reveal" data-delay="200">
        <div class="wt-marker"><span>03</span></div>
        <div class="wt-line"></div>
        <div class="wt-body glass">
          <div class="wt-row">
            <img src="1765723874223.jpeg" alt="Full Installation" class="wt-img">
            <div class="wt-text">
              <h4>সেবা সক্রিয়করণ</h4>
              <p class="wt-sub">Full Installation &amp; Activation</p>
              <p>পাইপলাইন স্থাপন, মিটার সংযোগ এবং ডিজিটাল প্রোফাইল তৈরি করা হয়। Live pipe and multi-meter grid installed. Digital profile creation and grid connection activated.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="wt-item reveal" data-delay="300">
        <div class="wt-marker last"><span>04</span></div>
        <div class="wt-line"></div>
        <div class="wt-body glass">
          <div class="wt-row">
            <img src="1765723868520.jpeg" alt="Full Service Active" class="wt-img">
            <div class="wt-text">
              <h4>পূর্ণাঙ্গ সেবা</h4>
              <p class="wt-sub">Service Acceptance &amp; Sign-off</p>
              <p>আমাদের টিম চূড়ান্ত পরিদর্শন করে। আপনি সংযোগ পরীক্ষা করেন এবং আনুষ্ঠানিকভাবে সেবা গ্রহণ করেন। Our team conducts final inspection — you verify and formally sign off the connection before go-live.</p>
            </div>
          </div>
        </div>
      </div>



    </div>
  </div>
</div>
</section>'''

if OLD_WORKFLOW:
    html = html[:OLD_WORKFLOW.start()] + NEW_WORKFLOW + html[OLD_WORKFLOW.end():]
    print('Workflow section replaced.')
else:
    print('WARNING: Could not find workflow section!')

# ── 2. Final sweep: all remaining ‚¬" and variants ───────────────────────────
sweep = [
    ('\u201a\u00ac\u201d', '\u2014'),   # ‚¬" -> —
    ('\u20ac\u201d',       '\u25cf'),   # €" -> ●
    ('\u00e2\u201e\u00a2', '\u2699\ufe0f'), # â„¢ -> ⚙️
    ('\u2014\u0153',       ' \u2192 '), # —œ -> →
    ('\u2014œ',            ' \u2192 '),
]
for bad, good in sweep:
    n = html.count(bad)
    if n:
        html = html.replace(bad, good)
        print(f'{n}x {repr(bad[:15])} -> {repr(good)}')

# ── 3. Fix BERC notice garbled block ─────────────────────────────────────────
html = re.sub(
    r'(<div class="berc-notice"[^>]*>).*?(</div>)',
    r'''\g<1>
  <div class="berc-inner">
    <span class="berc-icon">📋</span>
    <span class="berc-text"><strong>BERC Verified</strong> — LPG Cylinder 45kg: <strong>BDT 4,898</strong> &nbsp;·&nbsp; Effective 1 May 2026</span>
    <a href="https://berc.org.bd" target="_blank" class="berc-link">View Official Order →</a>
  </div>
\g<2>''',
    html, flags=re.DOTALL
)

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print('Saved. All fixes applied.')
