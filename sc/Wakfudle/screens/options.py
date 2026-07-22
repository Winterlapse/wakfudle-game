## imports ttk for options screen functionality ##
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

MONSTER_TYPES = ["Regular", "Dominant", "Archmonster"] # used for switches for the 'Monster Guesser' gamemode
ITEM_RARITIES = ["Legendary", "Epic", "Relic"] # used for switches for the 'Item Guesser' gamemode

def show_options(window, gamemode, on_back, on_start): # shows the options menu. appears when you click on a gamemode. contains the gameplay modes and switches for 'Monster Guesser' and 'Item Guesser' gamemodes
    frame = ttk.Frame(window)

    ttk.Label(frame, text=gamemode, font=("Arial", 28, "bold"), bootstyle=PRIMARY).pack(pady=20)
    ttk.Label(frame, text="Select a gameplay mode:", font=("Arial", 14)).pack(pady=10)

    ttk.Button(frame, text="Standard", width=20, bootstyle=SUCCESS,
        command=lambda: try_start("standard")).pack(pady=10)
    ttk.Button(frame, text="Against The Clock", width=20, bootstyle=WARNING,
        command=lambda: try_start("against_the_clock")).pack(pady=10)
    ttk.Button(frame, text="Endless", width=20, bootstyle=INFO,
        command=lambda: try_start("endless")).pack(pady=10)
    
    toggles = {} # toggles for the other modes!
    error_label = ttk.Label(frame, text="", bootstyle=DANGER)

    if gamemode == "Monster Guesser": # toggle panel for THIS mode
        ttk.Label(frame, text="Include:", font=("Arial", 12)).pack(pady=(20, 5))
        for monster_type in MONSTER_TYPES:
            var = ttk.IntVar(value=1)
            ttk.Checkbutton(frame, text=monster_type, variable=var,
                bootstyle="success-round-toggle").pack(pady=5)
            toggles[monster_type] = var
        error_label.pack(pady=5)

    elif gamemode == "Item Guesser": # toggle panel for THIS mode
        ttk.Label(frame, text="Include rarities:", font=("Arial", 12)).pack(pady=(20, 5))
        for rarity in ITEM_RARITIES:
            var = ttk.IntVar(value=1)
            ttk.Checkbutton(frame, text=rarity, variable=var,
                bootstyle="success-round-toggle").pack(pady=5)
            toggles[rarity] = var
        error_label.pack(pady=5)

    def try_start(gameplay_mode): # ensures that the player must select at least one option (toggle) to proceed
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