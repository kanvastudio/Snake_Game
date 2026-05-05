"""
=========================================================
🐍 RESPONSIVE SNAKE GAME
=========================================================
"""

# ---------------- KIVY CORE APP ----------------
from kivy.app import App  # base application class
from kivy.clock import Clock  # game loop scheduler (FPS timer)
from kivy.graphics import Rectangle, Color  # drawing primitives
from kivy.uix.screenmanager import ScreenManager, Screen  # screen switching system
from kivy.uix.boxlayout import BoxLayout  # vertical/horizontal layout container
from kivy.uix.button import Button  # clickable button widget
from kivy.uix.togglebutton import ToggleButton  # toggle-style buttons (menu)
from kivy.uix.label import Label  # text display widget
from kivy.uix.widget import Widget  # empty drawable container (game field)
from kivy.core.window import Window  # access screen size
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line # boundary lib
from kivy.core.audio import SoundLoader # sound support

# ---------------- GAME LOGIC ----------------
from game_logic import SnakeGame  # external snake rules engine

GAME_OFFSET_Y = 20

# =========================================================
# 🎮 GAME WIDGET (MAIN GAME UI + LOGIC CONTROLLER)
# =========================================================
class SnakeWidget(BoxLayout):  # main game container (vertical stack UI)

    def __init__(self, speed, wall_collision, **kwargs):
        super().__init__(orientation="vertical", **kwargs)  # vertical layout

        # create game logic instance
        self.game = SnakeGame(speed, wall_collision)

        # grid size (logical game resolution)
        self.cols = 20  # width in grid cells
        self.rows = 20  # height in grid cells

        # game state flags
        self.paused = False
        self._game_over_sent = False
        
        # --- SOUND TRACKING ---
        self.last_score = 0
        self.sound_eat = SoundLoader.load('eat.wav')
        self.sound_crash = SoundLoader.load('crash.wav')

        # =====================================================
        # SCORE BAR (TOP UI)
        # =====================================================
        self.score_label = Label(
            text="Score: 0",  # initial score
            size_hint=(1, 0.08)  # 8% of screen height
        )
        self.add_widget(self.score_label)  # add to layout

        # =====================================================
        # GAME AREA (CENTER DRAWING FIELD)
        # =====================================================
        self.game_area = Widget(size_hint=(1, 0.74))  # 74% height reserved for game field
        self.add_widget(self.game_area)

        # canvas used for drawing snake + food
        self.game_canvas = self.game_area.canvas.before

        # =====================================================
        # CONTROLS AREA (BOTTOM D-PAD)
        # =====================================================

        controls = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.18),
            padding=[5, 5, 5, 5],  # LEFT, TOP, RIGHT, BOTTOM
            spacing=5
        )

        # 3 rows for D-pad layout
        row1 = BoxLayout(size_hint=(1, 0.33))
        row2 = BoxLayout(size_hint=(1, 0.33))
        row3 = BoxLayout(size_hint=(1, 0.33))

        # direction buttons
        btn_up = Button(text="UP", size_hint=(0.3, 1))
        btn_down = Button(text="DOWN", size_hint=(0.3, 1))
        btn_left = Button(text="LEFT", size_hint=(0.3, 1))
        btn_right = Button(text="RIGHT", size_hint=(0.3, 1))

        # bind button clicks to direction changes
        btn_up.bind(on_press=lambda x: self.set_dir((0, 1)))
        btn_down.bind(on_press=lambda x: self.set_dir((0, -1)))
        btn_left.bind(on_press=lambda x: self.set_dir((-1, 0)))
        btn_right.bind(on_press=lambda x: self.set_dir((1, 0)))

        # layout positioning for UP button
        row1.add_widget(Widget())  # empty spacer left
        row1.add_widget(btn_up)
        row1.add_widget(Widget())  # empty spacer right

        # layout positioning for LEFT / RIGHT
        row2.add_widget(btn_left)
        row2.add_widget(Widget())
        row2.add_widget(btn_right)

        # layout positioning for DOWN
        row3.add_widget(Widget())
        row3.add_widget(btn_down)
        row3.add_widget(Widget())

        # add rows to control panel
        controls.add_widget(row1)
        controls.add_widget(row2)
        controls.add_widget(row3)

        # attach controls to main layout
        self.add_widget(controls)

        # =====================================================
        # RESPONSIVE SCALING (IMPORTANT FIX)
        # =====================================================
        self.game_area.bind(size=self.update_cell_size)  # recalc when resized
        self.update_cell_size()  # initial calculation

        # =====================================================
        # GAME LOOP TIMER
        # =====================================================
        self.event = Clock.schedule_interval(self.update, self.game.speed)

    # =========================================================
    # GAME FIELD SIZE CALCULATION
    # =========================================================
    def update_cell_size(self, *args):
        w, h = self.game_area.size  # ONLY game area size (not full screen!)
        
        # Adding a 0.95 multiplier creates a small safety margin
        self.cell_size = min(
            w / self.cols,  # width per cell
            h / self.rows   # height per cell
        ) * 0.95

    # =========================================================
    # INPUT CONTROL
    # =========================================================
    def set_dir(self, new_dir):
        # prevents snake reversing into itself
        if (new_dir[0] * -1, new_dir[1] * -1) != self.game.direction:
            self.game.direction = new_dir

    # =========================================================
    # GAME LOOP
    # =========================================================
    def update(self, dt):

        if self.paused:
            return

        if self.game.game_over:
            if not self._game_over_sent:
                if self.sound_crash:
                    self.sound_crash.play()
                self._game_over_sent = True
                # Return to menu after 1 second delay
                Clock.schedule_once(self.return_to_menu, 1.0)
            return

        # step game logic forward
        self.game.step()

        # --- SOUND TRIGGER ---
        if self.game.score > self.last_score:
            if self.sound_eat:
                self.sound_eat.play()
            self.last_score = self.game.score

        # update UI score
        self.score_label.text = f"Score: {self.game.score}"

        # redraw game field
        self.draw()

    def return_to_menu(self, dt):
        app = App.get_running_app()
        if app.sm.has_screen('game'):
            # Remove the game screen instance to reset it for next time
            game_screen = app.sm.get_screen('game')
            app.sm.remove_widget(game_screen)
        app.sm.current = "menu"

    # =========================================================
    # DRAW GAME FIELD
    # =========================================================
    def draw(self):
        self.game_canvas.clear()
        
        # 1. Get the base position of the widget (moves it UP)
        base_x, base_y = self.game_area.pos
        w, h = self.game_area.size

        # 2. Calculate centering offsets
        # This removes the "limit on the right" by centering the grid
        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        
        centering_x = (w - grid_width) / 2
        centering_y = (h - grid_height) / 2

        # Final draw position
        offset_x = base_x + centering_x
        offset_y = base_y + centering_y
        
        with self.game_canvas:
            # 1. DRAW BOUNDARY (White border)
            Color(1, 1, 1, 0.5) # Semi-transparent white
            Line(rectangle=(offset_x, offset_y, grid_width, grid_height), width=2)

        with self.game_canvas:
            # Draw food
            Color(1, 0, 0)
            fx, fy = self.game.food
            Rectangle(
                pos=(offset_x + fx * self.cell_size, offset_y + fy * self.cell_size),
                size=(self.cell_size, self.cell_size)
            )

            # Draw snake body
            for i, (x, y) in enumerate(self.game.snake):
                Color(0.2, 0.6, 1) if i == 0 else Color(0, 0.8, 0)
                Rectangle(
                    pos=(offset_x + x * self.cell_size, offset_y + y * self.cell_size),
                    size=(self.cell_size * 0.9, self.cell_size * 0.9)
                )


