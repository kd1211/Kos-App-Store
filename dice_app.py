import random
from ui.framework import App, Button, SCREEN_W, SCREEN_H, STATUS_BAR_H, FONT_MD, FONT_LG

class DiceApp(App):
    name = "Dice Roller"
    icon = "\U0001F3B2"

    def on_open(self):
        self.dice_value = 1
        self.buttons = [
            Button(SCREEN_W // 2 - 60, SCREEN_H - 80, 120, 44, 
                   "Roll Dice", self.roll_dice, font=FONT_MD),
            Button(SCREEN_W // 2 - 60, SCREEN_H - 130, 120, 42, 
                   "Home", self.os.go_home, font=FONT_MD)
        ]

    def roll_dice(self):
        self.dice_value = random.randint(1, 6)

    def draw(self, draw, canvas):
        # App Title
        draw.text((SCREEN_W // 2, STATUS_BAR_H + 30), "Dice Roller", 
                  font=FONT_MD, fill=(255, 255, 255), anchor="mm")
        
        # Display current dice value
        draw.text((SCREEN_W // 2, SCREEN_H // 2 - 20), str(self.dice_value), 
                  font=FONT_LG, fill=(255, 165, 0), anchor="mm")
        
        # Draw buttons
        for b in self.buttons:
            b.draw(draw)
