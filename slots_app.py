import random

class SlotsApp:
    name = "Dice Slots"
    icon = "D"

    def __init__(self, os_):
        self.os = os_
        self.money = 100
        self.user_class = "Player"
        self.message = "Press Roll"

    def draw(self):
        self.os.lcd.clear()

        self.os.lcd.text(20, 30, "Dice Slots", size=2)
        self.os.lcd.text(20, 80, f"Money: {self.money}", size=1)
        self.os.lcd.text(20, 110, f"Class: {self.user_class}", size=1)

        self.os.lcd.text(20, 160, self.message, size=1)

        self.os.lcd.text(40, 220, "[ ROLL ]", size=2)
        self.os.lcd.text(40, 270, "[ CLASS ]", size=2)

    def update(self, touch):
        if not touch:
            return

        x, y = touch

        if 40 <= x <= 160 and 200 <= y <= 250:
            self.roll()

        elif 40 <= x <= 180 and 250 <= y <= 310:
            self.change_class()

    def roll(self):
        if self.money < 10:
            self.message = "Not enough money"
            return

        self.money -= 10

        num1 = random.randint(1, 7)
        num2 = random.randint(1, 7)
        num3 = random.randint(1, 7)

        self.message = f"Rolled: {num1} {num2} {num3}"

        if num1 == num2 == num3:
            self.money += 100
            self.message = "JACKPOT +100!"

    def change_class(self):
        classes = [
            "Player",
            "High Roller",
            "Lil Win"
        ]

        index = classes.index(self.user_class)
        self.user_class = classes[(index + 1) % len(classes)]

        self.message = "Class changed"
