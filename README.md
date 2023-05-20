[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/I4_dFpC1)

---

# 1 Perspective Transformation

Run `python3 opencv_click.py [input file path] [output destination] [result width] [result height] [allow orientation fix]`
- input: input file path - *required*
- output: output destination path - *required*
- width: result width - *optional, default: 1920*
- height: result height - *optional, default: 1080*
- allow orientation fix: If allowed, the system recognizes if selected region is portrait or landscape. Width and height will be switches if more suitable - *optional, default: False*

### Controls
- Press `S` in the result view to save the image
- Press `ESC` to discard changes
- Press `Q` to quit

---

# 2 AR Game - PONG
Run `python3 opencv_pyglet.py [video in] [score] [difficulty]`
- video in: video input device - *optional*
- score: the score a player needs to win the game - *optional, default: 5*
- difficulty: difficulty defined by speed of ball - *optional, default: easy*

### Controls
- Place the AruCo-Board in front of your webcam
- Everyone knows Pong. But: use your hands instead of moving a paddle
- If no one wants to join in, you can use both your own hands - however then you will have to tape the AruCo-Board to your head or chest or whatever...well, it's up to you
- Hide a marker to **pause** the game
- Press `Q` to quit and `SPACE` to restart
