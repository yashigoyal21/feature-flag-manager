# This is your first Python file for the Feature Flag Manager project
# Lines starting with # are COMMENTS — Python ignores them
# They are notes for humans reading the code
 # ============================================================
# FEATURE FLAG MANAGER — main.py
# Person 1: Backend Logic
# ============================================================
 
import json   # This lets us read and write JSON files
import os     # This lets us check if files exist
import json
import os
from user_manager import add_beta_user, remove_beta_user, list_beta_users, is_beta_user  # ADD THIS LINE

 
 
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
 # ── GET CONFIG ──────────────────────────────────────────────
# Reads ONE config value by its name (called a 'key')
# Example: get_config('welcome_message') returns 'Hello, World!'
def get_config(key):
    data = load_flags()               # load everything from flags.json
    configs = data.get('configs', {}) # safely get configs section
                                      # if 'configs' missing, use empty {} instead of crashing
    if key in configs:                # check if this key exists
        return configs[key]           # send the value back to whoever called this function
    else:
        print(f"Config '{key}' not found!")
        return None                   # return None if key doesn't exist
 # ── SET CONFIG ──────────────────────────────────────────────
# Updates a config value and saves it permanently to flags.json
# Example: set_config('welcome_message', 'Good morning!')
def set_config(key, value):
    data = load_flags()                       # load current data
 
    # If there is no 'configs' section yet, create one
    if 'configs' not in data:
        data['configs'] = {}
 
    old_value = data['configs'].get(key, 'NOT SET')  # save old value for display
    data['configs'][key] = value                      # update with new value
    save_flags(data)                                  # save to flags.json
 
    print(f"Config '{key}' updated:")
    print(f"  Before: {old_value}")
    print(f"  After:  {value}")
 
# Prints all config variables in a neat table
def list_configs():
    data = load_flags()
    configs = data.get('configs', {})
 
    print()
    print('=' * 50)
    print('  CONFIG VARIABLES')
    print('=' * 50)
 
    if not configs:                           # if configs is empty
        print('  No config variables found.')
    else:
        for key, value in configs.items():    # loop through every key-value pair
            # if value is text, wrap in quotes. if number, just show it
            if isinstance(value, str):
                display = f'"{value}"'
            else:
                display = str(value)
            print(f'  {key:<28} : {display}')  # :<28 keeps columns aligned
 
    print('=' * 50)
    
    # ── ADD FLAG ────────────────────────────────────────────────
# Creates a brand new flag and adds it to flags.json
# Default values mean you only NEED to provide the name.
# Everything else is optional — Python uses the defaults if not provided.
def add_flag(name, rule='Everyone', enabled=False, rollout_percentage=100):
    data = load_flags()
 
    # First check if a flag with this name already exists
    for flag in data['flags']:
        if flag['name'] == name:
            print(f"ERROR: Flag '{name}' already exists!")
            return   # stop the function — do not create a duplicate
 
    # Build the new flag as a dictionary (same structure as flags in flags.json)
    new_flag = {
        'name': name,
        'enabled': enabled,
        'rule': rule,
        'rollout_percentage': rollout_percentage
    }
 
    data['flags'].append(new_flag)  # add it to the end of the flags list
    save_flags(data)                # save to file
 
    status = 'ON' if enabled else 'OFF'
    print(f"Created flag '{name}' [{status}]  Rule: {rule}")
   

# ── DELETE FLAG ─────────────────────────────────────────────
# Removes a flag from flags.json permanently
def delete_flag(name):
    data = load_flags()
    count_before = len(data['flags'])   # count flags before deletion
 
    # Keep ALL flags EXCEPT the one we want to delete
    # This is called list comprehension — a fast way to filter a list
    # Read it as: 'give me every flag f, but only if its name is NOT 'name''
    data['flags'] = [f for f in data['flags'] if f['name'] != name]
 
    if len(data['flags']) == count_before:
        # Count did not change = flag was never found
        print(f"ERROR: Flag '{name}' not found — nothing deleted.")
        return
 
    save_flags(data)
    print(f"Flag '{name}' has been deleted.")
   
    
# ── MAIN TEST BLOCK ─────────────────────────────────────────
# Runs only when you execute: python main.py directly
if __name__ == '__main__':
    print('=' * 50)
    print('  FEATURE FLAG MANAGER — Day 2 Test')
    print('=' * 50)
 
    # Show all flags
    list_flags()
 
    # Show all configs
    list_configs()
 
    # Test toggling
    print()
    toggle_flag('dark_mode_beta')     # flip ON
    toggle_flag('dark_mode_beta')     # flip back OFF
 
    # Test reading a config
    print()
    print('welcome_message is:', get_config('welcome_message'))
 
    # Test updating a config
    set_config('welcome_message', 'Welcome to our app!')
    print('After update:', get_config('welcome_message'))
    set_config('welcome_message', 'Hello, World!')  # restore original
 
    # Test creating and deleting a flag
    print()
    add_flag('temp_test_flag', rule='Everyone', enabled=True)
    list_flags()            # should show temp_test_flag at the bottom
    delete_flag('temp_test_flag')  # clean it up
 
    # Final view
    list_flags()            # should be back to normal
    list_configs()
 
    print()
    print('All Day 2 tests passed! ✅')
