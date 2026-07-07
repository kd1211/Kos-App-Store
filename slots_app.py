import random
from ui.framework import App, Button, SCREEN_W, SCREEN_H, STATUS_BAR_H, FONT_MD, FONT_LG


class SlotsApp(App):
    name = "Slots"
    icon = "🎰"

    def on_open(self):
        self.money = 100
        self.user_class = "Player"
        self.result = "Roll!"

        self.buttons = [
            Button(
                SCREEN_W // 2 - 60,
                SCREEN_H - 80,
                120,
                44,
                "Roll",
                self.roll,
                font=FONT_MD
            ),
            Button(
                SCREEN_W // 2 - 60,
                SCREEN_H - 130,
                120,
                42,
                "Class",
                self.change_class,
                font=FONT_MD
            ),
            Button(
                SCREEN_W // 2 - 60,
                SCREEN_H - 180,
                120,
                42,
                "Home",
                self.os.go_home,
                font=FONT_MD
            )
        ]

    def roll(self):
        if self.money < 10:
            self.result = "No money!"
            return

        self.money -= 10

        a = random.randint(1, 6)
        b = random.randint(1, 6)
        c = random.randint(1, 6)

        self.result = f"{a} {b} {c}"

        if a == b == c:
            self.money += 100
            self.result = "JACKPOT!"

    def change_class(self):
        classes = [
            "Player",
            "High Roller",
            "Lil Win"
        ]

        index = classes.index(self.user_class)
        self.user_class = classes[(index + 1) % len(classes)]

    def draw(self, draw, canvas):
        draw.text(
            (SCREEN_W // 2, STATUS_BAR_H + 30),
            "Dice Slots",
            font=FONT_MD,
            fill=(255, 255, 255),
            anchor="mm"
        )

        draw.text(
            (SCREEN_W // 2, SCREEN_H // 2 - 40),
            self.result,
            font=FONT_LG,
            fill=(255, 165, 0),
            anchor="mm"
        )

        draw.text(
            (SCREEN_W // 2, SCREEN_H // 2 + 20),
            f"${self.money} - {self.user_class}",
            font=FONT_MD,
            fill=(255, 255, 255),
            anchor="mm"
        )

        for b in self.buttons:
            b.draw(draw)
