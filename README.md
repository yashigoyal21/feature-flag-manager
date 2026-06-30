# 🚀 Feature Flag & Remote Config Engine

A self-hosted feature flag and remote config system with two interfaces — a terminal dashboard and a Flutter app — both reading and writing the same live data in real time.

Built for the GDSC Project Challenge, June 2026.
Inspired by production tools like LaunchDarkly and Firebase Remote Config.

---

## ✨ Features

- **Toggle flags ON/OFF instantly** from a terminal dashboard or a Flutter app
- **Smart targeting rules:**
  - `Everyone` — all users see the feature
  - `Beta Users Only` — only approved testers see it
  - `Percentage` — e.g. only 10% of users see it (consistent hashing, same user always gets the same result)
- **Manage beta testers** — add, remove, and check users
- **Edit config variables** live — text or number app settings (welcome messages, login limits, etc.)
- **Two synced interfaces** — a keyboard-driven terminal UI and a Flutter app, both backed by the same data
- **Live updates** — the Flutter app polls the server every 2 seconds, so changes made anywhere show up everywhere within seconds, no restart needed
- **Persistent storage** — all changes saved to `flags.json` automatically
- **Automated tests** — backend test suite to verify the rules engine

---

## 🏗️ Architecture

```
ui.py (terminal dashboard)  ─┐
                              ├──▶  main.py (backend logic)  ──▶  flags.json (data)
server.py (HTTP server)     ─┘            │
        ▲                                 └──▶ user_manager.py (beta users)
        │
        │ HTTP (poll every 2s)
        │
flag_client/ (Flutter app, runs in Chrome)
```

`main.py` holds all the core logic — flags, configs, the rules engine. Both `ui.py` (terminal) and `server.py` (HTTP server) call the same functions in `main.py`, so no matter which interface makes a change, it's saved to the same `flags.json` file and visible everywhere.

The Flutter app never touches `flags.json` directly — it only talks to `server.py` over HTTP, the same way a real mobile app talks to a real backend.

---

## 📁 Project Structure

| File / Folder | Description |
|---|---|
| `main.py` | Core backend — flags, configs, rules engine |
| `ui.py` | Terminal dashboard with keyboard navigation |
| `server.py` | HTTP server — lets the Flutter app read/update flags over the network |
| `user_manager.py` | Beta user management |
| `flags.json` | Data store — flags, configs, beta users |
| `requirements.txt` | Python library dependencies |
| `flag_client/` | Flutter app source code (runs in Chrome) |

---

## 🛠️ Requirements

- **Python 3.11+**
- **Flutter SDK** (stable channel) — [installation guide](https://flutter.dev/docs/get-started/install)
- **Google Chrome** (the Flutter app runs as a web app in Chrome)
- Both the Python server and the Flutter app must run **at the same time**, in **separate terminals**

---

## ▶️ How to Run

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/flag-feature-manager.git
cd flag-feature-manager
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the HTTP server (Terminal 1 — leave this running)
```bash
python server.py
```
You should see:
```
FEATURE FLAG SERVER STARTED
  Server running at: http://localhost:8000
```

### 4. (Optional) Run the terminal dashboard (Terminal 2)
```bash
python ui.py
```
| Key | Action |
|---|---|
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

## 📡 Server API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/all` | Returns all flags and configs |
| PUT | `/flags/<name>/toggle` | Toggles a flag ON/OFF |
| PUT | `/configs/<key>` | Updates a config value (JSON body: `{"value": ...}`) |

---

## 👥 Team

| Member | Contributions |
|---|---|
| Yashasvi Sharma | Backend logic, rules engine, terminal dashboard, HTTP server, Flutter app |
| Yashi | Beta user management, config system, flags.json data design |