from tkinter import *
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps

    reps = 0
    tick_mark_label.config(text="")
    window.after_cancel(timer)
    title_label.config(text="\nTimer", fg=GREEN)
    canvas_t.itemconfig(timer_text, text="00:00")


# ---------------------------- TIMER MECHANISM ------------------------------- #

def init_timer():
    if timer is not None:
        reset_timer()
    start_timer()


def start_timer():
    global reps

    reps += 1
    multiplier = 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * multiplier)
        title_label.config(text="Long\nbreak", fg=RED)
        reps = 0
    elif reps % 2 == 1:
        count_down(WORK_MIN * multiplier)
        title_label.config(text="\nWORK", fg=GREEN)
    else:
        count_down(SHORT_BREAK_MIN * multiplier)
        title_label.config(text="Short\nbreak", fg=PINK)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    countdown_text = f"{count_min}:{count_sec}"
    canvas_t.itemconfig(timer_text, text=countdown_text)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            lab_text = tick_mark_label.cget("text") + "✓ "
            tick_mark_label.config(text=lab_text)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas_t = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas_t.create_image(100, 112, image=tomato_img)
timer_text = canvas_t.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas_t.grid(row=1, column=1)

title_label = Label(text="\nTimer", font=(FONT_NAME, 40, "bold"), highlightthickness=0, fg=GREEN, bg=YELLOW)
title_label.grid(row=0, column=1)

# Start_button

start_button = Button(text="Start", font=(FONT_NAME, 25, "bold"), highlightthickness=0, command=init_timer)
start_button.grid(row=2, column=0, sticky="e")

# Reset_button

reset_button = Button(text="Reset", font=(FONT_NAME, 25, "bold"), highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2, sticky="w")

tick_mark_label = Label(font=(FONT_NAME, 25, "bold"), highlightthickness=0, fg=GREEN, bg=YELLOW)
tick_mark_label.grid(row=3, column=1)

window.mainloop()
