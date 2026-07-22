## imports modules for game functionality - this file is the heart of the game! ##
import os
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

def load_regions(images_dir): # 'regions' directory management - loads regions for the classic 'Wakguessr' gamemode
    data = {}
    for region in os.listdir(images_dir):
        region_path = os.path.join(images_dir, region)
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

def load_monsters(monsters_dir, selected_types): # 'monsters' directory management - loads monsters for the (WIP) 'Monster Guesser' gamemode - also includes switches/toggles for variation depending on player preference!
    data = {}
    type_map = {
        "Regular": "regular",
        "Dominant": "dominant",
        "Archmonster": "archmonster"
    }
    for family in os.listdir(monsters_dir):
        family_path = os.path.join(monsters_dir, family)
        if not os.path.isdir(family_path):
            continue
        for monster_type, folder_name in type_map.items():
            if monster_type not in selected_types:
                continue
            type_path = os.path.join(family_path, folder_name)
            if not os.path.isdir(type_path):
                continue
            images = [
                os.path.join(type_path, file)
                for file in os.listdir(type_path)
                if file.endswith(".png")
            ]
            for image in images:
                name = os.path.splitext(os.path.basename(image))[0]
                data[name] = [image]

    return data

def load_items(items_dir, selected_rarities): # 'items' directory management - loads items for the (WIP) 'Item Guesser' gamemode - includes switches/toggles as well!
    data = {}
    for rarity in selected_rarities:
        rarity_path = os.path.join(items_dir, rarity)
        if not os.path.isdir(rarity_path):
            continue
        for file in os.listdir(rarity_path):
            if file.endswith(".png"):
                name = os.path.splitext(file)[0]
                data[name] = [os.path.join(rarity_path, file)]

    return data

