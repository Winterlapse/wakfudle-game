## imports ttk for main menu functionality :) ##
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def show_menu(window, show_about, show_options): # shows the WHOLE!!!! main menu. stuff like buttons and other text labels
    frame = ttk.Frame(window)

    ttk.Label(frame, text="Wakfudle", font=("Arial", 36, "bold"), bootstyle=PRIMARY).pack(pady=10)

    ttk.Frame(frame, height=5).pack()  # spacer

    ttk.Button(frame, text="Wakguessr", width=25, bootstyle=SUCCESS,
        command=lambda: show_options("Wakguessr")).pack(pady=10)

    ttk.Button(frame, text="Monster Guesser", width=25, bootstyle=WARNING, state=DISABLED).pack(pady=(2, 5))
    ttk.Label(frame, text="Coming soon!", font=("Arial", 9), bootstyle=SECONDARY).pack()

    ttk.Button(frame, text="Item Guesser", width=25, bootstyle=WARNING, state=DISABLED).pack(pady=(2, 5))
    ttk.Label(frame, text="Coming soon!", font=("Arial", 9), bootstyle=SECONDARY).pack()

    ttk.Frame(frame, height=150).pack()  # spacer

    ttk.Button(frame, text="About", width=20, bootstyle=SECONDARY, command=show_about).pack(pady=10)
    ttk.Button(frame, text="Exit", width=20, bootstyle=DANGER, command=window.destroy).pack(pady=10)

    ttk.Label(frame, text="v1.0.0", font=("Arial", 9), bootstyle=SECONDARY).pack(anchor=SW, pady=5, padx=10)

    return frame