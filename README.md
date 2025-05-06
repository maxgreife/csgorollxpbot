# 🎲 CSGORoll XP Calculator Bot

A Discord bot that helps you calculate how much you need to wager (and lose 💸) to reach your XP goal or next level on [CSGORoll](https://csgo-roll.com). Uses the 94% Dice strategy with 1.01x multiplier and a fixed 5.06% loss rate.

---

## 🚀 Features

- **/xpgoal** – Calculate how much XP is still missing and how many coins you need to wager to reach your goal.
- **/levelup** – Enter your current XP and desired level – see how much you're missing.
- Supports XP inputs like `4,000,000` or `4.000.000`
- Calculates estimated loss using the Dice method: 94% @ 1.01x multiplier

---

## 🧮 Dice Strategy Details

- ✅ 94% win chance
- 📈 1.01x multiplier
- 🔻 Approx. 5.06% expected loss

---

## 💻 Installation

### Requirements

- Python 3.10+
- `discord.py`
- `flask`

### Setup

1. Clone the repo or upload the files manually:

```bash
git clone https://github.com/yourname/csgo-xp-bot.git
cd csgo-xp-bot
