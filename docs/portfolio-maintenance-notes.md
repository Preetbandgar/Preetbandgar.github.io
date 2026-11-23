# Portfolio V19 — final local revisions

- Research: Sheffield Hallam course line is ABOVE the dissertation link, as requested in latest feedback.
- Certificates: Level 1 and Nav2 issuer links have been exchanged to match the observed destinations reported in-browser. This conflicts with the published LinkedIn certificate-ID associations; manually open the links before publishing.
- No design or animation changes from V18.
- Generated homepage: edit `_includes/research.html`, run `python3 scripts/build_home.py`.
- Deploy the folder **contents** to the `Preetbandgar.github.io` repository root (do not place the folder itself there).

---

# Pritam Bandgar: portfolio site (V17)

Static site for GitHub Pages. Plain HTML, one CSS file, one small JS file. No build step is needed to deploy.

## Preview locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000/
```

Opening `index.html` straight from disk also works on desktop. On a phone, use the separately provided `Pritam_Portfolio_V17_Mobile_Preview.html` (single HTML file with embedded assets).

## Structure

- `index.html` is generated from `_includes/*.html` and `_includes/home.template`. After editing an include, run `python3 scripts/build_home.py`.
- `projects/*.html`, `cv.html`, `certificates.html` are edited directly.
- `assets/portfolio.css` (colours are variables in `:root`; later sections override earlier ones), `assets/portfolio.js` (menu, theme, image viewer, video, typing roles; roles are the `ROLES` array).
- `assets/videos/*.mp4` + `assets/media/posters/*.webp` are the project recordings; `assets/media/*.webp` are screenshots; `assets/icons/` are tool logos.

## Adding or replacing media

Everything is served locally; nothing is hot-linked from GitHub. To turn a GIF into a small looping video:

```bash
ffmpeg -i demo.gif -vf "scale='min(960,iw)':-2,fps=15,format=yuv420p" -c:v libx264 -crf 29 -preset veryfast -movflags +faststart -an assets/videos/demo.mp4
ffmpeg -ss 1 -i demo.gif -frames:v 1 poster.png   # then save as WebP in assets/media/posters/
```

Card videos (`data-card-video`) play only while visible and stay still with reduced-motion or data-saver. Detail-page videos have controls and do not autoplay.

## CV

Replace `assets/cv/Pritam_Bandgar_CV.pdf` and keep the filename.

## Motion

Effects live in the last sections of `assets/portfolio.css` and in `assets/portfolio.js`: hero entrance and glow, scroll progress bar, staggered reveals, card spotlight, button sweep, tool strip, nav scrollspy, page cross-fade.
They run only when `<html data-motion="full">`. The script sets that from the device's reduced-motion setting, and visitors can override it with the "Animations" switch in the footer (saved in `localStorage`). In reduced mode the hero roles still change, with no typing movement.

## Phone preview

The provided V17 phone preview is a convenience artifact for review. For publishing, deploy this multi-page folder. Rebuilding the homepage with `scripts/build_home.py` does not rebuild the standalone preview.

## Before you publish

- Social-card tags in each `<head>` assume the site lives at `https://preetbandgar.github.io/`. Change `og:image` if it does not.
- Tool logos: Devicon 2.16.0 (MIT) and the Nav2 logo from its repository. Foxglove has no logo here, by design.
- Project text describes what the repositories contain. Check it against your own runs before applying anywhere.

## V15 maintenance and responsive layout

- **Projects (titles, text, media):** Edit `projects/index.html` for the archive and the matching `projects/<repo-name>.html` for the case study. The homepage project cards live in `_includes/projects.html`.
- **Hero roles:** Edit the `ROLES` array near the top of `assets/portfolio.js`.
- **Theme:** By default the site follows the device `prefers-color-scheme` setting. A visitor who uses the theme button gets their choice saved in `localStorage`; it takes priority on return visits. To reset: clear the website's local storage.
- **Desktop project diagrams:** The AWS EKS and Java Blogging archive cards use *local* PNG files at `assets/projects/diagrams/{Terraform-aws-eks,FullStack-Blogging-App}.png`. They use `diagram-media` styling to display the entire diagram instead of cropping it.
- **Header CV button:** Its compact style is at the end of `assets/portfolio.css`.
- **Homepage edits:** Run `python3 scripts/build_home.py` and commit both `_includes/*` and generated `index.html`.
- **Local preview:** From the folder containing `index.html`, run `python3 -m http.server 8000`, then open `http://localhost:8000`. Check at 360, 390, 820, 1024, 1366 and 1920 CSS pixels in browser responsive mode.
- **Publish:** Copy/commit the contents of this folder into the existing GitHub Pages repository only after manually reviewing them. Do not copy a surrounding parent folder into the repo root.


## V16: two display fixes

- Hero's third role is **Robotics Simulation Engineer**. The roles live in `assets/portfolio.js`, and the accessible text is in `_includes/hero.html`. After editing the hero include, run `python3 scripts/build_home.py`.
- Two architecture images are embedded as PNG data inside `projects/index.html` to avoid local-file image loading problems on laptops. Original editable diagrams remain in `assets/projects/diagrams/`. If you change either diagram, run `python3 scripts/refresh_archive_diagrams.py` to update the embedded image; no external packages are required.
- For reliable checking, extract the ZIP and run `python3 -m http.server 8000` from the portfolio folder, then visit `http://localhost:8000`.

## V17 release changes

- TurtleBot3 Test 07 describes the default `robot_radius: 0.15` and the four-waypoint Simple Commander mission. See `docs/tuning.md` in the linked repository for exact settings.
- Certificate links: Level 1 and Nav2 were swapped to match the certificates seen by the owner. **Verify all three in a browser before publishing**, since Udemy may block automated inspection.
- Dissertation opens the owner-supplied Google Drive file link (the file must be shared for public viewing).
- Skills tool rows have complete, shortened labels rather than ellipses. At extremely narrow widths, the row may wrap instead of clipping.
- The source for the homepage remains `_includes/`; after editing it, run `python3 scripts/build_home.py`. Do not edit only `index.html` because the next build would overwrite your changes.
- To publish, upload the **contents** of this folder to the root of `Preetbandgar.github.io`, not the folder itself. No automated publishing was performed.

### Final manual checks before GitHub Pages deployment

1. From this directory run `python3 -m http.server 8000` and visit `http://localhost:8000`. Check homepage, archive, each project page, and the CV in phone/tablet/desktop responsive mode.
2. Open all three **View certificate** links; the Level 1 and Nav2 links were swapped per the owner's observation, but Udemy blocked automated verification.
3. Open **View dissertation** from an incognito window and confirm that Google Drive grants public view access to the intended PDF.
4. Test videos, the typing role cycle, the light/dark mode selector, image zoom, and reduced-motion mode.
5. After copying files to the GitHub Pages repository, confirm that the GitHub Pages build succeeded and check the site in a private window to avoid a stale cache.


## Release 18: avoid opening an older extraction

Extract into a **new** `Pritam_Portfolio_V18` folder; do not merge with V16/V17.
Open `VERSION_CHECK.txt` first and confirm the release number.
Run `python3 -m http.server 8000` and visit `http://localhost:8000` on your computer.
For an old cached view, perform a hard reload (`Ctrl+Shift+R`) or use a private window.
The file `index.html` contains `<meta name="portfolio-release" content="18">`.
This release deliberately allows technical-skill labels to wrap rather than conceal them with `...`; at common laptop widths the grid uses two columns.
The certificate IDs were checked against the owner's LinkedIn public certification records.
