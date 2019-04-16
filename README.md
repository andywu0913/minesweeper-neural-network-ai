# Minesweeper Neural Network AI

AI project for CS445.

This project is still under construction.

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
- `-5`  Possibly is in the yellow background win page
- `-99`  Cannot determine
