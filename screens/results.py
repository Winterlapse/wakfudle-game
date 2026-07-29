## imports ctk for results screen functionality ##
import customtkinter as ctk

def format_settings(gamemode, selected, mode): # formats the last settings for a cleaner look. doesn't show anything if Wakguessr was played
    if gamemode == "Wakguessr":
        return ""
    if gamemode == "Monster Guesser":
        types = ", ".join(selected) if selected else ""
        return f"{types}\nImage Mode: {mode}"
    return ", ".join(selected) if selected else ""

def show_results(window, gamemode, gameplay_mode, score, rounds, best_streak, total_rounds, selected, mode, on_menu, on_play_again): # the whole results screen! shows several text labels like your final score and best streak.
    frame = ctk.CTkFrame(window)

    ctk.CTkLabel(frame, text="Game Over!", font=("Arial", 28, "bold")).pack(pady=20)
    ctk.CTkLabel(frame, text=gamemode, font=("Arial", 16)).pack(pady=5)
    ctk.CTkLabel(frame, text=gameplay_mode.replace("_", " ").title(), font=("Arial", 14),
        text_color="gray").pack(pady=5)

    ctk.CTkLabel(frame, text=f"Final Score: {score}/{rounds}", font=("Arial", 18)).pack(pady=10)
    ctk.CTkLabel(frame, text=f"Best Streak: {best_streak}", font=("Arial", 18)).pack(pady=10)

    if rounds > 0:
        if total_rounds and score == total_rounds:
            msg, color = "Perfect Score! Well done!", "green"
        elif score == 0:
            msg, color = "Better luck next time!", "red"
        elif score >= rounds // 2:
            msg, color = "Good effort!", "#1f6aa5"
        else:
            msg, color = "Better luck next time!", "red"
    else:
        msg, color = "No rounds played.", "gray"

    ctk.CTkLabel(frame, text=msg, font=("Arial", 14), text_color=color).pack(pady=10)

    ctk.CTkFrame(frame, height=40, fg_color="transparent").pack() # spacer

    settings_text = format_settings(gamemode, selected, mode)
    if settings_text:
        ctk.CTkLabel(frame, text="Settings played:", font=("Arial", 13), text_color="gray").pack()
        ctk.CTkLabel(frame, text=settings_text, font=("Arial", 11), text_color="gray", justify="center").pack(pady=3)

    ctk.CTkFrame(frame, height=70, fg_color="transparent").pack() # spacer

    ctk.CTkButton(frame, text="Play Again", width=200, fg_color="green", hover_color="dark green", 
        command=on_play_again).pack(pady=10)
    ctk.CTkButton(frame, text="Main Menu", width=200, fg_color="gray", hover_color="dark gray",
        command=on_menu).pack(pady=5)

    return frame