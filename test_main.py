# ============================================================
# TEST SUITE — test_main.py
# Author: Person 2
# Description: Automated tests for all project functions.
# Run with: python test_main.py
# ============================================================
 
import json
from main import (
    load_flags, toggle_flag, get_config,
    set_config, add_flag, delete_flag, is_flag_enabled
)
from user_manager import (
    add_beta_user, remove_beta_user, is_beta_user, list_beta_users
)
 
# Counters to track how many tests pass and fail
passed = 0
failed = 0
 
def check(test_name, condition):
    """
    Helper function: prints PASS or FAIL for each test.
    condition = True means the test passed.
    condition = False means something is broken.
    """
    global passed, failed
    if condition:
        print(f'  ✅ PASS: {test_name}')
        passed += 1
    else:
        print(f'  ❌ FAIL: {test_name}')
        failed += 1
 
print('=' * 55)
print('  RUNNING FULL TEST SUITE')
print('=' * 55)
 
 
# ── TEST GROUP 1: DATA LOADING ───────────────────────────────
print()
print('--- Group 1: Data Loading ---')
data = load_flags()
check('load_flags returns a dictionary',     isinstance(data, dict))
check('flags section exists',               'flags' in data)
check('configs section exists',             'configs' in data)
check('beta_users section exists',          'beta_users' in data)
check('at least 6 flags loaded',            len(data['flags']) >= 6)
check('at least 5 configs loaded',          len(data['configs']) >= 5)
 
 
# ── TEST GROUP 2: TOGGLE FLAG ────────────────────────────────
print()
print('--- Group 2: Toggle Flag ---')
data         = load_flags()
flag_name    = data['flags'][1]['name']          # dark_mode_beta
original     = data['flags'][1]['enabled']       # remember original state
toggle_flag(flag_name)                           # flip it
data_after   = load_flags()
check('toggle changes enabled value',      data_after['flags'][1]['enabled'] != original)
toggle_flag(flag_name)                           # flip it back
data_restored = load_flags()
check('toggle twice restores original',    data_restored['flags'][1]['enabled'] == original)
 
 
# ── TEST GROUP 3: CONFIG FUNCTIONS ───────────────────────────
print()
print('--- Group 3: Config Functions ---')
original_msg = get_config('welcome_message')
check('get_config returns a value',        original_msg is not None)
check('welcome_message is a string',       isinstance(original_msg, str))
set_config('welcome_message', 'TEST_VALUE_XYZ')
check('set_config updates the value',      get_config('welcome_message') == 'TEST_VALUE_XYZ')
set_config('welcome_message', original_msg)     # restore
check('value restored correctly',          get_config('welcome_message') == original_msg)
check('get missing config returns None',   get_config('totally_fake_key') is None)
 
 
# ── TEST GROUP 4: ADD AND DELETE FLAG ────────────────────────
print()
print('--- Group 4: Add and Delete Flag ---')
data_before  = load_flags()
count_before = len(data_before['flags'])
add_flag('test_flag_abc_xyz', rule='Everyone', enabled=True)
data_after   = load_flags()
check('add_flag increases count by 1',     len(data_after['flags']) == count_before + 1)
names = [f['name'] for f in data_after['flags']]
check('new flag name appears in list',     'test_flag_abc_xyz' in names)
check('new flag is enabled',               data_after['flags'][-1]['enabled'] == True)
delete_flag('test_flag_abc_xyz')
data_final   = load_flags()
check('delete_flag reduces count by 1',    len(data_final['flags']) == count_before)
names_final  = [f['name'] for f in data_final['flags']]
check('deleted flag no longer in list',    'test_flag_abc_xyz' not in names_final)
 
 
# ── TEST GROUP 5: RULES ENGINE ───────────────────────────────
print()
print('--- Group 5: Rules Engine ---')
# new_checkout_flow is ON and Beta Users Only
check('beta user sees beta-only flag',     is_flag_enabled('new_checkout_flow', 'user_001'))
check('stranger cannot see beta flag',     not is_flag_enabled('new_checkout_flow', 'total_stranger_xyz'))
# dark_mode_beta is OFF — no one should see it
check('OFF flag hidden from beta user',    not is_flag_enabled('dark_mode_beta', 'user_001'))
check('OFF flag hidden from everyone',     not is_flag_enabled('dark_mode_beta', 'user_admin'))
# non-existent flag
check('missing flag returns False',        not is_flag_enabled('this_flag_does_not_exist', 'user_001'))
 
 
# ── TEST GROUP 6: BETA USER MANAGEMENT ──────────────────────
print()
print('--- Group 6: Beta User Management ---')
check('user_001 is a beta user',           is_beta_user('user_001'))
check('user_admin is a beta user',         is_beta_user('user_admin'))
check('unknown user is NOT beta',          not is_beta_user('totally_unknown_person_xyz'))
# Test add and remove
add_beta_user('temp_test_beta_999')
check('newly added user is beta',          is_beta_user('temp_test_beta_999'))
# Adding same user twice should not duplicate
add_beta_user('temp_test_beta_999')
data_check = load_flags()
count = data_check['beta_users'].count('temp_test_beta_999')
check('no duplicate users added',          count == 1)
remove_beta_user('temp_test_beta_999')
check('removed user is no longer beta',    not is_beta_user('temp_test_beta_999'))
 
 
# ── FINAL RESULTS ────────────────────────────────────────────
print()
print('=' * 55)
print(f'  RESULTS:  {passed} passed   |   {failed} failed')
print('=' * 55)
if failed == 0:
    print('  🎉 ALL TESTS PASSED! Project is ready for submission!')
    print('=' * 55)
else:
    print(f'  ⚠️  {failed} test(s) FAILED — check the functions listed above')
    print('  Fix the failures then run: python test_main.py again')
    print('=' * 55)
