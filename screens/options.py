## imports ctk for options screen functionality ##
import customtkinter as ctk

MONSTER_TYPES = ["Regular", "Dominants", "Archmonsters", "Intervention Bosses", "Ultimate Bosses"] # used for switches for the 'Monster Guesser' gamemode
ITEM_RARITIES = ["Legendary", "Epic", "Relic"] # used for switches for the 'Item Guesser' gamemode

def show_options(window, gamemode, on_back, on_start, last_settings=None): # shows the options menu. appears when you click on a gamemode. contains the gameplay modes and switches for 'Monster Guesser' and 'Item Guesser' gamemodes
    frame = ctk.CTkFrame(window)

    scroll_frame = ctk.CTkScrollableFrame(frame)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(scroll_frame, text=gamemode, font=("Arial", 28, "bold")).pack(pady=20)
    ctk.CTkLabel(scroll_frame, text="Select a gameplay mode:", font=("Arial", 14)).pack(pady=10)

    ctk.CTkButton(scroll_frame, text="Standard", width=200, fg_color="green", hover_color="dark green",
        command=lambda: try_start("standard")).pack(pady=10)
    ctk.CTkButton(scroll_frame, text="Against The Clock", width=200, fg_color="#d4a017", hover_color="#b8860b",
        command=lambda: try_start("against_the_clock")).pack(pady=10)
    ctk.CTkButton(scroll_frame, text="Endless", width=200, fg_color="#1f6aa5", hover_color="#144d7a",
        command=lambda: try_start("endless")).pack(pady=10)
    
    toggles = {} # toggles for the other modes!
    error_label = ctk.CTkLabel(frame, text="", fg_color="red")

    if gamemode == "Monster Guesser": # toggle panel for THIS mode
        ctk.CTkLabel(scroll_frame, text="Include:", font=("Arial", 12)).pack(pady=(20, 5))

        # first row of toggles (Regular, Dominants, Archmonsters)
        row1 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row1.pack(pady=3)
        for monster_type in ["Regular", "Dominants", "Archmonsters"]:
            default = True if last_settings is None else monster_type in last_settings["selected"]
            var = ctk.BooleanVar(value=default)
            ctk.CTkSwitch(row1, text=monster_type, variable=var).pack(side="left", padx=10)
            toggles[monster_type] = var

        # second row of toggles (Intervention Bosses, Ultimate Bosses)
        row2 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row2.pack(pady=3)
        for monster_type in ["Intervention Bosses", "Ultimate Bosses"]:
            default = True if last_settings is None else monster_type in last_settings["selected"]
            var = ctk.BooleanVar(value=default)
            ctk.CTkSwitch(row2, text=monster_type, variable=var).pack(side="left", padx=10)
            toggles[monster_type] = var

        # text labels for the last settings
        ctk.CTkLabel(scroll_frame, text="Image Mode:", font=("Arial", 12)).pack(pady=(15, 5))
        default_mode = "Normal" if last_settings is None else last_settings["mode"]
        image_mode = ctk.StringVar(value=default_mode)

        # horizontal Image Mode buttons
        mode_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        mode_row.pack(pady=3)
        ctk.CTkRadioButton(mode_row, text="Normal", variable=image_mode, value="Normal").pack(side="left", padx=20)
        ctk.CTkRadioButton(mode_row, text="Silhouette", variable=image_mode, value="Silhouette").pack(side="left", padx=20)

    elif gamemode == "Item Guesser": # toggle panel for THIS mode
        ctk.CTkLabel(scroll_frame, text="Include rarities:", font=("Arial", 12)).pack(pady=(20, 5))
        for rarity in ITEM_RARITIES:
            var = ctk.BooleanVar(value=True)
            ctk.CTkSwitch(scroll_frame, text=rarity, variable=var).pack(pady=3)
            toggles[rarity] = var

    error_label = ctk.CTkLabel(scroll_frame, text="", text_color="red")
    error_label.pack(pady=5)

    def try_start(gameplay_mode): # ensures that the player must select at least one option (toggle) to proceed
        if toggles:
            selected = [k for k, v in toggles.items() if v.get()]
            if not selected:
                error_label.configure(text="Please select at least one option.")
                return
        else:
            selected = []
        mode = image_mode.get() if gamemode == "Monster Guesser" else "Normal"
        on_start(gameplay_mode, selected, mode)

    if gamemode == "Wakguessr":
        ctk.CTkFrame(scroll_frame, height=95, fg_color="transparent").pack() # spacer

    ctk.CTkButton(scroll_frame, text="Back", width=200, fg_color="gray", hover_color="dark gray",
        command=on_back).pack(pady=20)
    
    return frame