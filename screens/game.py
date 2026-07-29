## imports modules for game functionality - this file is the heart of the game! ##
import os
import json
import random
import string
import customtkinter as ctk
from PIL import Image

## message list - these will be randomly selected to appear under the image label in a game session (Wakguessr or Monster Guesser, respectively) ##
WAKGUESSR_MESSAGES = [
    "I know this one!",
    "Looks four meal your... or something like that.",
    "I've seen this before. Maybe.",
    "I'm thinking I should give you a hint, but I don't really feel like it. Sorry.",
    "There's probably a Dofus hidden somewhere...",
    "I'll give you a hint. This one's in the World of Twelve.",
    "One gobball, two gobballs, three gobballs...",
    "Even Ogrest doesn't know where this is.",
    "Completely unrelated but, how do you feel about Castorbitals?",
    "Joris would know this one.",
    "Is that a Bow Meow in the corner?",
    "If you look close enough you might be able to get it.",
    "You know, Raeliss is a really nice and friendly guy. You should get to know him someday.",
    "What a beautiful place! Let me bring my buddy Nox to decimate everything.",
    "Not even Kerubim has been here. That's because he's lazy.",
    "Negi would like this place.",
    "Someone told me a certain Whisperer really likes capybaras.",
    "If you get this one right you might identify an item with four white slots tomorrow. Not quite sure what that means, though.",
    "This place would look a hundred times better with some Bellaphones wandering around.",
    "Sire Flexington hates this place. He said he would make it more 'purple' if he could... Not really sure what that means.",
    "Hey so uh... You come here often?",
    "Remember to stay hydrated. You could be sent to Ohwymi.",
    "There could be a Sram completely hidden here and you wouldn't know.",
    "Eltiskuterie spent his vacation days here. Some say he never came back, though.",
    "Maybe try asking the locals?",
    "This place is so unknown you couldn't even see it from the top of Mount Zinit."
]

MONSTER_MESSAGES = [
    "Is that a Gobball? Maybe not.",
    "You could probably give this one a headpat, if you were brave enough.",
    "I wouldn't want to meet this one in a dungeon.",
    "Even Joris would run from this one.",
    "This one looks friendly. Probably.",
    "I hear this monster drops something good.",
    "What's the name of this awful guy?",
    "What a cute lil' guy! Let's grab him and put him in the Haven Paddock.",
    "Pretty sure I've seen this one wandering around at the central park a few days ago.",
    "Even Rushu thinks this one looks terrifying.",
    "What a majestic creature.",
    "I can sense some evilness in this one.",
    "I can sense some kindness in this one.",
    "I can sense some sadness in this one.",
    "Would you hug it for five million kamas? Six? Se-, nevermind.",
    "I think I saw this guy just standing still in front of the Sufokia marketplace. Not really sure what he was doing.",
    "I couldn't imagine living the life of whatever this thing is. Must really be miserable.",
    "Did Osamodas even approve of the existence of this thing?",
    "Would you rather have 2 kamas... or 1 kama? Both are being stolen by a greedy Drheller anyway.",
    "I wonder if Stompion and this guy are siblings.",
]

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
                        if key not in data:
                            data[key] = []
                        for image in images:
                            data[key].append({"display": image, "reveal": None})
    return data

