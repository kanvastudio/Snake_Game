"""
=========================================================
🐍 RESPONSIVE SNAKE GAME (FINAL)
=========================================================
- Fully responsive UI
- D-pad controls
- Classic movement
- Proper canvas layering
=========================================================
"""

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from game_logic import SnakeGame


# =========================================================
# 🎮 GAME WIDGET
# =========================================================
class SnakeWidget(FloatLayout):
    def __init__(self, speed, wall_collision, **kwargs):
        super().__init__(**kwargs)

        self.game = SnakeGame(speed, wall_collision)

        self.cols = 20
        self.rows = 20

        self.update_cell_size()

        # separate canvas layer (FIX FOR DISAPPEARING UI)
        self.game_canvas = self.canvas.before

        # resize handling
        Window.bind(on_resize=self.on_resize)

        # game loop
        self.event = Clock.schedule_interval(self.update, self.game.speed)

        self.paused = False
        self._game_over_sent = False

        # -------------------------
        # SCORE UI
        # -------------------------
        self.score_label = Label(
            text="Score: 0",
            size_hint=(1, 0.1),
            pos_hint={"top": 1}
        )
        self.add_widget(self.score_label)

        # -------------------------
        # D-PAD
        # -------------------------
        self.create_controls()

        self.on_game_over_callback = None

    # =====================================================
    # RESPONSIVE CELL SIZE
    # =====================================================
    def update_cell_size(self):
        self.cell_size = min(
            Window.width / self.cols,
            Window.height / self.rows
        )

    def on_resize(self, *args):
        self.update_cell_size()

    # =====================================================
    # CONTROLS
    # =====================================================
    def create_controls(self):

        size = (0.18, 0.12)

        btn_up = Button(
            text="↑",
            size_hint=size,
            pos_hint={"center_x": 0.5, "y": 0.15}
        )
        btn_up.bind(on_press=lambda x: self.set_dir((0, 1)))

        btn_down = Button(
            text="↓",
            size_hint=size,
            pos_hint={"center_x": 0.5, "y": 0.02}
        )
        btn_down.bind(on_press=lambda x: self.set_dir((0, -1)))

        btn_left = Button(
            text="←",
            size_hint=size,
            pos_hint={"x": 0.32, "y": 0.085}
        )
        btn_left.bind(on_press=lambda x: self.set_dir((-1, 0)))

        btn_right = Button(
            text="→",
            size_hint=size,
            pos_hint={"right": 0.68, "y": 0.085}
        )
        btn_right.bind(on_press=lambda x: self.set_dir((1, 0)))

        self.add_widget(btn_up)
        self.add_widget(btn_down)
        self.add_widget(btn_left)
        self.add_widget(btn_right)

    def set_dir(self, new_dir):
        """Prevent reverse direction"""
        if (new_dir[0] * -1, new_dir[1] * -1) != self.game.direction:
            self.game.direction = new_dir

    # =====================================================
    # GAME LOOP
    # =====================================================
    def update(self, dt):

        if self.paused:
            return

        if self.game.game_over:
            if not self._game_over_sent:
                self._game_over_sent = True
                if self.on_game_over_callback:
                    self.on_game_over_callback(self.game.score)
            return

        self.game.step()

        # update speed dynamically
        self.event.cancel()
        self.event = Clock.schedule_interval(self.update, self.game.speed)

        self.score_label.text = f"Score: {self.game.score}"

        self.draw()

    # =====================================================
    # SWIPE CONTROL (OPTIONAL)
    # =====================================================
    def on_touch_move(self, touch):
        dx, dy = touch.dx, touch.dy

        if abs(dx) > abs(dy):
            self.set_dir((1, 0) if dx > 0 else (-1, 0))
        else:
            self.set_dir((0, 1) if dy > 0 else (0, -1))

    # =====================================================
    # DRAW
    # =====================================================
    def draw(self):
        self.game_canvas.clear()

        with self.game_canvas:

            # FOOD
            Color(1, 0, 0)
            fx, fy = self.game.food
            Rectangle(
                pos=(fx * self.cell_size, fy * self.cell_size),
                size=(self.cell_size, self.cell_size)
            )

            # SNAKE
            for i, (x, y) in enumerate(self.game.snake):

                if i == 0:
                    Color(0.2, 0.6, 1)
                else:
                    Color(0, 0.8, 0)

                Rectangle(
                    pos=(x * self.cell_size, y * self.cell_size),
                    size=(self.cell_size * 0.9, self.cell_size * 0.9)
                )


# =========================================================
# MENU
# =========================================================
class MenuScreen(Screen):
    def __init__(self, start_callback, **kwargs):
        super().__init__(**kwargs)

        self.start_callback = start_callback

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="SNAKE", font_size=40))

        layout.add_widget(Label(text="Speed"))

        self.speed = 0.2

        for text, value in [("Slow", 0.3), ("Medium", 0.2), ("Fast", 0.1)]:
            btn = ToggleButton(text=text, group="speed")

            if value == 0.2:
                btn.state = "down"

            btn.bind(on_press=lambda btn, v=value: self.set_speed(btn, v))
            layout.add_widget(btn)

        layout.add_widget(Label(text="Wall Mode"))

        self.wall = True

        btn1 = ToggleButton(text="Walls Kill", group="wall", state="down")
        btn2 = ToggleButton(text="Wrap Walls", group="wall")

        btn1.bind(on_press=lambda btn: self.set_wall(btn, True))
        btn2.bind(on_press=lambda btn: self.set_wall(btn, False))

        layout.add_widget(btn1)
        layout.add_widget(btn2)

        start_btn = Button(text="START GAME", size_hint=(1, 0.3))
        start_btn.bind(on_press=self.start_game)

        layout.add_widget(start_btn)

        self.add_widget(layout)

    def set_speed(self, btn, value):
        btn.state = "down"
        self.speed = value

    def set_wall(self, btn, value):
        btn.state = "down"
        self.wall = value

    def start_game(self, _):
        self.start_callback(self.speed, self.wall)


# =========================================================
# GAME SCREEN
# =========================================================
class GameScreen(Screen):
    def __init__(self, speed, wall, callback, **kwargs):
        super().__init__(**kwargs)

        self.widget = SnakeWidget(speed, wall)
        self.widget.on_game_over_callback = callback

        self.add_widget(self.widget)


# =========================================================
# GAME OVER
# =========================================================
class GameOverScreen(Screen):
    def __init__(self, restart_callback, score, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text=f"GAME OVER\nScore: {score}"))

        btn = Button(text="Back to Menu")
        btn.bind(on_press=lambda x: restart_callback())

        layout.add_widget(btn)

        self.add_widget(layout)


# =========================================================
# APP
# =========================================================
class SnakeApp(App):

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(self.start_game, name="menu"))
        return self.sm

    def start_game(self, speed, wall):
        self.sm.add_widget(GameScreen(speed, wall, self.game_over, name="game"))
        self.sm.current = "game"

    def game_over(self, score):
        self.sm.add_widget(GameOverScreen(self.go_menu, score, name="over"))
        self.sm.current = "over"

    def go_menu(self):
        for s in ["game", "over"]:
            if s in self.sm.screen_names:
                self.sm.remove_widget(self.sm.get_screen(s))

        self.sm.current = "menu"


if __name__ == "__main__":
    SnakeApp().run()