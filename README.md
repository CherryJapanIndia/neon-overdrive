# NEON OVERDRIVE 🏎️

A futuristic, polished top-down 2D racing game built with **Pygame** and **Python**. Features realistic physics, AI opponents, drift mechanics, nitro boosts, and a complete cyberpunk visual style.

![Python](https://img.shields.io/badge/python-3.8+-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

✨ **Full Physics Engine**
- Realistic acceleration, braking, and drift mechanics
- Friction-based velocity model with grip/drift coefficients
- Collision detection and resolution
- Nitro boost system with charge management

🤖 **Smart AI**
- Waypoint-based pathfinding
- Intelligent steering toward optimal racing line
- Rubber-banding difficulty scaling
- 3 AI opponents racing against the player

🎮 **Complete Gameplay**
- 4-car multiplayer (1 player + 3 AI)
- Lap timing with personal best tracking
- Checkpoint-based lap validation
- Real-time position leaderboard

🎨 **Cyberpunk Visuals**
- Neon colour palette (cyan, magenta, yellow, green)
- Grid-based track visualization
- Car glow effects
- Live minimap with all car positions

📊 **Professional HUD**
- Real-time speed display (km/h)
- Lap counter and best lap time
- Nitro charge bar
- Corner minimap
- Position standings

## Installation

### Requirements
- Python 3.8+
- Pygame 2.5+

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/neon-overdrive.git
cd neon-overdrive
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the game:**
```bash
python main.py
```

## Demo

- Hosted demo URL: `https://example.com/neon-overdrive-demo`
- Local demo: run `python main.py`

## Controls

| Input | Action |
|-------|--------|
| **↑ / W** | Accelerate |
| **↓ / S** | Reverse |
| **← / A** | Steer Left |
| **→ / D** | Steer Right |
| **Space** | Brake / Handbrake |
| **Shift** | Nitro Boost |
| **Esc** | Pause |

## Project Structure

```
neon_overdrive/
├── config.py       # Game constants & settings
├── physics.py      # Physics engine & vector math
├── car.py          # Car entity & logic
├── track.py        # Track system & checkpoints
├── hud.py          # In-game HUD display
├── main.py         # Main game loop
├── requirements.txt
├── README.md
└── LICENSE
```

## Game Mechanics

### Physics
- **Acceleration**: Throttle applies force forward
- **Drifting**: Hold handbrake while steering for reduced grip
- **Max Speed**: 800 pixels/sec (~280 km/h)
- **Friction**: Grip (0.88) vs Drift (0.92) coefficient

### AI Pathfinding
- AI cars follow waypoints placed around the track
- Steering smoothly toward optimal racing line
- Reaction time: 0.1 seconds
- Lookahead distance: 200 pixels

### Lap System
- Checkpoints validate each lap
- Lap times automatically tracked
- Best lap stored per session
- 3 laps to complete race

## Customization

Edit `config.py` to customize:
- Screen resolution (default: 1280x960)
- Physics constants (acceleration, max speed, etc.)
- Colour palette (neon cyberpunk theme)
- AI difficulty settings
- Game difficulty levels

Example:
```python
# config.py
Physics.MAX_SPEED = 1000.0  # Increase max speed
Physics.ACCELERATION = 1500.0  # Faster acceleration
```

## Code Quality

- Type hints throughout
- Docstrings for all classes/methods
- Clean module separation (physics, rendering, AI, etc.)
- ~650 lines of production-quality code

## Performance

- 60 FPS target
- Optimized collision detection
- Efficient AI pathfinding
- Minimal CPU/GPU usage

## Future Enhancements

- [ ] Multiple tracks (desert, city, mountain)
- [ ] Car customization (colors, upgrades)
- [ ] Sound effects & music
- [ ] Replay system
- [ ] Multiplayer networking
- [ ] Mobile touch controls
- [ ] Power-ups and hazards
- [ ] Dynamic difficulty scaling

## License

MIT License — See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Push and create a Pull Request

## Author

Created as a futuristic racing game demonstration showcasing Pygame capabilities and software architecture.

## Support

Have issues? Create a GitHub issue with:
- Python version
- Pygame version
- Error message
- Steps to reproduce

---

**🏁 Ready to race? Run `python main.py` and compete against the AI!**