def show_game(window, gamemode, gameplay_mode, selected, dirs, on_menu): # the core. shows the actual game and has all its other features like Streaks and Timer
    ## loads the right data based on the gamemode and selected options ##
    if gamemode == "Wakguessr":
        data = load_regions(dirs["regions"])
    elif gamemode == "Monster Guesser":
        data = load_monsters(dirs["monsters"], selected)
    else:
        data = load_items(dirs["items"], selected)

    ## gameplay mode settings ##
    if gameplay_mode == "standard":
        total_rounds = 10
        timer_duration = 30
    elif gameplay_mode == "against_the_clock":
        total_rounds = 15
        timer_duration = 60
    else:   # endless
        total_rounds = None
        timer_duration = None

    ## state ##
    score = [0]
    rounds = [0]
    streak = [0]
    best_streak = [0]
    answered = [False]
    current_answer = [None]
    time_left = [timer_duration]
    timer_job = [None]
    image_queue = []
    game_over = [False]

    def build_queue(): # builds a queue of images that are then later shuffled in a random order - this essentially avoids duplicates within the same session
        queue = []
        for name, images in data.items():
            for image in images:
                queue.append((name, image))
        random.shuffle(queue)
        image_queue.clear()
        image_queue.extend(queue)

    def show_info(): # shows a messagebox for more info ONLY on the 'Wakguessr' gamemode!
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Guessing information",
            "The Wakguessr gamemode uses a Region → Subregion format.\n\n"
            "For example, if you see a picture of Astrub Mountains,\n" \
            "the correct answer is 'Astrub Mountains', not just 'Astrub'.\n\n"
            "Also, while Mines are separated in-game, they are not in Wakguessr.\n\n"
            "For example, 'Bonta Mines' will always be the correct answer, no matter which side of the Mines is being shown.\n\n"
            "Have fun!")

    def show_image(image_path): # shows the image on the game screen
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    def start_round(skip=False): # starts the game session. also displays or hides other text labels like Streak, Rounds and Feedback depending on the conditions and gamemode chosen
        if game_over[0]:
            return
        if skip and not answered[0]:
            answered[0] = True
            rounds[0] += 1
            streak[0] = 0
            streak_label.config(text="Streak: 0")
            feedback_label.config(text=f"Skipped! The correct answer was: {current_answer[0]}", bootstyle=WARNING)
            score_label.config(text=f"Score: {score[0]}/{rounds[0]}")
            if total_rounds and rounds[0] >= total_rounds:
                window.after(1250, lambda: show_results())
                return
        if not image_queue: # builds an image queue when there isn't one - essentially builds one when a new game session is started
            build_queue()
        name, image_path = image_queue.pop(0)
        current_answer[0] = name
        answered[0] = False
        show_image(image_path)
        answer_entry.delete(0, END)
        if gameplay_mode != "against_the_clock":
            feedback_label.config(text="")
        if total_rounds:
            round_label.config(text=f"Round: {rounds[0] + 1}/{total_rounds}")
        if gameplay_mode == "standard":
            start_timer()

    def start_timer(): # starts the timer. changes functionality if Against The Clock was the gameplay mode chosen.
        if timer_job[0] is not None:
            window.after_cancel(timer_job[0])
        if gameplay_mode == "against_the_clock":
            pass
        else:
            time_left[0] = timer_duration
        timer_label.config(text=f"Time left: {time_left[0]}")
        timer_job[0] = window.after(1000, update_timer)

    def update_timer(): # updates the timer each second - also changes color depending on how much time is left
        if time_left[0] > 0:
            time_left[0] -= 1
            timer_label.config(text=f"Time left: {time_left[0]}")
            if time_left[0] > 10:
                timer_label.config(bootstyle=INFO)
            elif time_left[0] > 5:
                timer_label.config(bootstyle=WARNING)
            else:
                timer_label.config(bootstyle=DANGER)
            timer_job[0] = window.after(1000, update_timer)
        else: # ends the game if the timer reaches zero
            game_over[0] = True
            streak[0] = 0
            streak_label.config(text="Streak: 0")
            timer_label.config(text="Time's up!")
            answered[0] = True
            rounds[0] += 1
            feedback_label.config(text=f"Time's up! The correct answer was: {current_answer[0]}", bootstyle=DANGER)
            score_label.config(text=f"Score: {score[0]}/{rounds[0]}")
            if total_rounds and rounds[0] >= total_rounds:
                window.after(1250, lambda: show_results())
            elif gameplay_mode == "against_the_clock":
                window.after(1250, lambda: show_results())

    def submit_answer(): # checks if the answer is valid and correct. increases streak if correct, checks if the input field is empty, uses 'strip' and 'lower' to remove blankspaces and disregard capitalization, respectively
        if answered[0] or game_over[0]:
            return
        guess = answer_entry.get()
        if not guess.strip():
            feedback_label.config(text="Please enter a guess first.", bootstyle=DANGER)
            return
        if gameplay_mode != "against_the_clock":
            if timer_job[0] is not None:
                window.after_cancel(timer_job[0])
        answered[0] = True
        rounds[0] += 1
        if guess.strip().lower() == current_answer[0].strip().lower(): # increases score and streak if answer is correct. yay!
            score[0] += 1
            streak[0] += 1
            if streak[0] > best_streak[0]:
                best_streak[0] = streak[0]
            feedback_label.config(text="Correct!", bootstyle=SUCCESS)
            if gameplay_mode == "against_the_clock":
                score_label.config(text=f"Score: {score[0]}/{rounds[0]}")
                streak_label.config(text=f"Streak: {streak[0]}")
                if total_rounds and rounds[0] >= total_rounds: # ends game if maximum rounds are reached (10 for Standard, 15 for Against The Clock)
                    game_over[0] = True
                    window.after(1250, lambda: show_results())
                    return
                start_round()
                return
        else: # checks if the answer is wrong with some additional feedback like setting the streak back to zero - still deciding whether to remove 'current_answer' from the feedback or not. chud life
            streak[0] = 0
            feedback_label.config(text=f"Wrong! The correct answer was: {current_answer[0]}. Your streak has been lost.", bootstyle=DANGER)
            if gameplay_mode == "against_the_clock":
                score_label.config(text=f"Score: {score[0]}/{rounds[0]}")
                streak_label.config(text=f"Streak: {streak[0]}")
                if total_rounds and rounds[0] >= total_rounds:
                    game_over[0] = True
                    window.after(1250, lambda: show_results())
                    return
                start_round()
                return
        score_label.config(text=f"Score: {score[0]}/{rounds[0]}")
        streak_label.config(text=f"Streak: {streak[0]}")
        if total_rounds and rounds[0] >= total_rounds:
            game_over[0] = True
            round_label.config(text="")
            if gameplay_mode != "against_the_clock":
                if timer_job[0] is not None:
                    window.after_cancel(timer_job[0])
            window.after(1250, lambda: show_results())

    def show_results(): # shows results once a game session is over!
        if timer_job[0] is not None:
            window.after_cancel(timer_job[0])
        on_menu(score[0], rounds[0], best_streak[0])

    ## builds the game UI - includes buttons and labels that can change depending on the gameplay mode ##
    frame = ttk.Frame(window)

    ttk.Label(frame, text=gamemode, font=("Arial", 24, "bold"), bootstyle=PRIMARY).pack(pady=10) # gamemode label

    image_label = ttk.Label(frame) # image label. The home of image :)
    image_label.pack(pady=10)

    answer_entry = ttk.Entry(frame, width=50) # answer entry field
    answer_entry.pack(pady=5)
    window.bind("<Return>", lambda event: start_round() if answered[0] else submit_answer())

    feedback_label = ttk.Label(frame, text="") # shows the feedback when an answer is entered
    feedback_label.pack(pady=5)

    score_label = ttk.Label(frame, text="Score: 0", font=("Arial", 12)) # score label. you know, keeps track of current score and such
    score_label.pack(pady=5)

    if gameplay_mode != "endless": # checks if the selected game mode was 'Endless' or not - hides timer if No, displays timer if Yes
        timer_label = ttk.Label(frame, text=f"Time: {timer_duration}", font=("Arial", 10), bootstyle=INFO)
        timer_label.pack(pady=5)
    else:
        timer_label = ttk.Label(frame, text="")

    round_label = ttk.Label(frame, text="", font=("Arial", 10)) # round label. keeps track of current / last round
    round_label.pack(pady=5)

    streak_label = ttk.Label(frame, text="Streak: 0", font=("Arial", 10)) # streak label. Keeps track of your streak, probably. Depends on the mood
    streak_label.pack(pady=5)

    ## frame configuration for the Info button ##
    bottom_frame = ttk.Frame(frame)
    bottom_frame.pack(side=BOTTOM, fill=X, pady=5, padx=10)

    left_frame = ttk.Frame(bottom_frame)
    left_frame.pack(side=LEFT, expand=True, fill=X)

    center_frame = ttk.Frame(bottom_frame)
    center_frame.pack(side=LEFT, expand=True, fill=X)

    right_frame = ttk.Frame(bottom_frame)
    right_frame.pack(side=LEFT, expand=True, fill=X)

    if gamemode == "Wakguessr": # displays the Info button ONLY for the 'Wakguessr' gamemode - and configures the placement of others
        ttk.Button(left_frame, text="ℹ Info", command=show_info, bootstyle=INFO).pack(side=LEFT)

    ttk.Button(center_frame, text="Exit", command=show_results, bootstyle=DANGER).pack(side=LEFT, padx=160)

    ttk.Button(frame, text="Submit", command=submit_answer, bootstyle=SUCCESS).pack(pady=5)

    if gameplay_mode == "standard":
        ttk.Button(frame, text="Skip", command=lambda: start_round(skip=True), bootstyle=WARNING).pack(pady=5)

    build_queue()
    if gameplay_mode == "against_the_clock":
        start_timer()
    start_round()

    return frame