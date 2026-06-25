# This is your first Python file for the Feature Flag Manager project
# Lines starting with # are COMMENTS — Python ignores them
# They are notes for humans reading the code
 # ============================================================
# FEATURE FLAG MANAGER — main.py
# Person 1: Backend Logic
# ============================================================
 
import json   # This lets us read and write JSON files
import os     # This lets us check if files exist
 
 
# ── LOAD FLAGS ──────────────────────────────────────────────
# This function opens flags.json and returns all the data
def load_flags():
    # 'with open' safely opens a file (auto-closes when done)
    # 'r' means read mode
    with open('flags.json', 'r') as file:
        data = json.load(file)  # convert JSON text to Python object
    return data
 
 
# ── SAVE FLAGS ──────────────────────────────────────────────
# This function saves updated data BACK into flags.json
def save_flags(data):
    with open('flags.json', 'w') as file:  # 'w' means write mode
        json.dump(data, file, indent=2)    # indent=2 makes it readable
 
 
# ── LIST FLAGS ──────────────────────────────────────────────
# This function prints all flags neatly in the terminal
def list_flags():
    data = load_flags()          # load the data from file
    flags = data['flags']        # get just the flags list
 
    print()
    print('=' * 50)
    print('  FEATURE FLAGS')
    print('=' * 50)
 
    for i, flag in enumerate(flags):   # loop through each flag
        status = 'ON ' if flag['enabled'] else 'OFF'
        print(f"  [{i+1}] {flag['name']:<25} [{status}]  ({flag['rule']})")
 
    print()
    print('CONFIG VARIABLES:')
    for key, value in data['configs'].items():
        print(f'  - {key}: {value}')
    print('=' * 50)
 
 
# ── TOGGLE FLAG ─────────────────────────────────────────────
# This flips a flag from ON to OFF, or OFF to ON
def toggle_flag(name):
    data = load_flags()
 
    for flag in data['flags']:      # loop through all flags
        if flag['name'] == name:    # find the one we want
            # 'not' flips True to False and False to True
            flag['enabled'] = not flag['enabled']
            save_flags(data)        # save the change to file
 
            new_status = 'ON' if flag['enabled'] else 'OFF'
            print(f"Flag '{name}' is now: {new_status}")
            return  # stop the function after finding the flag
 
    # If we reach here, the flag was not found
    print(f"ERROR: Flag '{name}' does not exist!")
 
 
# ── MAIN PROGRAM ────────────────────────────────────────────
# This code runs when you execute: python main.py
# It is a simple test to make sure everything works
if __name__ == '__main__':
    print('Testing Feature Flag Manager...')
    print()
 
    # Test 1: Show all flags
    list_flags()
 
    # Test 2: Toggle a flag
    print()
    print('Toggling dark_mode_beta...')
    toggle_flag('dark_mode_beta')
 
    # Test 3: Show flags again to see the change
    list_flags()
 
    # Test 4: Toggle it back
    print('Toggling dark_mode_beta back...')
    toggle_flag('dark_mode_beta')
    list_flags()


