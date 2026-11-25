# Portfolio V21 — Current Build & living engineering journal

## Apply once

Keep your accepted V20 checkout. Do NOT reapply V20 or replace the whole website.

From the root of your existing portfolio repository (the folder containing `index.html`, `assets`, `_includes`, and `scripts`), run:

```bash
python3 /path/to/apply_build_journal.py
```

Alternatively, give the repository path as the argument. Python 3 only; no extra package, service, or AI is required. The patch modifies `_includes/education.html`, `_includes/home.template`, `projects/physical-differential-drive-robot.html`, and appends narrowly scoped CSS to `assets/portfolio.css`. It regenerates `index.html` using the existing script and copies the current robot inventory PDF to a dated archive path. It does not modify other project pages, CV, research, certificates, animations, or global JavaScript. Running it twice does not duplicate the journal or heading. It makes no Git commits or pushes.

```bash
git diff --stat
git diff -- _includes/education.html projects/physical-differential-drive-robot.html assets/portfolio.css
python3 -m http.server 8000
```

Open `http://localhost:8000` in your browser. To generate your **exact full mobile HTML preview** from this updated checkout, use the existing `python3 build_preview.py` (requires Beautiful Soup as before). It embeds the journal along with the existing site. The current patch does not replace that preview builder.

## What visitors see

- Homepage: the Current Build has a matching left heading, **From hardware to autonomy.**, and the existing amber **See build progress ↗** button style.
- Robot project: project overview, current status, then a newest-first build journal. The first historical entry is November 2026 (not an invented exact day). Expand/collapse each entry independently. Each entry has a stable URL fragment, including the original record.
- The initial entry preserves the previously published build description, photos, decisions, plans and next steps. Its inventory link uses a dated PDF copy; the sidebar still links to the current inventory.

## Add a new entry manually (no AI)

1. Open `projects/physical-differential-drive-robot.html` in VS Code.
2. Copy `new_journal_entry_template.html.txt`, replace all example fields, and paste the completed `<details> ... </details>` block immediately **after** `<!-- ROBOT JOURNAL ENTRIES: newest first -->`. Never delete earlier entries. Remove the `open` attribute from the previous latest entry so it is collapsed by default; retain it on the new entry. Readers can expand any number of records.
3. Give each new entry a unique ID, for example `build-2026-12-03-motor-test` (use the actual date and a meaningful slug), and update the permalink to match. Change the entry number and date. Do not invent a date or claim completion before testing.
4. In the `id="current-status"` block near the top, update the date, verified current state and next step. If your homepage's short status is stale, update only the paragraph in `_includes/education.html` under `ROS 2 Mobile Robot Platform`, then run `python3 scripts/build_home.py`.
5. Put new evidence in a dated folder such as `assets/media/physical-robot/2026-12-03/`. Use the real filenames in the entry. Keep older files in their original locations; do not overwrite them. Use a new dated PDF in `assets/docs/robot-journal/` if the bill of materials changes, and link that copy from the relevant entry. The current inventory PDF can still be maintained separately. Add code or test-log links to GitHub commits (prefer immutable commit URLs for old entries).
6. Preview locally and commit the site, images and supporting evidence together. Share a specific entry with a URL like `https://preetbandgar.github.io/projects/physical-differential-drive-robot.html#build-2026-11-dry-fit` (works after deployment).

## What makes this an engineering record

Record actual work: objective, design constraints, implementation, observations and measurements, failures, changes, next step. Include evidence for significant decisions. For example, motor fit, verified encoder counts, wheel-odometry error, EKF comparisons, navigation repeatability, and robot-to-cloud telemetry can each be future entries once performed. The templates are not claims those milestones have been completed. Avoid copying generic assembly instructions, listing all purchases, or presenting plans as completed features.

The journal is static HTML with native browser disclosure controls; it does not require a backend, cloud subscription, database, or custom JavaScript. As the record grows, you can optionally move very old entries to year-specific archive pages while keeping permalinks/redirect links. There is no automatic GitHub-to-website sync; you decide when to publish a record and commit it.