# =========================================================
# MENU SCREEN
# (unchanged logic, only UI wrapper)
# =========================================================
class MenuScreen(Screen):

    def __init__(self, start_callback, **kwargs):
        super().__init__(**kwargs)

        self.start_callback = start_callback

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="A Snake game. Ver. 1.05. KanvaStudio", font_size=30))

        self.speed = 0.2

        for text, value in [("Slow", 0.3), ("Medium", 0.2), ("Fast", 0.1)]:
            btn = ToggleButton(text=text, group="speed")
            if value == 0.2:
                btn.state = "down"
            btn.bind(on_press=lambda b, v=value: self.set_speed(b, v))
            layout.add_widget(btn)

        self.wall = True

        btn1 = ToggleButton(text="Walls Kill", group="wall", state="down")
        btn2 = ToggleButton(text="Wrap Walls", group="wall")

        btn1.bind(on_press=lambda b: self.set_wall(b, True))
        btn2.bind(on_press=lambda b: self.set_wall(b, False))

        layout.add_widget(btn1)
        layout.add_widget(btn2)

        start_btn = Button(text="START GAME")
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
# GAME SCREEN WRAPPER
# =========================================================
class GameScreen(Screen):

    def __init__(self, speed, wall, callback, **kwargs):
        super().__init__(**kwargs)

        self.widget = SnakeWidget(speed, wall)
        self.add_widget(self.widget)


# =========================================================
# APP ENTRY POINT
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
        print("GAME OVER:", score)


if __name__ == "__main__":
    SnakeApp().run()