def load_monsters(monsters_dir, selected_types, mode): # 'monsters' directory management - loads monsters for the (WIP) 'Monster Guesser' gamemode - also includes switches/toggles for variation depending on player preference!
    data = {}
    type_map = {
        "Regular": "regular",
        "Dominants": "dominant",
        "Archmonsters": "archmonster",
        "Intervention Bosses": "interventionbosses",
        "Ultimate Bosses": "ultimatebosses"
    }
    subfolder = "silhouette" if mode == "Silhouette" else "normal" # searches for silhouette images if Silhouette image mode was selected

    for family in os.listdir(monsters_dir):
        family_path = os.path.join(monsters_dir, family)
        if not os.path.isdir(family_path):
            continue
        for monster_type, folder_name in type_map.items():
            if monster_type not in selected_types:
                continue
            type_path = os.path.join(family_path, folder_name, subfolder)
            if not os.path.isdir(type_path):
                continue
            for file in os.listdir(type_path):
                if not file.endswith(".png"):
                    continue
                name = os.path.splitext(file)[0]
                if name.startswith("S_"):
                    name = name[2:]
                silhouette_path = os.path.join(type_path, file)
                # find matching normal image
                normal_path = os.path.join(family_path, folder_name, "normal", f"{name}.png")
                data[name] = {
                    "display": silhouette_path if mode == "Silhouette" else normal_path,
                    "reveal": normal_path if mode == "Silhouette" else None
                }
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
                data[name] = {"display": os.path.join(rarity_path, file), "reveal": None}
    return data

def load_silhouette_groups(data_dir): # loads silhouette groups - used for monsters with identical silhouettes
    groups_path = os.path.join(data_dir, "silhouette_groups.json")
    if os.path.exists(groups_path):
        with open(groups_path, "r") as f:
            return json.load(f)
    return []

def load_normal_groups(data_dir): # loads normal groups - used for monsters with identical sprites (colors and shape)
    groups_path = os.path.join(data_dir, "normal_groups.json")
    if os.path.exists(groups_path):
        with open(groups_path, "r") as f:
            return json.load(f)
    return []

