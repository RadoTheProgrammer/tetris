This is a home-made game tetris that I made with pygame.

1. Clone the repo: `git clone https://github.com/RadoTheProgrammer/tetris`
2. install the dependencies: `pip install pygame numpy`
3. run the file `main.py`

You can update `START_LEVEL` of main.py to start at any level

# Controls
| Action            | Control
| ---------------   | -----------------
| move the piece:   |  left and right arrow
| turn the piece:   |  up arrow
| soft drop:        |  down arrow
| hard drop:        |  space
| hold:             |  C

# Score system
| Action            | Score
| ---------------   | -
| clear 1 line      | +100
| clear 2 lines     | +300
| clear 3 lines     | +500
| clear 4 lines (tetris)    | +800
| soft drop         | +1 per move
| hard drop         | +2 per move
| when leveling up  | score of line cleared is multiplied

