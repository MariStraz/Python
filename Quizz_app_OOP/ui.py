from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.configure(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0)
        self.canvas_bg = Canvas(bg="white")
        self.question_text = self.canvas.create_text(150, 125,
                                                     text='Here comes the question',
                                                     width=280,
                                                     fill=THEME_COLOR,
                                                     font=('Arial', 20, 'italic'))
        self.canvas.grid(column=0, row=1, columnspan=2, padx=20, pady=20)

        self.label_score = Label(fg="white", pady=20, bg=THEME_COLOR, text="Score: 0", highlightthickness=0)
        self.label_score.grid(column=1, row=0)

        img_yes = PhotoImage(file="images/true.png")
        self.button_yes = Button(image=img_yes, bg=THEME_COLOR, highlightthickness=0, command=self.action_yes)
        self.button_yes.grid(column=0, row=2, padx=20, pady=20)

        img_no = PhotoImage(file="images/false.png")
        self.button_no = Button(image=img_no, bg=THEME_COLOR, highlightthickness=0, command=self.action_no)
        self.button_no.grid(column=1, row=2, padx=20, pady=20)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        """
        Display text of question to UI
        :return:
        """
        self.canvas.configure(bg="white")
        self.label_score.config(text=f"Score: {self.quiz.score}")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text,
                                   text=f"You've reached the end of the quiz of {len(self.quiz.question_list)} questions")
            self.button_no.config(state="disabled")
            self.button_yes.config(state="disabled")

    def action_no(self):
        """ Checks if "False/No" is correct answer and displays red/green color accordingly"""
        is_right = self.quiz.check_answer("false")
        self.change_color(is_right)

    def action_yes(self):
        """ Checks if "True/Yes" is correct answer and displays red/green color accordingly"""
        is_right = self.quiz.check_answer("true")
        self.change_color(is_right)

    def change_color(self, is_right):
        """ Changes background in correct(green)/ not correct(red) manner, after delay call next question """
        if is_right:
            self.canvas.configure(bg="green")
        else:
            self.canvas.configure(bg="red")
        self.window.after(1000, self.get_next_question)