def show_game(window, gamemode, gameplay_mode, selected, mode, dirs, on_menu): # the core. shows the actual game and has all its other features like Streaks and Timer
    ## loads the right data based on the gamemode and selected options ##
    if gamemode == "Wakguessr":
        data = load_regions(dirs["regions"])
    elif gamemode == "Monster Guesser":
        data = load_monsters(dirs["monsters"], selected, mode)
    else:
        data = load_items(dirs["items"], selected)

    if gamemode == "Monster Guesser":
        if mode == "Silhouette":
            silhouette_groups = load_silhouette_groups(os.path.dirname(dirs["monsters"]))
        else:
            silhouette_groups = load_normal_groups(os.path.dirname(dirs["monsters"]))
    else:
        silhouette_groups = []

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

    ## state variables! ##
    score = [0]
    rounds = [0]
    streak = [0]
    best_streak = [0]
    answered = [False]
    current_answer = [None]
    current_paths = [None]
    time_left = [timer_duration]
    timer_job = [None]
    elapsed = [0]
    elapsed_job = [None]
    image_queue = []
    game_over = [False]

    def build_queue(): # builds a queue of images that are then later shuffled in a random order - this essentially avoids duplicates within the same session
        queue = []
        for name, paths_list in data.items():
            if isinstance(paths_list, list):
                for paths in paths_list:
                    queue.append((name, paths))
            else:
                queue.append((name, paths_list))
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
            "For example, 'Bonta Mines' will be the correct answer, no matter which part (Galleries or Depths) of the Mines is being shown.\n\n"
            "Have fun!")

    def show_image(image_path): # shows the image on the game screen
        image = Image.open(image_path)

        # creates rounded corners for the images
        radius = 15
        mask = Image.new("L", image.size, 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

        rounded = Image.new("RGBA", image.size, (0, 0, 0, 0)) # gives the image rounded corners
        rounded.paste(image, mask=mask)

        ctk_image = ctk.CTkImage(light_image=rounded, dark_image=rounded, size=(image.width, image.height))
        image_label.configure(image=ctk_image)
        image_label.image = ctk_image

    def start_round(skip=False): # starts the game session. also displays or hides other text labels like Streak, Rounds and Feedback depending on the conditions and gamemode chosen
        if game_over[0]:
            return
        if skip and not answered[0]:
            answered[0] = True
            rounds[0] += 1
            streak[0] = 0
            streak_label.configure(text="Streak: 0")
            feedback_label.configure(text=f"Skipped! The correct answer was: {current_answer[0]}", text_color="orange")
            score_label.configure(text=f"Score: {score[0]}/{rounds[0]}")
            if total_rounds and rounds[0] >= total_rounds:
                game_over[0] = True
                window.after(1250, lambda: show_results())
                return
        if not image_queue: # builds an image queue when there isn't one - essentially builds one when a new game session is started
            build_queue()
        name, paths = image_queue.pop(0)
        current_answer[0] = name
        current_paths[0] = paths
        answered[0] = False
        show_image(paths["display"])
        messages = MONSTER_MESSAGES if gamemode == "Monster Guesser" else WAKGUESSR_MESSAGES
        message_label.configure(text=random.choice(messages))
        answer_entry.focus()
        answer_entry.delete(0, "end")
        shortcut_label.configure(text="")
        if gameplay_mode != "against_the_clock":
            feedback_label.configure(text="")
        if total_rounds:
            round_label.configure(text=f"Round: {rounds[0] + 1}/{total_rounds}")
        if gameplay_mode == "standard":
            start_timer()

    def start_timer(): # starts AND restarts the timer each round in Standard mode. changes functionality if Against The Clock was chosen
        if timer_job[0] is not None:
            window.after_cancel(timer_job[0])
        if gameplay_mode == "against_the_clock":
            pass
        else:
            time_left[0] = timer_duration
        timer_label.configure(text=f"Time left: {time_left[0]}")
        timer_job[0] = window.after(1000, update_timer)

    def update_timer(): # updates the timer each second - also changes color depending on how much time is left
        if time_left[0] > 0:
            time_left[0] -= 1
            timer_label.configure(text=f"Time left: {time_left[0]}")
            if time_left[0] > 10:
                timer_label.configure(text_color="#1f6aa5")
            elif time_left[0] > 5:
                timer_label.configure(text_color="orange")
            else:
                timer_label.configure(text_color="red")
            timer_job[0] = window.after(1000, update_timer)
        else: # ends the game if the timer reaches zero
            streak[0] = 0
            streak_label.configure(text="Streak: 0")
            timer_label.configure(text="Time's up!")
            answered[0] = True
            rounds[0] += 1
            feedback_label.configure(text=f"Time's up! The correct answer was: {current_answer[0]}", text_color="red")
            score_label.configure(text=f"Score: {score[0]}/{rounds[0]}")
            if total_rounds and rounds[0] >= total_rounds:
                game_over[0] = True
                window.after(1250, lambda: show_results())
            elif gameplay_mode == "against_the_clock":
                game_over[0] = True
                window.after(1250, lambda: show_results())

    def update_elapsed(): # updates time elapsed label (only for endless mode)
        elapsed[0] += 1
        minutes = elapsed[0] // 60
        seconds = elapsed[0] % 60
        elapsed_label.configure(text=f"Time elapsed: {minutes:02d}:{seconds:02d}")
        elapsed_job[0] = window.after(1000, update_elapsed)

    def submit_answer(): # checks if the answer is valid and correct. increases streak if correct, checks if the input field is empty, uses 'strip' and 'lower' to remove blankspaces and disregard capitalization, respectively
        if answered[0] or game_over[0]:
            return
        guess = answer_entry.get()
        if not guess.strip():
            feedback_label.configure(text="Please enter a guess first.", text_color="red")
            return
        if gameplay_mode != "against_the_clock":
            if timer_job[0] is not None:
                window.after_cancel(timer_job[0])
        answered[0] = True
        rounds[0] += 1
        shortcut_label.configure(text="Press Enter to continue.")
        if mode == "Silhouette" and current_paths[0] and current_paths[0]["reveal"]:
            show_image(current_paths[0]["reveal"])
        if normalize(guess) == normalize(current_answer[0]) or (gamemode == "Monster Guesser" and is_pity_match(guess, current_answer[0])): # increases score and streak if answer is correct. also disregards punctuation characters from answer submission
            score[0] += 1
            streak[0] += 1
            if streak[0] > best_streak[0]:
                best_streak[0] = streak[0]
            feedback_label.configure(text="Correct!", text_color="green")
            if gameplay_mode == "against_the_clock":
                score_label.configure(text=f"Score: {score[0]}/{rounds[0]}")
                streak_label.configure(text=f"Streak: {streak[0]}")
                if total_rounds and rounds[0] >= total_rounds: # ends game if maximum rounds are reached (10 for Standard, 15 for Against The Clock)
                    game_over[0] = True
                    window.after(1250, lambda: show_results())
                    return
                start_round()
                return
        else: # checks if the answer is wrong with some additional feedback like setting the streak back to zero
            streak[0] = 0
            feedback_label.configure(text=f"Wrong! The correct answer was: {current_answer[0]}. Your streak has been lost.", text_color="red")
            if gameplay_mode == "against_the_clock":
                score_label.configure(text=f"Score: {score[0]}/{rounds[0]}")
                streak_label.configure(text=f"Streak: {streak[0]}")
                if total_rounds and rounds[0] >= total_rounds:
                    game_over[0] = True
                    window.after(1250, lambda: show_results())
                    return
                start_round()
                return
        score_label.configure(text=f"Score: {score[0]}/{rounds[0]}")
        streak_label.configure(text=f"Streak: {streak[0]}")
        if total_rounds and rounds[0] >= total_rounds:
            game_over[0] = True
            round_label.configure(text="")
            if gameplay_mode != "against_the_clock":
                if timer_job[0] is not None:
                    window.after_cancel(timer_job[0])
            window.after(1250, lambda: show_results())

    def show_results(): # shows results once a game session is over and cancels timer for it to get reset when a new game is started
        if timer_job[0] is not None:
            window.after_cancel(timer_job[0])
        if elapsed_job[0] is not None:
            window.after_cancel(elapsed_job[0])
        on_menu(score[0], rounds[0], best_streak[0])

    def normalize(text): # function to normalize answer submissions - disregards punctuation characters like commas, periods and apostrophes
        text = text.strip().lower()
        text = text.replace("-", " ")
        text = text.translate(str.maketrans("", "", "',.:;"))
        return text

    def is_pity_match(guess, correct): # pity system for silhouette mode. if two or more mobs are in the same group due to identical silhouettes, guessing either of them will be deemed as correct
        normalized_guess = normalize(guess)
        normalized_correct = normalize(correct)
        for group in silhouette_groups:
            normalized_group = [normalize(g) for g in group]
            if normalized_correct in normalized_group and normalized_guess in normalized_group:
                return True
        return False

    def confirm_exit(): # triggers a confirmation messagebox when the player clicks to leave mid game
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Quit", "Are you sure you want to quit? You will be sent back to the main menu and your progress will be lost."):
            show_results()

    ## builds the game UI - main frame ##
    frame = ctk.CTkFrame(window)

    ## title at the top ##
    ctk.CTkLabel(frame, text=gamemode, font=("Arial", 24, "bold")).pack(pady=10)

    ## horizontal separator under title ##
    ctk.CTkFrame(frame, height=2, fg_color="gray30").pack(fill="x", padx=10, pady=5)

    ## two column layout ##
    columns_frame = ctk.CTkFrame(frame, fg_color="transparent")
    columns_frame.pack(fill="both", expand=True, padx=10, pady=5)

    ## left column - image ##
    left_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
    left_column.pack(side="left", fill="both", expand=True, padx=10)

    image_label = ctk.CTkLabel(left_column, text="") # image label. The home of image :)
    image_label.pack(expand=True, anchor="n", pady=(50, 0))

    message_label = ctk.CTkLabel(left_column, text=random.choice(WAKGUESSR_MESSAGES), # text label for the messages that appear under the image :)
        font=("Arial", 12, "italic"), text_color="gray", wraplength=255)
    message_label.pack(pady=(0, 120))

    ## vertical separator between columns ##
    ctk.CTkFrame(columns_frame, width=2, fg_color="gray30").pack(side="left", fill="y", pady=10)

    ## right column - labels and buttons ##
    right_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
    right_column.pack(side="left", fill="both", padx=10, pady=10)

    score_label = ctk.CTkLabel(right_column, text="Score: 0", font=("Arial", 16)) # score label. you know, keeps track of current score and such
    score_label.pack(pady=5, anchor="w")

    streak_label = ctk.CTkLabel(right_column, text="Streak: 0", font=("Arial", 14)) # streak label. Keeps track of your streak, probably. Depends on the mood
    streak_label.pack(pady=5, anchor="w")

    if gameplay_mode == "endless": # shows the time elapsed label only for endless mode
        elapsed_label = ctk.CTkLabel(right_column, text="Time elapsed: 00:00", font=("Arial", 14))
        elapsed_label.pack(pady=5, anchor="w")
    else:
        elapsed_label = ctk.CTkLabel(right_column, text="")

    round_label = ctk.CTkLabel(right_column, text="", font=("Arial", 14)) # round label. keeps track of current / last round
    round_label.pack(pady=5, anchor="w")

    if gameplay_mode != "endless": # checks if the selected game mode was 'Endless' or not - hides timer if No, displays timer if Yes
        timer_label = ctk.CTkLabel(right_column, text=f"Time: {timer_duration}", font=("Arial", 14), text_color="#1f6aa5")
        timer_label.pack(pady=5, anchor="w")
    else:
        timer_label = ctk.CTkLabel(right_column, text="")

    feedback_label = ctk.CTkLabel(right_column, text="", font=("Arial", 12), wraplength=200, height=60) # shows the feedback when an answer is entered
    feedback_label.pack(pady=5, anchor="w")

    answer_entry = ctk.CTkEntry(right_column, width=200, font=("Arial", 13), placeholder_text="Enter your answer here...") # answer entry field
    answer_entry.pack(pady=5)
    window.bind("<Return>", lambda event: start_round() if answered[0] else submit_answer())
    window.bind("<Control-s>", lambda event: start_round(skip=True) if gameplay_mode == "standard" else None)

    ctk.CTkButton(right_column, text="Submit", command=submit_answer, # submit button :)
        fg_color="green", hover_color="dark green", width=200).pack(pady=5)

    if gameplay_mode == "standard": # skip button - only displays for wakguessr in standard mode
        ctk.CTkButton(right_column, text="Skip", command=lambda: start_round(skip=True), 
            fg_color="#d4a017", hover_color="#b8860b", width=200).pack(pady=5)

    shortcut_label = ctk.CTkLabel(right_column, text="", font=("Arial", 11), text_color="gray") # text label for enter key shortcut
    shortcut_label.pack(pady=40)

    ## horizontal separator under columns ##
    ctk.CTkFrame(frame, height=2, fg_color="gray30").pack(fill="x", padx=10, pady=5 )

    ## bottom bar for Info and Exit buttons ##
    bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
    bottom_frame.pack(side="bottom", fill="x", pady=5, padx=10)

    if gamemode == "Wakguessr": # displays the Info button ONLY for the 'Wakguessr' gamemode - and configures the placement of others
        ctk.CTkButton(bottom_frame, text="i Info", width=80, command=show_info,
            fg_color="#1f6aa5", hover_color="#144d7a").pack(side="left")

    ctk.CTkButton(bottom_frame, text="Exit", command=confirm_exit, # exit button - command triggers a confirm exit messagebox prompt when clicked
        fg_color="red", hover_color="dark red", width=200).pack(side="right", padx="9")

    build_queue()
    if gameplay_mode == "against_the_clock":
        start_timer()
    if gameplay_mode == "endless":
        update_elapsed()
    start_round()

    return frame