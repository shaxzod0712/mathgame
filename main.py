import tkinter as tk
from random import randint
import os

class AddGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Olovli Qo‘shish O‘yini 🔥")
        self.root.geometry("360x640")  # Telefon o‘lchami 9:16
        self.root.config(bg="#121212")

        # Natijalar
        self.reset_game()
        self.high_score = self.load_high_score()

        self.create_widgets()
        self.new_question()
        self.update_timer()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.time_left = 30
        self.game_over = False

    def create_widgets(self):
        # Sarlavha
        self.title_label = tk.Label(
            self.root, text="🔥 OLUVLI MATEMATIKA 🔥",
            font=("Helvetica", 16, "bold"),
            fg="#ff9800", bg="#121212"
        )
        self.title_label.pack(pady=15)

        # Taymer
        self.timer_label = tk.Label(
            self.root, text="⏳ 30", font=("Helvetica", 15, "bold"),
            fg="#00e5ff", bg="#121212"
        )
        self.timer_label.pack()

        # Level
        self.level_label = tk.Label(
            self.root, text="📊 Level: 1",
            font=("Helvetica", 12), bg="#121212", fg="#90caf9"
        )
        self.level_label.pack(pady=5)

        # Savol
        self.question_label = tk.Label(
            self.root, text="", font=("Helvetica", 22, "bold"),
            fg="white", bg="#121212"
        )
        self.question_label.pack(pady=25)

        # Javob maydoni
        self.answer_entry = tk.Entry(
            self.root, font=("Helvetica", 18), justify='center',
            bg="#1f1f1f", fg="white", insertbackground="white"
        )
        self.answer_entry.pack(pady=10, ipadx=5, ipady=8)
        self.answer_entry.bind("<Return>", self.check_answer)

        # Tekshirish tugmasi
        self.check_button = tk.Button(
            self.root, text="✅ Tekshirish", font=("Helvetica", 13, "bold"),
            command=self.check_answer, bg="#388e3c", fg="white",
            relief="flat", width=15, height=2
        )
        self.check_button.pack(pady=10)

        # Fikr-mulohaza
        self.feedback_label = tk.Label(
            self.root, text="", font=("Helvetica", 14),
            bg="#121212", fg="yellow"
        )
        self.feedback_label.pack(pady=10)

        # Ballar
        self.score_label = tk.Label(
            self.root, text=f"✅ To‘g‘ri: 0", font=("Helvetica", 13),
            bg="#121212", fg="lightgreen"
        )
        self.score_label.pack(pady=5)

        # Rekord
        self.highscore_label = tk.Label(
            self.root, text=f"🏆 Rekord: {self.high_score}",
            font=("Helvetica", 13), bg="#121212", fg="#ffd600"
        )
        self.highscore_label.pack(pady=5)

        # Tugmalar paneli
        self.buttons_frame = tk.Frame(self.root, bg="#121212")
        self.buttons_frame.pack(pady=20)

        self.restart_button = tk.Button(
            self.buttons_frame, text="🔄 Qayta o‘ynash", font=("Helvetica", 13, "bold"),
            command=self.restart_game, bg="#1976d2", fg="white",
            relief="flat", width=12, height=2
        )
        self.restart_button.grid(row=0, column=0, padx=10)

        self.exit_button = tk.Button(
            self.buttons_frame, text="🚪 Chiqish", font=("Helvetica", 13, "bold"),
            command=self.root.destroy, bg="#d32f2f", fg="white",
            relief="flat", width=12, height=2
        )
        self.exit_button.grid(row=0, column=1, padx=10)

    def new_question(self):
        if self.game_over:
            return
        # Levelga qarab murakkablik
        if self.level == 1:
            max_num = 20
        elif self.level == 2:
            max_num = 100
        else:
            max_num = 999

        # Faqat qo‘shish
        self.a = randint(1, max_num)
        self.b = randint(1, max_num)
        self.correct_answer = self.a + self.b

        self.question_label.config(text=f"{self.a} + {self.b} = ?")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

    def check_answer(self, event=None):
        if self.game_over:
            return

        user_input = self.answer_entry.get()

        if not user_input.strip() or not user_input.isdigit():
            self.feedback_label.config(text="⚠️ Faqat raqam kiriting.")
            return

        user_answer = int(user_input)

        if user_answer == self.correct_answer:
            self.score += 1
            self.feedback_label.config(text="✅ To‘g‘ri!", fg="lightgreen")
            self.score_label.config(text=f"✅ To‘g‘ri: {self.score}")
            if self.score % 5 == 0:
                self.level += 1
                self.level_label.config(text=f"📊 Level: {self.level}")
            self.root.after(800, self.new_question)
        else:
            self.end_game("❌ Xato javob")

    def update_timer(self):
        if self.game_over:
            return
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"⏳ {self.time_left}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game("⏰ Vaqt tugadi")

    def end_game(self, reason="O‘yin tugadi"):
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        # Savol o‘rniga natija chiqarish
        self.question_label.config(text=reason)
        self.feedback_label.config(
            text=f"✅ To‘g‘ri: {self.score}   🏆 Rekord: {self.high_score}",
            fg="orange"
        )

    def restart_game(self):
        self.reset_game()
        self.level_label.config(text="📊 Level: 1")
        self.score_label.config(text="✅ To‘g‘ri: 0")
        self.timer_label.config(text="⏳ 30")
        self.feedback_label.config(text="")
        self.question_label.config(text="")
        self.new_question()
        self.update_timer()
        self.game_over = False

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))


# Dastur ishga tushishi
if __name__ == "__main__":
    root = tk.Tk()
    app = AddGameApp(root)
    root.mainloop()
