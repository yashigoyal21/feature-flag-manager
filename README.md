# 🚀 Feature Flag & Config Manager
 
A lightweight terminal-based tool to manage feature flags
and remote config variables — built for the GDSC project challenge.
 
## What This Does
- Toggle app features ON/OFF without restarting the app
- Target flags to specific groups: Beta Users, percentage rollout, or Everyone
- Manage a list of beta testers (add/remove users)
- Edit config variables (text or number app settings) in real-time
- Clean terminal interface with keyboard controls (coming Day 4)

 
## How to Install and Run
 
### Step 1: Make sure Python is installed
```
python --version
```
You should see Python 3.11 or higher.
 
### Step 2: Clone this repository
```
git clone https://github.com/YOUR-USERNAME/feature-flag-manager.git
cd feature-flag-manager
```
 
### Step 3: Install dependencies
```
pip install rich readchar
```
 
### Step 4: Run the app
```
python main.py
```
 
## Project Structure
- `main.py` — Core backend logic (flags, configs, rules engine)
- `user_manager.py` — Beta user management (add/remove/check users)
- `ui.py` — Terminal dashboard (added Day 4)
- `flags.json` — Data storage (6 feature flags, 5 config variables)
- `test_main.py` — Automated tests (added Day 6)


