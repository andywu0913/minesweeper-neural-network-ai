# Minesweeper Neural Network AI

AI project for CS445.

This is an ongoing project. Any effective outcome is not guaranteed.

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

## Current Progress

Right now we have trained our model by playing 30,000 times of the game. Our traing is still ongoing and we will keep updating the latest model to the folder.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/generation_30000/stat.png" width="600px">



