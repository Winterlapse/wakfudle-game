import ttkbootstrap as ttk
from ttkbootstrap.constants import *

MONSTER_TYPES = ["Regular", "Dominant", "Archmonster"]
ITEM_RARITIES = ["Legendary", "Epic", "Relic"]

def show_options(window, gamemode, on_back, on_start):
    frame = ttk.Frame(window)

    ttk.Label(frame, text=gamemode, font=("Arial", 28, "bold"), bootstyle=PRIMARY).pack(pady=20)
    ttk.Label(frame, text="Select a gameplay mode:", font=("Arial", 14)).pack(pady=10)

    ttk.Button(frame, text="Standard", width=20, bootstyle=SUCCESS,
        command=lambda: try_start("standard")).pack(pady=10)
    ttk.Button(frame, text="Against The Clock", width=20, bootstyle=WARNING,
        command=lambda: try_start("against_the_clock")).pack(pady=10)
    ttk.Button(frame, text="Endless", width=20, bootstyle=INFO,
        command=lambda: try_start("endless")).pack(pady=10)
    
    toggles = {}
    error_label = ttk.Label(frame, text="", bootstyle=DANGER)

    if gamemode == "Monster Guesser":
        ttk.Label(frame, text="Include:", font=("Arial", 12)).pack(pady=(20, 5))
        for monster_type in MONSTER_TYPES:
            var = ttk.IntVar(value=1)
            ttk.Checkbutton(frame, text=monster_type, variable=var,
                bootstyle="success-round-toggle").pack(pady=5)
            toggles[monster_type] = var
        error_label.pack(pady=5)

    elif gamemode == "Item Guesser":
        ttk.Label(frame, text="Include rarities:", font=("Arial", 12)).pack(pady=(20, 5))
        for rarity in ITEM_RARITIES:
            var = ttk.IntVar(value=1)
            ttk.Checkbutton(frame, text=rarity, variable=var,
                bootstyle="success-round-toggle").pack(pady=5)
            toggles[rarity] = var
        error_label.pack(pady=5)

    def try_start(gameplay_mode):
        if toggles:
            selected = [k for k, v in toggles.items() if v.get() == 1]
            if not selected:
                error_label.config(text="Please select at least one option.")
                return
        else:
            selected = []
        on_start(gameplay_mode, selected)

    ttk.Frame(frame, height=150).pack()  # Spacer
    
    ttk.Button(frame, text="Back", width=20, bootstyle=SECONDARY,
        command=on_back).pack(pady=5)
    
    return frame