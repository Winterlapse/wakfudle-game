## imports modules and screens for game functionality ##
import os
import sys
import random
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from screens.menu import show_menu
from screens.about import show_about
from screens.options import show_options
from screens.game import show_game
from screens.results import show_results as results_screen

if getattr(sys, 'frozen', False): # 'data' folder directory management
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data") # checks for 'data' folder - returns an error messagebox if the folder is missing!
if not os.path.isdir(DATA_DIR):
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Missing Data Folder", # displays an error messagebox if the 'data' folder is missing
        "The 'data' folder could not be found.\n\n"
        "Please make sure the 'data' folder is in the same directory as Wakfudle.exe.\n"
        "If you deleted it accidentally, please redownload the program from GitHub.")
    sys.exit()

## directory management for subfolders in the 'data' folder ##
REGIONS_DIR = os.path.join(BASE_DIR, "data", "regions")
MONSTERS_DIR = os.path.join(BASE_DIR, "data", "monsters")
ITEMS_DIR = os.path.join(BASE_DIR, "data", "items")
TOTAL_ROUNDS = 10

def load_data(): # loads all data in the 'data' folder - also checks if images end with '.png'
    data = {}
    for region in os.listdir(REGIONS_DIR):
        region_path = os.path.join(REGIONS_DIR, region)
        if os.path.isdir(region_path):
            for subregion in os.listdir(region_path):
                subregion_path = os.path.join(region_path, subregion)
                if os.path.isdir(subregion_path):
                    images = [
                        os.path.join(subregion_path, file)
                        for file in os.listdir(subregion_path)
                        if file.endswith(".png")
                    ]
                    if images:
                        key = subregion.split(" - ")[-1] if " - " in subregion else subregion
                        data[key] = images
    return data

def pick_round(data): # picks random images in the 'data' folder and its subfolders
    region = random.choice(list(data.keys()))
    image = random.choice(data[region])
    return region, image

def check_answer(guess, correct): # checks if the answer is correct or incorrect - also correctly validates regardless of capitalization!
    return guess.strip().lower() == correct.strip().lower()

def show_image(image_label, image_path): # shows the selected image on the program during a game
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def main(): # all functions contained inside this one are for switching frames (windows) whenever a button is clicked - 'Results' and 'About' for example
    window = ttk.Window(themename="darkly")
    window.title("Wakfudle")
    window.minsize(600, 500)
    window.resizable(False, False)

    current_frame = [None]

    def switch_frame(new_frame): # responsible for switching from one frame to another
        if current_frame[0] is not None:
            current_frame[0].pack_forget()
        current_frame[0] = new_frame
        current_frame[0].pack(fill=BOTH, expand=True)

    def go_to_results(gamemode, gameplay_mode, score, rounds, best_streak, selected): # switches to the 'Results' window if the conditions are met
        total_rounds = 10 if gameplay_mode == "standard" else 15 if gameplay_mode == "against_the_clock" else None
        switch_frame(results_screen(window, gamemode, gameplay_mode, score, rounds, best_streak, total_rounds,
        go_to_menu,
        lambda: go_to_game(gamemode, gameplay_mode, selected)))

    def go_to_game(gamemode, gameplay_mode, selected): # switches to the actual 'Game' window. you know, where you actually play the game
        switch_frame(show_game(window, gamemode, gameplay_mode, selected, {
            "regions": REGIONS_DIR,
            "monsters": MONSTERS_DIR,
            "items": ITEMS_DIR
        }, lambda score, rounds, best_streak: go_to_results(gamemode, gameplay_mode, score, rounds, best_streak, selected)))

    def go_to_options(gamemode): # switches to the 'Options' window - the one that shows up after you select a gamemode in the Main Menu
        switch_frame(show_options(window, gamemode, go_to_menu,
            lambda gameplay_mode, selected: go_to_game(gamemode, gameplay_mode, selected)))

    def go_to_about(): # switches to the 'About' window
        switch_frame(show_about(window, go_to_menu))

    def go_to_menu(): # switches to the 'Menu' window
        switch_frame(show_menu(window, go_to_about, go_to_options))

    go_to_menu()
    window.mainloop()

if __name__ == "__main__":
    main()