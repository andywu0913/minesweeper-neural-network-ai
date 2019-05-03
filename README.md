# Minesweeper Neural Network AI

AI project for CS445.

This is an ongoing project. Any effective outcome is not guaranteed.

Start a new minesweeper game by opening `minesweeper/minecore.html` and run the file `solveAI.py` to make neural network working.

To change rows, columns and number of bombs of the gameboard. Host the subfolder *minesweeper* on webserver such as Apache before opening the html files. It uses cookies to keep track of the gameboard configuration.

- `resolution_scale` should change to `2` when running on Mac retina display or other devices that doubled the pixels from its resolution.

## Environment

- Python 3.7.2
- Tensorflow 1.13.1

## Block Status Code

- `1`  Num 1 Blue Block
- `2`  Num 2 Green Block
- `3`  Num 3 Red Block
- `4`  Num 4 Dark Blue Block
- `5`  Num 5 Dark Red Block
- `6`  Num 6 Cyan Block
- `7`  Num 7 Black Block
- `8`  Num 8 Gray Block
- `9`  Opened Block
- `0`  Undetermined Block
- `-1`  Flag
- `-2`  Current Opened Bomb
- `-3`  Other Opened Bomb
- `-4`  Misplaced Flag
- `-5`  Possibly is in the win page with yellow background
- `-99`  Cannot determine

## Current Training Progress

### Games Generation 0 to 100,000

In the first 100,000 times of our neural network plays the game, we set the size of the game board to 24x32 with 99 bombs. The purpose is to let our neural network quickly learn how the game is played without being distracted by the border.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/generation_100000/stat.png" width="600px">

### Games Generation 100,000 above

After 100,000 times of games played, we set the size of the game board to 8x8 with 10 bombs to let our neural network starts learning the blocks near the border. We have gone through 140,000 generations so far.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/generation_140000/stat.png" width="600px">
