<div align="center">

<br/>

```
██╗   ██╗███████╗██╗  ██╗    ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ ███████╗
██║   ██║██╔════╝╚██╗██╔╝    ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗██╔════╝
██║   ██║█████╗   ╚███╔╝     ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║███████╗
╚██╗ ██╔╝██╔══╝   ██╔██╗     ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║╚════██║
 ╚████╔╝ ███████╗██╔╝ ██╗    ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝███████║
  ╚═══╝  ╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝
```

# VEX Worlds 2026 · Skills Rankings

**Scouting tool for the 2026 VEX Robotics World Championship — Middle School**  
Built by [Kayan Shah](https://github.com/KayanShah), Team Leader · **HABS Gliders 34071B**

<br/>

[![Live Site](https://img.shields.io/badge/Live%20Site-vex--skills--ranking.vercel.app-e94560?style=for-the-badge&logo=vercel&logoColor=white)](https://vex-skills-ranking.vercel.app)
[![VEX Worlds 2026](https://img.shields.io/badge/VEX%20Worlds-2026%20Missouri-4f8ef7?style=for-the-badge)](https://www.roboticseducation.org/vex-robotics-world-championship/)
[![Team](https://img.shields.io/badge/Team-34071B%20HABS%20Gliders-ffd700?style=for-the-badge)](https://www.robotevents.com/teams/V5RC/34071B)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com)

<br/>

![Preview](https://img.shields.io/badge/─────────────────────────────────────────────-transparent?style=flat-square)

</div>

---

## ✦ What is this?

A fast, fully client-side scouting web app for the **2026 VEX Robotics World Championship** (Middle School). It lets you instantly preview and download beautifully formatted **skills standings PDFs** for any of the 7 competition divisions — or the entire Worlds field at once.

No backend. No database. No login. Just a single HTML file that runs entirely in the browser.

---

## ✦ Features

| | Feature |
|---|---|
| 🌍 | **All Worlds ranking** — every team across all 7 divisions in one ranked list |
| 📐 | **Per-division rankings** — Arts, Engineering, Innovate, Math, Science, Spirit, Technology |
| 📄 | **PDF export** — beautifully formatted with HABS Gliders branding, medal highlights, and clickable hyperlinks |
| 🥇 | **Medal rows** — gold / silver / bronze highlighting for top 3 in each division |
| ⚡ | **Instant preview** — live ranked table in-browser before you download |
| 🔗 | **Zero dependencies** at runtime — no framework, no server, pure HTML/JS |
| 🚀 | **Auto-deploys** — push to GitHub → Vercel rebuilds in ~30 seconds |

---

## ✦ Live Preview

```
┌─────────────────────────────────────────────────────┐
│  VEX WORLDS 2026                        [HABS Logo] │
│  Middle School · Skills Rankings · 34071B           │
├───────────────┬─────────────────────────────────────┤
│  All Divisions│  MATH DIVISION · 84 TEAMS · 83 RANKED
│  ────────────  │                          [⬇ Download]
│  🌍 All Worlds│  ┌──────────────────────────────────┐│
│               │  │ # │ Team  │ Score │ Auto │ Driver ││
│  By Division  │  ├──────────────────────────────────┤│
│  🎨 Arts      │  │🥇1│ 88825H│  182  │  91  │   91  ││
│  ⚙️ Engineering│  │🥈2│ 2429A │  182  │  85  │   97  ││
│  💡 Innovate  │  │🥉3│ 8838D │  178  │  75  │  103  ││
│  📐 Math ◀   │  │  4│ 16688A│  167  │  70  │   97  ││
│  🔬 Science   │  │  5│ 1698A │  166  │  84  │   82  ││
│  🏆 Spirit    │  │ …│  …    │   …   │   …  │    …  ││
│  🤖 Technology│  └──────────────────────────────────┘│
│               │                                      │
│ [GENERATE PDF]│                                      │
└───────────────┴─────────────────────────────────────┘
```

---

## ✦ Tech Stack

```
Frontend    →  Vanilla HTML · CSS · JavaScript (no framework)
PDF Engine  →  jsPDF + jsPDF-AutoTable (CDN, client-side)
Fonts       →  Google Fonts — Bebas Neue, DM Sans, DM Mono
Hosting     →  Vercel (static, auto-deploy from GitHub)
Data        →  Embedded JSON — VEX global skills CSV + division team lists
```

---

## ✦ Project Structure

```
vex-skills-app/
├── public/
│   └── index.html          ← Entire app (HTML + CSS + JS + embedded data)
├── vercel.json             ← Vercel config (output dir: public)
└── README.md
```

Everything lives in **one file**. The skills data and division team lists are embedded directly as JSON constants inside `index.html` — no network requests, no API calls, instant load.

---

## ✦ Data Coverage

| Division | Teams | Ranked |
|---|---|---|
| 🌍 All Worlds | 586 | ~575 |
| 🎨 Arts | 84 | 81 |
| ⚙️ Engineering | 84 | 82 |
| 💡 Innovate | 83 | 80 |
| 📐 Math | 84 | 83 |
| 🔬 Science | 84 | 83 |
| 🏆 Spirit | 83 | 83 |
| 🤖 Technology | 84 | 83 |

Teams without a recorded skills score are listed separately at the bottom of each PDF.

---

## ✦ PDF Output

Each PDF includes:

- **Dark navy banner** with HABS Gliders logos on both sides, event title, division name, and team count
- **Full ranked table** with Div #, Global #, Score, Auto, Driver, Team #, Team Name, Country
- **Medal row highlights** — gold / silver / bronze for the top 3
- **Per-page footer** on every page: page number · division label · *[Kayan Shah](https://github.com/KayanShah)* (clickable hyperlink) · HABS Gliders Scouting
- **End block** — centred logo, team name, clickable author credit
- **No-score section** listing any teams with no skills data
- **Timestamp footer** — data freshness note + ranking methodology

The **All Worlds PDF** generates in **landscape A4** with an extra Division column.

---

## ✦ Updating the Data

Skills data is embedded in `index.html` as a JS constant. To update:

### 1. Update skills scores

Replace the `skills` object inside the `const RAW = {...}` block with fresh data from the VEX skills standings CSV.

### 2. Update division team lists

Replace the `teams` arrays inside `RAW.divisions` with the latest official team lists from RobotEvents.

### 3. Deploy

```bash
cd vex-skills-app
git add -A
git commit -m "Update skills data — [date]"
git push
```

Vercel auto-deploys in ~30 seconds. Works from private repos too.

---

## ✦ Local Development

No build step needed — just open the file:

```bash
# Option 1: open directly
open public/index.html

# Option 2: serve locally (avoids any browser file:// restrictions)
cd public
python3 -m http.server 8080
# → http://localhost:8080
```

---

## ✦ Ranking Logic

```
1. Filter division teams against global skills standings
2. Sort by Score DESC
3. Tiebreak by Global Rank ASC (better global rank wins)
4. Assign division rank (#1, #2, …)
5. Teams with no score listed separately (unranked)
```

---

## ✦ About

Built as a scouting tool for **[HABS Gliders 34071B](https://www.robotevents.com/teams/V5RC/34071B)** ahead of the 2026 VEX Robotics World Championship in Missouri.

HABS Gliders qualified for Worlds in their first competitive season, reaching the International Finals of the Greenpower Electric Car Challenge and ranking **#11 globally** in the VEX Virtual Skills programme.

---

<div align="center">

<br/>

Made with 🤖 by **[Kayan Shah](https://github.com/KayanShah)**  
Team Leader · HABS Gliders · 34071B · United Kingdom

<br/>

*Skills scores up to date as of 19:45 BST, Friday 10th April 2026*

</div>