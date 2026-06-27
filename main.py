# This is your first Python file for the Feature Flag Manager project
# Lines starting with # are COMMENTS — Python ignores them
# They are notes for humans reading the code
 # ============================================================
# FEATURE FLAG MANAGER — main.py
# Person 1: Backend Logic
# ============================================================
 
import json        # This lets us read and write JSON files
import hashlib  
import os     # This lets us check if files exist
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
   
   # ── IS FLAG ENABLED ─────────────────────────────────────────
# The RULES ENGINE — decides if a user should see a flag
# Returns True (show the feature) or False (hide the feature)
#
# Parameters:
#   flag_name  — which flag to check (e.g. 'new_checkout_flow')
#   user_id    — which user is asking (e.g. 'user_001')
import hashlib   # add this at the TOP of main.py with other imports!
 
def is_flag_enabled(flag_name, user_id):
    data = load_flags()
 
    # Step 1: Find the flag in our list
    target_flag = None
    for flag in data['flags']:
        if flag['name'] == flag_name:
            target_flag = flag
            break   # found it — stop looking
 
    # If flag does not exist at all, return False
    if target_flag is None:
        print(f"Flag '{flag_name}' does not exist!")
        return False
 
    # Step 2: If flag is OFF globally, no one sees it
    if not target_flag['enabled']:
        return False
 
    # Step 3: Apply the rule
    rule = target_flag.get('rule', 'Everyone')
 
    # RULE 1: Everyone — all users see it
    if rule == 'Everyone':
        return True
 
    # RULE 2: Beta Users Only — check if this user is a beta tester
    if rule == 'Beta Users Only':
        beta_users = data.get('beta_users', [])
        return user_id in beta_users   # True if in list, False if not
 
    # RULE 3: Percentage — use hash to consistently assign user to a group
    if rule == 'Percentage':
        percentage = target_flag.get('rollout_percentage', 100)
        # Convert user_id to a big number using MD5 hash
        hash_number = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        # Get remainder when divided by 100 (gives 0-99)
        remainder = hash_number % 100
        # If remainder is less than percentage, user is in the group
        return remainder < percentage
 
    # If rule is something unknown, default to False (safe)
    return False

    
# ── MAIN TEST BLOCK ─────────────────────────────────────────
# Runs only when you execute: python main.py directly
if __name__ == '__main__':
    print('Day 3 — Rules Engine Test')
    print()
 
    # Test 1: Everyone rule
    print('--- Rule: Everyone ---')
    print(is_flag_enabled('dark_mode_beta', 'any_user'))      # False (flag is OFF)
    print(is_flag_enabled('holiday_sale_banner', 'any_user')) # False (flag is OFF)
 
    # Test 2: Beta Users Only rule
    print()
    print('--- Rule: Beta Users Only ---')
    print(is_flag_enabled('new_checkout_flow', 'user_001'))   # True (user_001 is beta)
    print(is_flag_enabled('new_checkout_flow', 'stranger'))   # False (not beta)
 
    # Test 3: Percentage rule
    print()
    print('--- Rule: Percentage (10%) ---')
    # Test many users — roughly 10% should return True
    in_group = 0
    total = 100
    for i in range(total):
        if is_flag_enabled('ai_recommendations', f'user_{i}'):
            in_group += 1
    print(f'{in_group} out of {total} users are in the 10% group')
    print('Expected: roughly 10 users')
 
    # Test 4: Non-existent flag
    print()
    print(is_flag_enabled('fake_flag', 'user_001'))  # Should say flag not found
