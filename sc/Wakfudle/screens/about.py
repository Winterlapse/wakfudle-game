## imports webbrowser and ttk modules for about screen functionality ##
import webbrowser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def open_link(url): # used for linking the GitHub and Forums post webpages at the bottom
    webbrowser.open(url)

def show_about(window, on_back): # the about screen! whoa!
    frame = ttk.Frame(window)

    ttk.Label(frame, text="About Wakfudle", font=("Arial", 28, "bold"), bootstyle=PRIMARY).pack(pady=20)

    about_text = (
        "Wakfudle is a fan-made guessing game built around the world of Wakfu.\n\n"
        "How to play:\n"
        "Choose a gamemode and a gameplay mode, then guess what's\n"
        "shown on screen based on the image.\n"
        "Type your answer and press Enter to submit.\n\n"
        "In Standard mode you have 30 seconds per round, you play a\n"
        "maximum of 10 rounds.\n\n"
        "In Against The Clock you have 60 seconds total, you play a\n"
        "maximum of 15 rounds.\n"
        "You have to guess as many as you can before the time runs out.\n\n"
        "In Endless mode you play until you decide to stop.\n\n"
        "DISCLAIMER:\n"
        "This is a fan-made project created purely for entertainment.\n"
        "All images, assets, and intellectual property shown in this\n"
        "program belong to Ankama and the Wakfu development team.\n"
        "This project is not affiliated with or endorsed by Ankama\n"
        "in any way.\n\n"
        "If you have any feedback or would like to report bugs,\n"
        "please contact me on Discord at .wistfulheart\n\n"
        "NOTE:\n"
        "This program is still in development, and more features will\n"
        "be added in the future.\n"
        "This program is free and open-source, and you can find it at\n"
        "my GitHub repository linked at the bottom of this window.\n"
        "Do not trust any websites other than my GitHub repository.\n"
        "It's the only official source to download this program.\n"
    )

    ttk.Label(frame, text=about_text, font=("Arial", 11), justify=LEFT).pack(pady=10, padx=30) # displays the text right above

    links_frame = ttk.Frame(frame) # frame containing the two links
    links_frame.pack(pady=5)

    github_link = ttk.Label(links_frame, text="GitHub Repo", font=("Arial", 11, "underline"), bootstyle=PRIMARY, cursor="hand2") # GitHub link label
    github_link.pack(side=LEFT, padx=10)
    github_link.bind("<Button-1>", lambda e: open_link("https://github.com/Winterlapse/wakfudle-game"))

    ttk.Button(frame, text="Back", width=20, bootstyle=SECONDARY, command=on_back).pack(pady=20)

    return frame