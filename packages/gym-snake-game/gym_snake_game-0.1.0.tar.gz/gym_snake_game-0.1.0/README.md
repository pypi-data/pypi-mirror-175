# Gym_Snake_Game
 Snake game for OpenAI gym


## Quick Start

```python
import gym_snake_game
import gym

env = gym.make('Snake-v0', render_mode='human')
d = False

# for human playing
env.play()

# for ai playing
while True:
    s, r, d, t, _info = env.step(env.action_space.sample())
    if d:
        env.reset()

```

**Ming Yu**