# ============================================================
# USER MANAGER — user_manager.py
# Person 2: Beta User Management
# Handles adding, removing, and listing beta users
# ============================================================
 
import json
 
 
# ── HELPER: LOAD AND SAVE ────────────────────────────────────
# We need our own load/save here since this is a separate file
def _load():
    with open('flags.json', 'r') as f:
        return json.load(f)
 
def _save(data):
    with open('flags.json', 'w') as f:
        json.dump(data, f, indent=2)
 
 
# ── LIST BETA USERS ──────────────────────────────────────────
# Shows all users who have special beta access
def list_beta_users():
    data = _load()
    users = data.get('beta_users', [])
 
    print()
    print('=' * 50)
    print('  BETA USERS')
    print('=' * 50)
 
    if not users:
        print('  No beta users registered.')
    else:
        for i, user in enumerate(users):
            print(f'  [{i+1}] {user}')
 
    print(f'  Total: {len(users)} beta user(s)')
    print('=' * 50)
 
 
# ── ADD BETA USER ────────────────────────────────────────────
# Adds a new user ID to the beta_users list
def add_beta_user(user_id):
    data = _load()
 
    # Make sure beta_users section exists
    if 'beta_users' not in data:
        data['beta_users'] = []
 
    # Check if user is already in the list
    if user_id in data['beta_users']:
        print(f"User '{user_id}' is already a beta user!")
        return
 
    data['beta_users'].append(user_id)  # add to the list
    _save(data)
    print(f"Added '{user_id}' to beta users. Total: {len(data['beta_users'])} user(s)")
 
 
# ── REMOVE BETA USER ─────────────────────────────────────────
# Removes a user ID from the beta_users list
def remove_beta_user(user_id):
    data = _load()
    users = data.get('beta_users', [])
 
    if user_id not in users:
        print(f"User '{user_id}' is not in beta users list!")
        return
 
    users.remove(user_id)          # .remove() deletes by VALUE, not index
    data['beta_users'] = users
    _save(data)
    print(f"Removed '{user_id}' from beta users. Remaining: {len(users)} user(s)")
 
 
# ── IS BETA USER ─────────────────────────────────────────────
# Returns True if user_id is in beta users, False otherwise
# Person 1 will use this in the rules engine tomorrow
def is_beta_user(user_id):
    data = _load()
    return user_id in data.get('beta_users', [])

    # ── ADD / UPDATE RULE ───────────────────────────────────────
# Changes the rule of an existing flag
# rule options: 'Everyone', 'Beta Users Only', 'Percentage'
def set_flag_rule(flag_name, rule, rollout_percentage=100):
    data = _load()


    # Validate the rule value
    valid_rules = ['Everyone', 'Beta Users Only', 'Percentage']
    if rule not in valid_rules:
        print(f"ERROR: '{rule}' is not a valid rule.")
        print(f"Valid options: {valid_rules}")
        return
 
    # Find the flag and update its rule
    for flag in data['flags']:
        if flag['name'] == flag_name:
            old_rule = flag.get('rule', 'Everyone')
            flag['rule'] = rule
            flag['rollout_percentage'] = rollout_percentage
            _save(data)
            print(f"Flag '{flag_name}' rule updated:")
            print(f"  Before: {old_rule}")
            print(f"  After:  {rule} ({rollout_percentage}%)")
            return
 
    print(f"ERROR: Flag '{flag_name}' not found!")

     # ── GET FLAG INFO ───────────────────────────────────────────
# Shows full details of one specific flag
def get_flag_info(flag_name):
    data = _load()
 
    for flag in data['flags']:
        if flag['name'] == flag_name:
            print()
            print('=' * 50)
            print(f"  FLAG: {flag['name']}")
            print('=' * 50)
            status = 'ON' if flag['enabled'] else 'OFF'
            print(f"  Status     : [{status}]")
            print(f"  Rule       : {flag.get('rule','Everyone')}")
            print(f"  Rollout    : {flag.get('rollout_percentage',100)}%")
            print('=' * 50)
            return flag   # also return it so other code can use it
 
    print(f"Flag '{flag_name}' not found!")
    return None
 
 
# ── SELF TEST ────────────────────────────────────────────────
# This only runs when you execute: python user_manager.py directly
if __name__ == '__main__':
    print('Testing User Manager — Day 3')
    print()
 
    # Show all beta users
    list_beta_users()
 
    # Test is_beta_user
    print()
    print(is_beta_user('user_001'))      # True
    print(is_beta_user('nobody'))        # False
 
    # Test set_flag_rule
    print()
    set_flag_rule('dark_mode_beta', 'Beta Users Only')
    get_flag_info('dark_mode_beta')
    set_flag_rule('dark_mode_beta', 'Everyone')   # restore
 
    # Test get_flag_info
    print()
    get_flag_info('ai_recommendations')
    get_flag_info('new_checkout_flow')
 
    print()
    print('All Day 3 user_manager tests passed! ✅')



    
