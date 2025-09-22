from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from random import randint


class AddGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        self.score = 0
        self.wrong = 0
        self.time_left = 30  # soniyada
        self.game_over = False

        # Sarlavha
        self.title_label = Label(text="🔥 Olovli Qo‘shish O‘yini 🔥", font_size=28, color=(1, 0.5, 0, 1))
        self.add_widget(self.title_label)

        # Taymer
        self.timer_label = Label(text=f"⏳ Vaqt: {self.time_left}", font_size=20)
        self.add_widget(self.timer_label)

        # Savol
        self.question_label = Label(text="", font_size=32)
        self.add_widget(self.question_label)

        # Javob kiritish
        self.answer_input = TextInput(hint_text="Javobni kiriting", multiline=False, font_size=24, input_filter="int")
        self.add_widget(self.answer_input)

        # Tekshirish tugmasi
        self.check_button = Button(text="✅ Tekshirish", font_size=22, background_color=(0, 0.6, 0, 1))
        self.check_button.bind(on_press=self.check_answer)
        self.add_widget(self.check_button)

        # Natija (feedback)
        self.feedback_label = Label(text="", font_size=20)
        self.add_widget(self.feedback_label)

        # Hisob
        self.score_label = Label(text="✅ To‘g‘ri: 0    ❌ Xato: 0", font_size=20)
        self.add_widget(self.score_label)

        # Qayta o‘ynash tugmasi
        self.restart_button = Button(text="🔄 Qayta o‘ynash", font_size=22, background_color=(0.2, 0.4, 1, 1))
        self.restart_button.bind(on_press=self.restart_game)
        self.restart_button.disabled = True
        self.add_widget(self.restart_button)

        # Yangi savol
        self.new_question()

        # Taymer ishga tushirish
        Clock.schedule_interval(self.update_timer, 1)

    def new_question(self):
        self.a = randint(1, 999)
        self.b = randint(1, 999)
        self.question_label.text = f"{self.a} + {self.b} = ?"
        self.answer_input.text = ""
        self.feedback_label.text = ""

    def check_answer(self, instance):
        if self.game_over:
            return

        user_input = self.answer_input.text.strip()

        if not user_input.isdigit():
            self.feedback_label.text = "⚠️ Iltimos, faqat son kiriting."
            return

        user_answer = int(user_input)
        correct = self.a + self.b

        if user_answer == correct:
            self.score += 1
            self.feedback_label.text = "✅ To‘g‘ri!"
            self.feedback_label.color = (0, 1, 0, 1)
        else:
            self.wrong += 1
            self.feedback_label.text = f"❌ Xato! To‘g‘ri javob: {correct}"
            self.feedback_label.color = (1, 0, 0, 1)

        self.score_label.text = f"✅ To‘g‘ri: {self.score}    ❌ Xato: {self.wrong}"
        self.new_question()

    def update_timer(self, dt):
        if self.game_over:
            return

        self.time_left -= 1
        self.timer_label.text = f"⏳ Vaqt: {self.time_left}"

        if self.time_left <= 0:
            self.end_game()

    def end_game(self):
        self.game_over = True
        self.question_label.text = "🎮 O‘yin tugadi!"
        self.feedback_label.text = f"✅ To‘g‘ri: {self.score}   ❌ Xato: {self.wrong}"
        self.restart_button.disabled = False
        self.check_button.disabled = True
        self.answer_input.disabled = True

    def restart_game(self, instance):
        self.score = 0
        self.wrong = 0
        self.time_left = 30
        self.game_over = False
        self.score_label.text = "✅ To‘g‘ri: 0    ❌ Xato: 0"
        self.timer_label.text = f"⏳ Vaqt: {self.time_left}"
        self.feedback_label.text = ""
        self.check_button.disabled = False
        self.answer_input.disabled = False
        self.restart_button.disabled = True
        self.new_question()


class AddGameApp(App):
    def build(self):
        return AddGame()


if __name__ == "__main__":
    AddGameApp().run()
