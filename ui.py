
# ============================================================
# TERMINAL DASHBOARD — ui.py
# Person 1 (Yashasvi): Visual interface for the Feature Flag Manager
# Uses 'rich' for colours/tables and 'readchar' for keyboard input
# ============================================================
 
from rich.console import Console   # the main object for all output
from rich.table import Table       # for drawing the flags table
from rich.panel import Panel       # for the header and footer boxes
from rich import box               # table border style options
import readchar                    # keyboard input without Enter
from main import (                 # import our backend functions
    load_flags, toggle_flag, get_config,
    set_config, add_flag, delete_flag
)
 
# Create ONE console object — we use this for all printing
console = Console()
 
 
# ── DISPLAY FUNCTION ─────────────────────────────────────────
# Draws the entire dashboard. Called every time anything changes.
# 'selected' = which row is highlighted (0 = first flag, 1 = second, etc.)
def display_dashboard(selected=0):
    console.clear()               # wipe the screen before redrawing
    data = load_flags()           # get fresh data from flags.json
 
    # ── HEADER ──────────────────────────────────────────────
    console.print(Panel(
        '[bold white]🚀  FEATURE FLAG & CONFIG MANAGER[/bold white]',
        style='bold blue', expand=False
    ))
    console.print()
 
    # ── FLAGS TABLE ─────────────────────────────────────────
    console.print('[bold cyan]  FEATURE FLAGS:[/bold cyan]')
    console.print()
 
    table = Table(box=box.SIMPLE, show_header=True, header_style='bold blue')
    table.add_column('#',         width=4,  style='dim')
    table.add_column('Flag Name', width=26)
    table.add_column('Status',    width=8)
    table.add_column('Rule',      width=20)
    table.add_column('Rollout',   width=10)
 
    for i, flag in enumerate(data['flags']):
        # Green ON or red OFF
        status = '[green][ ON ][/green]' if flag['enabled'] else '[red][OFF][/red]'
 
        # Highlight the currently selected row with cyan arrow
        if i == selected:
            name = f'[bold cyan]▶ {flag["name"]}[/bold cyan]'
        else:
            name = flag['name']
 
        pct  = str(flag.get('rollout_percentage', 100)) + '%'
        rule = flag.get('rule', 'Everyone')
        table.add_row(str(i+1), name, status, rule, pct)
 
    console.print(table)
 
    # ── CONFIGS SECTION ─────────────────────────────────────
    console.print()
    console.print('[bold cyan]  CONFIG VARIABLES:[/bold cyan]')
    for key, val in data.get('configs', {}).items():
        console.print(f'  [dim]-[/dim] [yellow]{key}[/yellow] : {val}')
 
    # ── FOOTER — shows keyboard shortcuts ───────────────────
    console.print()
    console.print(Panel(
        '[dim][↑↓] Navigate   [Space] Toggle   [E] Edit Config   [N] New Flag   [D] Delete   [Q] Quit[/dim]',
        style='dim', expand=False
    ))
 
 
# ── CONFIG EDITOR ────────────────────────────────────────────
# Shows a prompt so user can select and edit a config value
# Called when user presses E in the dashboard
def edit_config_prompt():
    console.clear()
    data  = load_flags()
    configs = data.get('configs', {})
 
    if not configs:
        console.print('[red]No config variables found![/red]')
        readchar.readkey()    # wait for any key before going back
        return
 
    console.print('[bold cyan]Select a config to edit:[/bold cyan]')
    console.print()
    keys = list(configs.keys())
    for i, k in enumerate(keys):
        console.print(f'  [{i+1}] {k} = {configs[k]}')
    console.print()
 
    choice = console.input('[yellow]Enter number (or 0 to cancel): [/yellow]')
    if not choice.isdigit() or int(choice) == 0:
        return
 
    idx = int(choice) - 1
    if idx < 0 or idx >= len(keys):
        console.print('[red]Invalid number![/red]')
        readchar.readkey()
        return
 
    key = keys[idx]
    console.print(f'[yellow]Current value:[/yellow] {configs[key]}')
    new_val = console.input('[yellow]New value: [/yellow]')
 
    # Try to convert to int or float — if not possible, keep as text string
    try:    new_val = int(new_val)
    except: 
        try: new_val = float(new_val)
        except: pass
 
    set_config(key, new_val)
    console.print(f'[green]✅ Updated: {key} = {new_val}[/green]')
    import time; time.sleep(1)    # pause so user can see the success message
 
 
# ── MAIN LOOP ────────────────────────────────────────────────
# This keeps the dashboard running until Q is pressed.
# It listens for keypresses and responds to each one.
def run():
    data         = load_flags()
    total        = len(data['flags'])
    selected     = 0     # start with first flag highlighted
 
    while True:          # keep looping forever until Q pressed
        display_dashboard(selected)
        key = readchar.readkey()    # wait for a keypress
 
        # Q — quit
        if key in ('q', 'Q'):
            console.clear()
            console.print('[bold green]Goodbye! 👋[/bold green]')
            break
 
        # Arrow UP — move selection up (wraps to bottom if at top)
        elif key == readchar.key.UP:
            selected = (selected - 1) % total
 
        # Arrow DOWN — move selection down (wraps to top if at bottom)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % total
 
        # SPACE — toggle the currently selected flag
        elif key == ' ':
            data = load_flags()
            flag_name = data['flags'][selected]['name']
            toggle_flag(flag_name)   # flip ON/OFF
            data  = load_flags()     # reload after change
            total = len(data['flags'])
 
        # E — edit a config variable
        elif key in ('e', 'E'):
            edit_config_prompt()
 
        # N — create a new flag
        elif key in ('n', 'N'):
            console.clear()
            name = console.input('[yellow]New flag name (no spaces): [/yellow]')
            rule = console.input('[yellow]Rule — type exactly one of:\n  Everyone / Beta Users Only / Percentage\n> [/yellow]')
            if name.strip() and rule.strip():
                add_flag(name.strip(), rule=rule.strip())
                data  = load_flags()
                total = len(data['flags'])
                selected = total - 1    # jump to the new flag
 
        # D — delete the selected flag
        elif key in ('d', 'D'):
            data = load_flags()
            flag_name = data['flags'][selected]['name']
            delete_flag(flag_name)
            data  = load_flags()
            total = len(data['flags'])
            selected = min(selected, total - 1)   # make sure selection is still valid
 
 
# ── ENTRY POINT ──────────────────────────────────────────────
# When you run: python ui.py  — this calls run() to start the dashboard
if __name__ == '__main__':
    run()
