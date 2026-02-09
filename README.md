# gen-slater

Have you ever wanted to correctly communicate with a friend or family member of a different generation, and thus uses incomprehensible slang? Now that is finally possible with GEN-SLATER. With an API key, this application uses a next-word-prediction-model to consistently translate your slang to slang of another generation.

## Battle Bots Game

This repository also includes **Battle Bots**, an exciting pygame-based battle bot video game where you control a bot and fight against AI-controlled enemy bots in arena combat!

## Installation and Initialization

There are some very simple steps in order for you to be able to run this application yourself.

1. Clone git repository:
   ```bash
   git clone https://github.com/rrocketmann/gen-slater
   cd gen-slater
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. Run application:
   ```bash
   flask run
   ```

## Thank You!

Please star this repo if you like it and find it useful. 

**Live Demo:** [gen-slater.onrender.com](https://gen-slater.onrender.com) (Note: May sleep after inactivity on free tier)

---

## Battle Bots Game

### How to Play

**Battle Bots** is an action-packed arena combat game where you control a blue battle bot fighting against red enemy bots.

#### Installation

1. Install dependencies (including pygame):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the game:
   ```bash
   python battle_bots.py
   ```

#### Controls

- **WASD** or **Arrow Keys**: Move your bot
- **Mouse**: Aim your bot (it faces the cursor)
- **Left Click** or **Space**: Fire bullets
- **R**: Restart game (after victory/defeat)
- **ESC**: Quit game

#### Gameplay

- Destroy all enemy bots to win!
- Avoid enemy fire and manage your health
- Each bot has a health bar displayed above it
- Enemy bots have AI that will chase and shoot at you
- When low on health, enemies will try to retreat

#### Features

- Real-time combat mechanics
- AI-controlled enemy bots with chase and retreat behaviors
- Health system with visual health bars
- Projectile-based combat
- Victory and defeat conditions
- Smooth 60 FPS gameplay

Good luck, commander!
