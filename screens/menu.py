## imports ctk for main menu functionality :) ##
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def show_menu(window, show_about, show_options): # shows the WHOLE!!!! main menu. stuff like buttons and other text labels
    frame = ctk.CTkFrame(window)

    ctk.CTkLabel(frame, text="Wakfudle", font=("Arial", 36, "bold")).pack(pady=10)

    ctk.CTkFrame(frame, height=5, fg_color="transparent").pack()  # spacer

    ctk.CTkButton(frame, text="Wakguessr", width=200, fg_color="green", hover_color="dark green",
        command=lambda: show_options("Wakguessr")).pack(pady=10)

    ctk.CTkButton(frame, text="Monster Guesser", width=200, fg_color="gray", hover_color="gray",
        state="disabled").pack(pady=(2, 0))
    ctk.CTkLabel(frame, text="Coming soon!", font=("Arial", 10), text_color="gray").pack()

    ctk.CTkButton(frame, text="Item Guesser", width=200, fg_color="gray", hover_color="gray",
        state="disabled").pack(pady=(2, 0))
    ctk.CTkLabel(frame, text="Coming soon!", font=("Arial", 10), text_color="gray").pack()

    ctk.CTkFrame(frame, height=150, fg_color="transparent").pack()  # spacer

    ctk.CTkButton(frame, text="About", width=200, fg_color="gray", hover_color="dark gray",
        command=show_about).pack(pady=5)
    ctk.CTkButton(frame, text="Exit", width=200, fg_color="red", hover_color="dark red",
        command=window.destroy).pack(pady=5)

    ctk.CTkLabel(frame, text="v1.0.1", font=("Arial", 10), text_color="gray").pack(anchor="sw", pady=5, padx=10)

    return frame