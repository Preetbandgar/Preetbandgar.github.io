# Pritam Bandgar — Robotics Software Engineering Portfolio

Source for my GitHub Pages portfolio: https://preetbandgar.github.io/

The site documents hands-on ROS 2 and robotics projects, research, technical skills, and selected DevOps work. Case studies link to source repositories and the evidence available for each project. Work in progress is described as such.

## Site structure

- `index.html` — homepage, generated from `_includes/`
- `projects/` — project archive and individual case studies
- `certificates.html` and `cv.html` — training record and CV viewer
- `assets/` — styles, JavaScript, photos, demo videos, project files and public PDF
- `scripts/build_home.py` — regenerates the homepage
- `build_preview.py` — generates a standalone phone-preview HTML file

## Local preview

```bash
python3 scripts/build_home.py
python3 -m http.server 8000
```

Open `http://localhost:8000/`. To generate a standalone multi-page phone preview (requires Beautiful Soup):

```bash
python3 build_preview.py
```

## Editing and deployment

Edit the appropriate `_includes/*.html` file rather than editing the generated homepage in isolation. Regenerate `index.html` using `python3 scripts/build_home.py`. The public component PDF is limited to parts intended for the physical robot build.

The site is static HTML, CSS and JavaScript. Publishing changes requires a Git commit to the GitHub Pages repository. Previous release and maintenance notes are archived in `MAINTENANCE_HISTORY.md`.

## Source attribution

The TurtleBot3 simulation uses ROBOTIS and ROS 2/Nav2 components. The OpenTelemetry Demo and course-based applications are credited in their respective case studies. Project write-ups distinguish completed work from planned integration.
