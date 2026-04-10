# VEX Worlds 2026 — Skills Rankings Generator

Built by **HABS Gliders (34071B)** for scouting at the 2026 VEX Robotics World Championship.

## How it works

1. User visits the site and picks a division (Arts, Engineering, Innovate, Math, Science, Spirit, Technology)
2. The Python API reads the division's team list PDF + the global skills CSV from `/data`
3. It cross-references every team, ranks by score (ties broken by global rank), and streams back a formatted PDF
4. The PDF previews in-browser with a download button

## Repo structure

```
/
├── api/
│   └── generate.py          # Vercel Python serverless function
├── data/
│   ├── skills-standings.csv                        # ← update & push to refresh
│   ├── arts-division-team-list.pdf
│   ├── engineering-division-team-list.pdf
│   ├── innovate-division-team-list.pdf
│   ├── math-division-team-list.pdf
│   ├── science-division-team-list.pdf
│   ├── spirit-division-team-list.pdf
│   └── technology-division-team-list.pdf
├── public/
│   └── index.html           # Frontend
├── requirements.txt         # Python deps for Vercel
├── vercel.json              # Vercel config
└── README.md
```

## Updating the skills standings

1. Download the latest CSV from the VEX skills standings page
2. Replace `data/skills-standings.csv`
3. `git add data/skills-standings.csv && git commit -m "Update skills standings" && git push`
4. Vercel auto-redeploys in ~30 seconds — done

## Updating division team lists

Same process — replace the relevant PDF in `/data` and push.

## Local development

```bash
# Install Python deps
pip3 install pdfplumber reportlab

# Run the Python function manually to test
python3 -c "
import sys; sys.path.insert(0, 'api')
# then call generate logic directly
"

# Or just open public/index.html and point the fetch at a local Flask dev server
```

## Deploy to Vercel

```bash
npm i -g vercel
vercel --prod
```

Or connect the GitHub repo in the Vercel dashboard — it will auto-deploy on every push.

## File naming convention

Division PDFs must be named exactly:
```
{division-lowercase}-division-team-list.pdf
```
e.g. `math-division-team-list.pdf`, `spirit-division-team-list.pdf`
