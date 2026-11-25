#!/usr/bin/env python3
"""Create a new standalone journal page from the portfolio's existing page shell.
No AI, no external libraries, no changes to earlier entries or the journal index.
"""
from pathlib import Path
from datetime import date
from html import escape
import argparse,re,sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('date',help='Actual build date, YYYY-MM-DD')
parser.add_argument('title',help='Short description of the work')
args=parser.parse_args()
try: day=date.fromisoformat(args.date)
except ValueError: sys.exit('Use YYYY-MM-DD.')
if day.isoformat()!=args.date: sys.exit('Use YYYY-MM-DD.')
if not args.title.strip(): sys.exit('Provide a meaningful title.')
root=Path(__file__).resolve().parents[1]
hub=root/'projects/physical-differential-drive-robot.html'
source=hub.read_text(encoding='utf-8')
if 'id="build-journal"' not in source: sys.exit('Apply the journal update first.')
slug='robot-build-'+day.isoformat(); dest=root/'projects'/f'{slug}.html'
if dest.exists(): sys.exit(f'{dest.name} already exists. Edit it instead of overwriting it.')
name=escape(args.title.strip()); display=f'{day.day} {day.strftime("%B %Y")}'
page_title=f'{name} · Robot build journal · Pritam Bandgar'
head,sep,tail=source.partition('<main id="main">')
if not sep or '</main>' not in tail: sys.exit('Project shell changed; could not create entry.')
head=re.sub(r'<title>.*?</title>',lambda _:f'<title>{page_title}</title>',head,count=1,flags=re.S)
# Update descriptions/titles while keeping original site metadata and shared assets.
head=re.sub(r'<meta\b[^>]*(?:name="description"|property="og:description")[^>]*/?>',lambda m: '<meta content="'+name+' — dated robot build journal entry." '+('name="description"' if 'name="description"' in m[0] else 'property="og:description"')+'/>',head)
head=re.sub(r'<meta\b[^>]*property="og:title"[^>]*/?>',lambda _:f'<meta content="{page_title}" property="og:title"/>',head)
footer=tail.split('</main>',1)[1]
entry=f'''<main id="main"><section class="interior-head"><div class="shell"><div class="project-breadcrumb"><a href="physical-differential-drive-robot.html#build-journal">← Build journal</a> / Robotics</div><span class="eyebrow">BUILD JOURNAL · <time datetime="{day.isoformat()}">{display}</time></span><h1>{name}</h1><p class="repo-slug repo-slug--dark">ROS 2 Mobile Robot Platform — Hardware to Cloud</p></div></section>
<section class="detail"><div class="shell detail-layout"><article class="detail-main">
<!-- DRAFT: Replace the comments with factual content before publishing. Remove unused headings. -->
<h2>Objective</h2>
<!-- <p>What was I trying to achieve, and why?</p> -->
<h2>Work and engineering decisions</h2>
<!-- <ul class="engineering-points"><li>What I actually did or changed.</li><li>Why I chose this approach.</li></ul> -->
<h2>Verification and results</h2>
<!-- <ul class="engineering-points"><li>Test setup, expected behaviour, actual result and units if measured.</li><li>Pass/fail or not tested yet. Do not invent results.</li></ul> -->
<h2>Limitations and next step</h2>
<!-- <p>What remains unresolved, and what is the next test?</p> -->
<h2>Evidence</h2>
<!-- Add original photos, logs or code links here. Example (replace file and description):
<figure class="detail-figure"><a class="media-zoom" data-lightbox="" href="../assets/media/physical-robot/{day.isoformat()}/photo.webp"><img src="../assets/media/physical-robot/{day.isoformat()}/photo.webp" alt="Describe the actual evidence" loading="lazy" decoding="async"/></a><figcaption>Describe what the photograph verifies.</figcaption></figure>
-->
</article><aside class="detail-aside"><span class="eyebrow">BUILD JOURNAL</span><a class="evidence-link" href="physical-differential-drive-robot.html#build-journal">↗ All journal entries</a><a class="evidence-link" href="physical-differential-drive-robot.html#build-2026-11">↗ First build entry</a></aside></div></section></main>'''
dest.write_text(head+entry+footer,encoding='utf-8')
print('Created draft:',dest.relative_to(root))
print('Fill the entry and add actual evidence. Then add this line to the index, newest first:')
print(f'<li><time datetime="{day.isoformat()}">{display}</time><a href="{slug}.html">{name} ↗</a></li>')
print('No earlier entries changed. Do not commit the draft before it is complete.')
