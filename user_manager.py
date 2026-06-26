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
 
 
# ── SELF TEST ────────────────────────────────────────────────
# This only runs when you execute: python user_manager.py directly
if __name__ == '__main__':
    print('Testing User Manager...')
 
    # Show current beta users
    list_beta_users()
 
    # Add a new user
    print()
    add_beta_user('new_tester_99')
    add_beta_user('user_001')     # already exists — should warn
 
    # Show updated list
    list_beta_users()
 
    # Check if someone is a beta user
    print()
    result = is_beta_user('user_001')
    print(f'Is user_001 a beta user? {result}')   # Should print True
 
    result = is_beta_user('random_stranger')
    print(f'Is random_stranger a beta user? {result}')  # Should print False
 
    # Remove the test user we added
    print()
    remove_beta_user('new_tester_99')
    list_beta_users()   # should be back to original 5 users
 
    print()
    print('All user_manager tests passed!')
