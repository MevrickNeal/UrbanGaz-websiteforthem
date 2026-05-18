import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_content = []
in_app_section = False
for i, line in enumerate(lines):
    if '<div class="app-visual reveal">' in line and i == 92:
        new_content.append('      <section id="app" style="margin-top: 80px; margin-bottom: 80px;">\n')
        new_content.append('        <div class="container">\n')
        new_content.append('          <div class="app-layout">\n')
        new_content.append('            <div class="app-visual reveal">\n')
        in_app_section = True
    elif in_app_section and '<div class="app-info reveal" data-delay="150">' in line:
        new_content.append('            <div class="app-info reveal" data-delay="150" style="text-align: justify;">\n')
    elif in_app_section and '<h2>Pay Your Bill<br>' in line:
        new_content.append('              <h2 style="text-align: left;">Pay Your Bill<br><span class="highlight">Anytime, Anywhere</span></h2>\n')
    elif in_app_section and '<strong>Reading Collection</strong>' in line:
        new_content.append('              <strong style="text-align: left; display: block;">Reading Collection</strong>\n')
    elif in_app_section and '<strong>Bill Generation</strong>' in line:
        new_content.append('              <strong style="text-align: left; display: block;">Bill Generation</strong>\n')
    elif in_app_section and '<strong>SMS &amp; Portal Notification</strong>' in line:
        new_content.append('              <strong style="text-align: left; display: block;">SMS &amp; Portal Notification</strong>\n')
    elif in_app_section and '<strong>Payment Gateway</strong>' in line:
        new_content.append('              <strong style="text-align: left; display: block;">Payment Gateway</strong>\n')
    elif in_app_section and '<div class="app-trust-row">' in line:
        new_content.append('              <div class="app-trust-row" style="justify-content: flex-start;">\n')
    elif in_app_section and '      </div>' in line and i == 149:
        new_content.append(line)
        new_content.append('          </div>\n')
        new_content.append('        </div>\n')
        new_content.append('      </section>\n')
        in_app_section = False
    else:
        new_content.append(line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_content)
