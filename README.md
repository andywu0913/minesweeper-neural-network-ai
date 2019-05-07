# Minesweeper Neural Network AI

AI project for CS445.

This is an ongoing project. Any effective outcome is not guaranteed.

## Usage

We did not use datasets to train or test our model, instead, it is realtime based. Thus we have to create the environment first before using the model.

A new environment(minesweeper game) can be created by opening `minesweeper/minecore.html`. To change rows, columns and number of bombs of the gameboard. Host the subfolder *minesweeper* on webserver such as Apache before opening the html files. It uses cookies to keep track of the gameboard configuration.

Remember to change the `resolution_scale` to fit the resolution of the device. For example, `resolution_scale` should change to `2` when running on Mac retina display or other devices that double the pixels from their resolutions. The program recognizes the game board blocks by their colors, so resolution scale has to be set correctly in order to calculate the correct block position.

### Training

Leave the browser(minesweeper) half of the screen large and the terminal the rest of the screen.

Run the command below to start training the neural network.

````
python3.7 trainAI.py
````

### Testing

Leave the browser(minesweeper) half of the screen large and the terminal the rest of the screen.

Run the command below to start testing the neural network.

````
python3.7 solveAI.py
````

## Development Environment

- macOS High Sierra 10.13.4 (Retina Display)
- Python 3.7.2
- Tensorflow 1.13.1
- NumPy 1.16.1
- PyAutoGUI 0.9.41
- Pillow 5.4.1
- mss 4.0.2

## Block Status Code

- `1`  &nbsp;&nbsp;Num 1 Blue Block
- `2`  &nbsp;&nbsp;Num 2 Green Block
- `3`  &nbsp;&nbsp;Num 3 Red Block
- `4`  &nbsp;&nbsp;Num 4 Dark Blue Block
- `5`  &nbsp;&nbsp;Num 5 Dark Red Block
- `6`  &nbsp;&nbsp;Num 6 Cyan Block
- `7`  &nbsp;&nbsp;Num 7 Black Block
- `8`  &nbsp;&nbsp;Num 8 Gray Block
- `9`  &nbsp;&nbsp;Opened Block
- `0`  &nbsp;&nbsp;Undetermined Block
- `-1`  &nbsp;Flag
- `-2`  &nbsp;Current Opened Bomb
- `-3`  &nbsp;Other Opened Bomb
- `-4`  &nbsp;Misplaced Flag
- `-5`  &nbsp;Possibly is in the win page with yellow background
- `-99`  Cannot determine

## Training Progress

### Game Generations 0 to 100,000

In the first 100,000 times of our neural network plays the game, we set the size of the game board to 24x32 with 99 bombs. The purpose is to let our neural network quickly learn how the game is played without being distracted by the border.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/generation_100000/stat.png" width="600px">

### Game Generations 100,000 above

After 100,000 times of games played, we set the size of the game board to 8x8 with 10 bombs to let our neural network start learning the blocks near the border. Until May 7, the day before our project presentation, the neural network has gone through 207,421 generations of playing.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/stat.png" width="600px">
