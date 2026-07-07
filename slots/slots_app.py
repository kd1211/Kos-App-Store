from ui import sound
from ui.framework import App, Button, SCREEN_W, SCREEN_H, STATUS_BAR_H, \
    FONT_MD, FONT_SM, CARD_COLOR, ACCENT

from symbols import load_symbol, pick_symbols, SYMBOL_NAMES

CLASSES = [
    {"name": "Player", "bet": 10, "jackpot": 100},
    {"name": "High Roller", "bet": 25, "jackpot": 300},
    {"name": "Lil Win", "bet": 5, "jackpot": 40},
]

REEL_W = 72
REEL_GAP = 12
REEL_TOP = STATUS_BAR_H + 110


class SlotsApp(App):
    name = "Slots"
    icon = "\U0001F3B0"

    def on_open(self):
        self.money = 100
        self.class_idx = 0
        self.reels = pick_symbols(3)
        self.message = "Tap Spin ($10)"
        self._build_buttons()
        self._sync_message()

    def _tier(self):
        return CLASSES[self.class_idx]

    def _sync_message(self):
        tier = self._tier()
        self.message = f"Bet ${tier['bet']}  |  Jackpot ${tier['jackpot']}"

    def _build_buttons(self):
        self.buttons = [
            Button(SCREEN_W // 2 - 70, SCREEN_H - 120, 140, 44,
                   "Spin", self._spin, font=FONT_MD),
            Button(SCREEN_W // 2 - 70, SCREEN_H - 68, 140, 40,
                   "Class", self._next_class, font=FONT_SM),
            Button(SCREEN_W // 2 - 60, SCREEN_H - 24, 120, 36,
                   "Home", self.os.go_home, font=FONT_SM),
        ]

    def _next_class(self):
        self.class_idx = (self.class_idx + 1) % len(CLASSES)
        self._sync_message()

    def _spin(self):
        tier = self._tier()
        bet = tier["bet"]
        if self.money < bet:
            self.message = "Not enough coins!"
            sound.beep(220, 120)
            return

        self.money -= bet
        self.reels = pick_symbols(3)

        if self.reels[0] == self.reels[1] == self.reels[2]:
            win = tier["jackpot"]
            self.money += win
            self.message = f"JACKPOT! +${win}"
            sound.chime()
        elif self.reels[0] == self.reels[1] or self.reels[1] == self.reels[2]:
            win = bet * 2
            self.money += win
            self.message = f"Small win +${win}"
            sound.beep(660, 100)
        else:
            self.message = f"Try again  (-${bet})"
            sound.beep(330, 80)

    def draw(self, draw, canvas):
        tier = self._tier()
        draw.text((SCREEN_W // 2, STATUS_BAR_H + 24), "Slots", font=FONT_MD,
                   fill=(255, 255, 255), anchor="mm")
        draw.text((SCREEN_W // 2, STATUS_BAR_H + 48),
                   f"${self.money}  |  {tier['name']}", font=FONT_SM,
                   fill=(200, 200, 210), anchor="mm")

        total_w = REEL_W * 3 + REEL_GAP * 2
        x0 = (SCREEN_W - total_w) // 2
        for i, name in enumerate(self.reels):
            x = x0 + i * (REEL_W + REEL_GAP)
            y = REEL_TOP
            draw.rounded_rectangle([x - 4, y - 4, x + REEL_W + 4, y + REEL_W + 4],
                                    radius=12, fill=CARD_COLOR)
            symbol = load_symbol(name, REEL_W)
            canvas.paste(symbol, (x, y), symbol)

        draw.text((SCREEN_W // 2, REEL_TOP + REEL_W + 36), self.message,
                   font=FONT_MD, fill=ACCENT, anchor="mm")

        legend_y = REEL_TOP + REEL_W + 68
        draw.text((SCREEN_W // 2, legend_y),
                   f"{len(SYMBOL_NAMES)} symbols  |  3-match pays jackpot",
                   font=FONT_SM, fill=(150, 150, 160), anchor="mm")

        for b in self.buttons:
            b.draw(draw)
