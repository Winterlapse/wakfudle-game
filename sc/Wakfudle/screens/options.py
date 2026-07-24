## imports ctk for options screen functionality ##
import customtkinter as ctk

MONSTER_TYPES = ["Regular", "Dominants", "Archmonsters"] # used for switches for the 'Monster Guesser' gamemode
ITEM_RARITIES = ["Legendary", "Epic", "Relic"] # used for switches for the 'Item Guesser' gamemode

def show_options(window, gamemode, on_back, on_start): # shows the options menu. appears when you click on a gamemode. contains the gameplay modes and switches for 'Monster Guesser' and 'Item Guesser' gamemodes
    frame = ctk.CTkFrame(window)

    ctk.CTkLabel(frame, text=gamemode, font=("Arial", 28, "bold")).pack(pady=20)
    ctk.CTkLabel(frame, text="Select a gameplay mode:", font=("Arial", 14)).pack(pady=10)

    ctk.CTkButton(frame, text="Standard", width=200, fg_color="green", hover_color="dark green",
        command=lambda: try_start("standard")).pack(pady=10)
    ctk.CTkButton(frame, text="Against The Clock", width=200, fg_color="#d4a017", hover_color="#b8860b",
        command=lambda: try_start("against_the_clock")).pack(pady=10)
    ctk.CTkButton(frame, text="Endless", width=200, fg_color="#1f6aa5", hover_color="#144d7a",
        command=lambda: try_start("endless")).pack(pady=10)
    
    toggles = {} # toggles for the other modes!
    error_label = ctk.CTkLabel(frame, text="", fg_color="red")

    if gamemode == "Monster Guesser": # toggle panel for THIS mode
        ctk.CTkLabel(frame, text="Include:", font=("Arial", 12)).pack(pady=(20, 5))
        for monster_type in MONSTER_TYPES:
            var = ctk.BooleanVar(value=True)
            ctk.CTkSwitch(frame, text=monster_type, variable=var).pack(pady=3)
            toggles[monster_type] = var
        error_label.pack(pady=5)

    elif gamemode == "Item Guesser": # toggle panel for THIS mode
        ctk.CTkLabel(frame, text="Include rarities:", font=("Arial", 12)).pack(pady=(20, 5))
        for rarity in ITEM_RARITIES:
            var = ctk.BooleanVar(value=True)
            ctk.CTkSwitch(frame, text=rarity, variable=var).pack(pady=3)
            toggles[rarity] = var
        error_label.pack(pady=5)

    def try_start(gameplay_mode): # ensures that the player must select at least one option (toggle) to proceed
        if toggles:
            selected = [k for k, v in toggles.items() if v.get()]
            if not selected:
                error_label.config(text="Please select at least one option.")
                return
        else:
            selected = []
        on_start(gameplay_mode, selected)

    ctk.CTkFrame(frame, height=175, fg_color="transparent").pack()  # Spacer
    ctk.CTkButton(frame, text="Back", width=200, fg_color="gray", hover_color="dark gray",
        command=on_back).pack(pady=5)
    
    return frame