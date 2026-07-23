## imports ttk for results screen functionality ##
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def show_results(window, gamemode, gameplay_mode, score, rounds, best_streak, total_rounds, on_menu, on_play_again): # the whole results screen! shows several text labels like your final score and best streak.
    frame = ttk.Frame(window)

    ttk.Label(frame, text="Game Over!", font=("Arial", 28, "bold"), bootstyle=PRIMARY).pack(pady=20)
    ttk.Label(frame, text=gamemode, font=("Arial", 16)).pack(pady=5)
    ttk.Label(frame, text=gameplay_mode.replace("_", " ").title(), font=("Arial", 14), bootstyle=SECONDARY).pack(pady=5)

    ttk.Frame(frame, height=15).pack() # spacer

    ttk.Label(frame, text=f"Final Score: {score}/{rounds}", font=("Arial", 18)).pack(pady=10)
    ttk.Label(frame, text=f"Best Streak: {best_streak}", font=("Arial", 18)).pack(pady=10)

    if rounds > 0:
        if total_rounds and score == total_rounds:
            msg, style = "Perfect Score! Well done!", SUCCESS
        elif score == 0:
            msg, style = "Better luck next time!", DANGER
        elif score >= rounds // 2:
            msg, style = "Good effort!", PRIMARY
        else:
            msg, style = "Better luck next time!", DANGER
    else:
        msg, style = "No rounds played.", SECONDARY

    ttk.Label(frame, text=msg, font=("Arial", 14), bootstyle=style).pack(pady=10)

    ttk.Frame(frame, height=75).pack() # spacer

    ttk.Button(frame, text="Play Again", command=on_play_again, bootstyle=SUCCESS, width=20).pack(pady=10)
    ttk.Button(frame, text="Main Menu", command=on_menu, bootstyle=SECONDARY, width=20).pack(pady=5)

    return frame