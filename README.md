


# 🚀 Feature Flag & Config Manager
 
A lightweight terminal-based tool to manage feature flags and remote config
variables in real-time — without restarting or redeploying the app.
 
Built for the GDSC Project Challenge, June 2026.
Inspired by production tools like LaunchDarkly and Firebase Remote Config.
 
---
 
## ✨ Features
 
- **Toggle flags ON/OFF instantly** from a colourful terminal dashboard
- **Smart targeting rules:**
  - `Everyone` — all users see the feature
  - `Beta Users Only` — only approved testers see it
  - `Percentage Rollout` — e.g. only 10% of users see it (consistent hashing)
- **Manage beta testers** — add, remove, and check users
- **Edit config variables** live — text or number app settings
- **Keyboard navigation** — arrow keys, spacebar, no mouse needed
- **Persistent storage** — all changes saved to flags.json automatically
- **Automated tests** — full test suite to verify all functions
 
---
 
## 🛠️ Installation
 
### 1. Make sure Python 3.11+ is installed
```
python --version
```
 
### 2. Clone this repository
```
git clone https://github.com/YOUR_USERNAME/feature-flag-manager.git
cd feature-flag-manager
```
 
### 3. Install dependencies (one command)
```
pip install -r requirements.txt
```
 
### 4. Run the dashboard
```
python ui.py
```
 
### 5. Or run backend directly
```
python main.py
```
 
### 6. Run automated tests
```
python test_main.py
```
 
---
 
## ⌨️ Keyboard Controls
 
| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate between flags |
| Space | Toggle selected flag ON/OFF |
| E | Edit a config variable |
| N | Create a new flag |
| D | Delete selected flag |
| Q | Quit |
 
---
 
## 📁 Project Structure
 
| File | Description | Owner |
|------|-------------|-------|
| `main.py` | Core backend — flags, configs, rules engine | Person 1 |
| `ui.py` | Terminal dashboard with keyboard controls | Person 1 |
| `user_manager.py` | Beta user management | Person 2 |
| `flags.json` | Data store — 6 flags, 5 configs, 5 beta users | Person 2 |
| `requirements.txt` | Python library dependencies | Person 2 |
| `test_main.py` | Automated test suite | Both |
 
---
 
## 🏗️ Architecture
 
```
ui.py  (dashboard)
  └── imports ──▶  main.py  (backend logic)
                     └── reads/writes ──▶  flags.json  (data)
                     └── imports ──▶  user_manager.py  (beta users)
```
 
---
 