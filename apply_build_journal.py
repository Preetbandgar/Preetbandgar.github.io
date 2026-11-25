#!/usr/bin/env python3
"""Surgical update for the existing portfolio (V20 or compatible V19).
Run from repo root: python3 /path/to/apply_build_journal.py
Optional argument: path to repo root. No external dependencies. Does not commit/push.
"""
from pathlib import Path
import re, sys, subprocess, shutil

ROOT = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv)>1 else Path.cwd()
if not (ROOT/'scripts/build_home.py').is_file():
    raise SystemExit('Run this from your current portfolio repository root, or pass its path.')

def read(name):
    return (ROOT/name).read_text(encoding='utf-8')

def require_one(pattern, text, label, flags=0):
    hits=list(re.finditer(pattern,text,flags))
    if len(hits)!=1: raise SystemExit(f'Expected exactly one {label}; found {len(hits)}. No changes written.')
    return hits[0]

# Read and validate first; do not reset, replace or regenerate unrelated pages.
edu_path='_includes/education.html'
physical_path='projects/physical-differential-drive-robot.html'
css_path='assets/portfolio.css'
template_path='_includes/home.template'
edu, physical, css, template = map(read,(edu_path, physical_path, css_path, template_path))
section=require_one(r'<section\b[^>]*class="[^"]*\bcurrent-build-section\b[^"]*"[^>]*>.*?</section>',edu,'Current Build section',re.S)
block=section.group()
if 'class="current-build-heading' not in block:
    old=require_one(r'<div\b[^>]*class="current-build-spacer"[^>]*>\s*</div>',block,'empty Current Build column',re.S)
    left='''<div class="current-build-heading reveal"><span class="eyebrow">CURRENT PROJECT</span><h2 id="current-build-heading">From hardware<br/><em>to autonomy.</em></h2></div>'''
    block=block[:old.start()]+left+block[old.end():]
    block=block.replace('aria-labelledby="current-build-title"','aria-labelledby="current-build-heading"',1)
button=require_one(r'<a\b[^>]*href="projects/physical-differential-drive-robot\.html"[^>]*>.*?</a>',block,'Current Build link',re.S)
block=block[:button.start()]+'''<a class="button button--amber" href="projects/physical-differential-drive-robot.html">See build progress <span aria-hidden="true">↗</span></a>'''+block[button.end():]
edu_new=edu[:section.start()]+block+edu[section.end():]

# Preserve the complete November record as a dated snapshot. Future entries go above it.
marker='<!-- ROBOT JOURNAL ENTRIES: newest first -->'
current_pdf=ROOT/'assets/docs/Physical_Robot_Component_Inventory_Public.pdf'
snapshot=ROOT/'assets/docs/robot-journal/2026-11-component-inventory.pdf'
new_snapshot=False
if marker not in physical:
    article=require_one(r'(<article\b[^>]*class="[^"]*\bdetail-main\b[^"]*"[^>]*>)(.*?)(</article>)',physical,'robot project article',re.S)
    historical=article.group(2).strip()
    # Keep the historic inventory distinct from the current, editable inventory.
    if not current_pdf.is_file(): raise SystemExit('Current robot inventory PDF missing; cannot preserve a dated snapshot. No changes written.')
    historical=historical.replace('../assets/docs/Physical_Robot_Component_Inventory_Public.pdf','../assets/docs/robot-journal/2026-11-component-inventory.pdf')
    if 'id="build-photos"' not in historical:
        historical=historical.replace('<h2>Photos from the actual build</h2>','<h2 id="build-photos">Photos from the actual build</h2>',1)
    journal='''
<span class="eyebrow">LIVING ENGINEERING PROJECT</span>
<h2>Project overview</h2>
<p>A reusable mobile robot platform for learning how embedded control, ROS 2 autonomy and cloud integration fit together. The journal records the engineering work from the first hardware checks onward, including problems, design decisions, tests and evidence.</p>
<div class="robot-current-status" id="current-status">
  <span class="paper-index">LATEST RECORDED STATUS · NOVEMBER 2026</span>
  <p><strong>Mechanical dry-fit.</strong> Chassis and wheel-clearance checks are underway. A standalone ESP32 micro-ROS publisher has communicated with ROS 2 through the serial agent. The rolling chassis and integrated drivetrain are not yet complete.</p>
  <p><strong>Next:</strong> Resolve the motor and caster mounting, then begin electrical bring-up.</p>
</div>
<h2 id="build-journal">Build journal</h2>
<p>Newest entries appear first. Open any earlier entry to see the evidence and the state of the project at that point in time.</p>
<div class="robot-journal-list">
<!-- ROBOT JOURNAL ENTRIES: newest first -->
<details class="robot-journal-entry" id="build-2026-11-dry-fit" open>
  <summary><span class="robot-journal-summary"><span class="paper-index">NOVEMBER 2026 · ENTRY 001</span><strong>Chassis dry-fit &amp; first micro-ROS check</strong><span class="robot-journal-subtitle">Initial mechanical checks, mounting constraints, hardware plan and build photos</span></span><span class="robot-journal-chevron" aria-hidden="true"></span></summary>
  <div class="robot-journal-content">
    <p class="robot-journal-note">Historical record as documented in November 2026. Plans and status below reflect that stage, not necessarily the current configuration. <a href="#build-2026-11-dry-fit">Link to this entry ↗</a></p>
'''+historical+'''
  </div>
</details>
<!-- END ROBOT JOURNAL ENTRIES -->
</div>
'''
    physical_new=physical[:article.start(2)]+journal+physical[article.end(2):]
    # Keep aside design; make its navigation useful for an expanding journal.
    aside=require_one(r'(<aside\b[^>]*class="[^"]*\bdetail-aside\b[^"]*"[^>]*>)(.*?)(</aside>)',physical_new,'robot evidence sidebar',re.S)
    nav='''<span class="eyebrow">BUILD EVIDENCE</span>
<a class="evidence-link" href="#current-status">↗ Current status</a>
<a class="evidence-link" href="#build-journal">↗ Build journal &amp; photos</a>
<a class="evidence-link" href="../assets/docs/Physical_Robot_Component_Inventory_Public.pdf" rel="noopener" target="_blank">↗ Component inventory PDF</a>
<p style="font-size:.86rem;line-height:1.6;margin-top:1.5rem">Each dated journal entry keeps its original observations, evidence and next steps.</p>'''
    physical_new=physical_new[:aside.start(2)]+nav+physical_new[aside.end(2):]
    new_snapshot=not snapshot.exists()
