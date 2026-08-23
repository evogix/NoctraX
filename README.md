# NoctraX — by Md. Faizal (@faizalx1337)
### `WE SEE WHAT YOU TRY TO HIDE` — Dark Ghost Trace OSINT

<p align="center">
  <img src="https://img.shields.io/badge/NoctraX-v2.2%20VOID%20SPECTER-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Author-Md.%20Faizal%20@faizalx1337-cyan?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GitHub-evogix/NoctraX-black?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" />
</p>

```
 ███╗   ██╗  ██████╗   ██████╗ ████████╗██████╗  █████╗ ██╗  ██╗
 ████╗  ██║ ██═══██╗ ██╔════╝ ╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
 ██╔██╗ ██║ ██║   ██║ ██║         ██║   ██████╔╝███████║ ╚███╔╝ 
 ██║╚██╗██║ ██║   ██║ ██║         ██║   ██╔══██╗██╔══██║ ██╔██╗ 
 ██║ ╚████║ ╚██████╔╝ ╚██████╗    ██║   ██║  ██║██║  ██║██╔╝ ██╗
 ╚═╝  ╚═══╝  ╚═════╝   ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

  Specter in the Void  •  by Md. Faizal (@faizalx1337)  •  v2.2
  WE SEE WHAT YOU TRY TO HIDE
  IG: @faizalx1337  |  GitHub: github.com/evogix/NoctraX
```

> **Professional Dark OSINT — 100% Native • No APIs • Silent Hunt • Pipeline**

---

## ⚡ Features

| Module | What it does | Sites |
|--------|--------------|-------|
| **Email** | 76 sites + breach (xposedornot) + Gravatar | Spotify, GitHub, X, Paytm, Flipkart, etc |
| **Username** | 50+ socials/profile hunt | GitHub, Insta, X, TikTok, Reddit, HTB, etc |
| **Phone** | Carrier + Region + WhatsApp + Timezone | Airtel/Jio/Vi + WA surface |
| **Pipeline** | `cat file.txt \| noctrax` auto-detect mixed | Email + Phone + Username one shot |
| **Export** | CSV / JSON | For reporting |
| **UI** | Neon hacker box + colorama + silent mode | `WE SEE WHAT YOU TRY TO HIDE` |

- ✅ 100% Native — no holehe, no sherlock dependency
- ✅ Colorama neon dark theme — professional hacker vibe
- ✅ Silent mode — `output hata ke` sirf FOUND
- ✅ File pipeline — mixed `email, phone, username` in one file
- ✅ Ethical — dummy examples only, no real PII in docs

---

## 📦 Install

### From GitHub (latest)
```bash
pip install git+https://github.com/evogix/NoctraX.git --break-system-packages
# Termux/Kali
pip install phonenumbers httpx trio beautifulsoup4 termcolor colorama tqdm --break-system-packages
pip install -e . --break-system-packages
```

### From Local
```bash
git clone https://github.com/evogix/NoctraX.git
cd NoctraX
pip install -e . --break-system-packages
```

### Verify
```bash
noctrax --help
noctrax --version
# NoctraX v2.2 by Md. Faizal — VOID SPECTER
```

---

## 🚀 Usage — All Commands

### 1. Email Hunt
```bash
# Basic
noctrax example@gmail.com
noctrax example@gmail.com --only-used
noctrax example@gmail.com --silent
noctrax example@gmail.com --silent --json
noctrax example@gmail.com --csv --json
noctrax example@gmail.com --no-breach
noctrax example@gmail.com --timeout 15
noctrax example@gmail.com --no-color
```

### 2. Username Hunt
```bash
noctrax --username example_user
noctrax --username example_user --only-used
noctrax --username target123 --silent
noctrax --username target123 --silent --json
noctrax --username target123 --csv
```

### 3. Phone Intel
```bash
noctrax --phone +91XXXXXXXXXX
noctrax --phone +919999999999
noctrax --phone +91XXXXXXXXXX --json
noctrax --phone +91XXXXXXXXXX --silent
```

### 4. PIPELINE — File Auto Detect 🔥
```bash
# file.txt can contain mix of emails + phones + usernames (one per line or mixed)
cat file.txt | noctrax
cat file.txt | noctrax --only-used
cat file.txt | noctrax --silent
cat file.txt | noctrax --silent --json
cat file.txt | noctrax --csv

# Direct file (no cat)
noctrax file.txt --only-used
noctrax targets.txt --silent --json
```

**file.txt example:**
```
example@gmail.com
target@example.com
+91XXXXXXXXXX
+919999999999
example_user
target123
hacker_007
```

### 5. Flags Cheatsheet
```bash
--only-used    # sirf FOUND dikhao
--silent       # output hata ke, no banner
--json         # JSON export
--csv          # CSV export
--no-breach    # breach skip (email)
--timeout 15   # per-request timeout
--no-color     # color off
--no-clear     # screen clear off
--help         # help
--version      # version
```

### 6. Pro Examples
```bash
# Silent pipeline + JSON for automation
cat targets.txt | noctrax --only-used --silent --json > results.json

# Full recon + CSV
noctrax --username example_user --csv --json

# Fast email check
noctrax example@gmail.com --only-used --no-breach --timeout 5
```

---

## 🎨 UI Preview

```
  ╔══════════════════════════════════════════════════════════╗
  ║                  ► example@gmail.com ◀                   ║
  ╚══════════════════════════════════════════════════════════╝
  ☠  BREACHED: Canva, Adobe, LinkedIn [+3 leaks]
  ────────────────────────────────────────────────────────────
  [+] github.com                 ● FOUND
  [+] twitter.com                ● FOUND
  [+] spotify.com                ● FOUND

  ✔ 3 FOUND  •  71 not found • 2 rate-limit  •  76 checked
  ◆ NoctraX v2.2  •  Md. Faizal  •  IG: @faizalx1337  •  github.com/evogix/NoctraX
```

---

## 🛠 Tech Stack
- Python 3.8+ • httpx • trio (async) • beautifulsoup4 • phonenumbers • colorama • termcolor

---

## ⚠️ Disclaimer — Ethical Use Only
> This tool is for **educational & authorized OSINT only**. Don't trace real emails/phones/usernames without consent. Use dummy examples (`example@gmail.com`, `+91XXXXXXXXXX`) in public demos. Author not responsible for misuse.

---

## 👤 Author
**Md. Faizal — IG: @faizalx1337**  
GitHub: **github.com/evogix/NoctraX**  
Tagline: **WE SEE WHAT YOU TRY TO HIDE** — *Specter in the Void*

<p align="center">
  <b>⭐ Star the repo if you like NoctraX — VOID SPECTER</b><br>
  <code>pip install git+https://github.com/evogix/NoctraX.git</code>
</p>