else:
    physical_new=physical
    if not snapshot.is_file(): raise SystemExit('Journal exists but November inventory snapshot is missing; restore that PDF before applying again.')

CSS_MARK='/* V21 — Current Build and robot journal only. */'
CSS_ADD='''
/* V21 — Current Build and robot journal only. */
.current-build-section .current-build-heading{min-width:0;padding-top:2px}
.current-build-heading .eyebrow{color:#7a5a2e}
.current-build-heading .eyebrow::after{content:"";display:inline-block;width:44px;height:1px;background:currentColor;vertical-align:middle;margin-left:14px;opacity:.7}
.current-build-heading h2{font-size:clamp(2.8rem,5.2vw,5.4rem);margin:14px 0 0;line-height:1.14;overflow-wrap:normal}
.current-build-heading h2 em{color:#8a6232}
html[data-theme="dark"] .current-build-heading .eyebrow{color:#e0b57c}
html[data-theme="dark"] .current-build-heading h2 em{color:#e7ad63}
.current-build-body .button{margin-top:22px;max-width:100%;white-space:normal}
@media(max-width:780px){.current-build-section .current-build-heading{padding:0 0 28px}.current-build-heading h2{font-size:clamp(2.55rem,9vw,4.2rem)}.current-build-body{padding-top:25px}}
.robot-current-status{border:1px solid var(--outline);border-radius:14px;background:var(--surface);padding:20px 22px;margin:24px 0 34px;scroll-margin-top:95px}
.robot-current-status .paper-index{display:block;margin-bottom:12px}
.robot-current-status p{margin:0 0 9px;line-height:1.65}
.robot-current-status p:last-child{margin-bottom:0}
.robot-journal-list{display:grid;gap:15px;margin:22px 0 0;min-width:0}
.robot-journal-entry{border:1px solid var(--outline);border-radius:15px;background:var(--surface);min-width:0;scroll-margin-top:95px;overflow:hidden}
.robot-journal-entry>summary{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px 22px;cursor:pointer;list-style:none;color:var(--text)}
.robot-journal-entry>summary::-webkit-details-marker{display:none}
.robot-journal-entry>summary:focus-visible{outline:2px solid var(--amber);outline-offset:-4px;border-radius:14px}
.robot-journal-summary{display:grid;gap:6px;min-width:0}
.robot-journal-summary strong{font-family:Manrope,system-ui,sans-serif;font-size:clamp(1.1rem,2vw,1.4rem);line-height:1.3;overflow-wrap:anywhere}
.robot-journal-subtitle{color:var(--subtext);font-size:.9rem;line-height:1.5}
.robot-journal-chevron{flex:0 0 11px;width:11px;height:11px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);margin-right:4px}
.robot-journal-entry[open]>.robot-journal-chevron,.robot-journal-entry[open]>summary .robot-journal-chevron{transform:rotate(225deg)}
.robot-journal-entry[open]>summary{border-bottom:1px solid var(--outline)}
.robot-journal-content{padding:22px;min-width:0;overflow-wrap:break-word}
.robot-journal-content .robot-journal-note{color:var(--subtext);font-size:.85rem;line-height:1.65;border-bottom:1px solid var(--outline);padding-bottom:16px;margin:0 0 22px}
.robot-journal-note a{white-space:normal;text-decoration:underline;text-underline-offset:3px}
.robot-journal-content h2{margin-top:28px}
.robot-journal-content h2:first-of-type{margin-top:18px}
.robot-journal-content pre{max-width:100%;white-space:pre-wrap;overflow-wrap:anywhere}
.robot-journal-content img,.robot-journal-content video{max-width:100%}
.robot-journal-content .evidence-gallery{min-width:0;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}
@media(max-width:600px){.robot-journal-entry>summary{padding:16px}.robot-journal-content{padding:16px}.robot-current-status{padding:17px}.robot-journal-content .evidence-gallery{grid-template-columns:1fr}}
'''
css_new=css if CSS_MARK in css else css.rstrip()+'\n'+CSS_ADD
# Change cache keys on affected pages only. Do not touch the shared JavaScript.
def cache(s):
    return re.sub(r'(portfolio\.css)(?:\?v=[^"\']+)?(?=["\'])',r'\1?v=21',s)
physical_new=cache(physical_new)
template_new=cache(template)
changes={edu_path:edu_new,physical_path:physical_new,css_path:css_new,template_path:template_new}
if new_snapshot:
    snapshot.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(current_pdf,snapshot)
    print('PRESERVED',snapshot.relative_to(ROOT))
for name,content in changes.items():
    p=ROOT/name
    if p.read_text(encoding='utf-8')!=content:
        p.write_text(content,encoding='utf-8');print('UPDATED',name)
    else: print('UNCHANGED',name)
subprocess.run([sys.executable,str(ROOT/'scripts/build_home.py')],cwd=ROOT,check=True)
print('Done. No Git commits or pushes. Review locally before publishing.')
