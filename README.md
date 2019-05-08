# Minesweeper Neural Network AI

This is a course project in CS445. Any effective outcome is not guaranteed.

## Neural Network Structure

The neural network has 4 hidden layers with each of them contain 120 neurons. It takes a 1x24 matrix as its input which represents 2 outer cyclic surroundings, and outputs a value between 0 and 1 that shows how confident is opening the middle block without getting a bomb.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_structure.png" width="750px">

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

If the training slows down the computer, try decrease the loop times in `trainAI.py` and use `sh run.sh` to loop `trainAI.py`.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/demo_training.gif" width="600px">

### Testing

Leave the browser(minesweeper) half of the screen large and the terminal the rest of the screen.

Run the command below to start testing the neural network.

````
python3.7 solveAI.py
````

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/demo_testing.gif" width="600px">

## Development Environment

- macOS High Sierra 10.13.4 (Retina Display)
- Python 3.7.2
- Tensorflow 1.13.1
- NumPy 1.16.1
- PyAutoGUI 0.9.41
- Pillow 5.4.1
- mss 4.0.2

## Training Records

### Game Generations 0 to 100,000

In the first 100,000 times of our neural network plays the game, we set the size of the game board to 24x32 with 99 bombs. The purpose is to let our neural network quickly learn how the game is played without being distracted by the border.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/generation_100000/stat.png" width="600px">

### Game Generations 100,000 above

After 100,000 times of games played, we set the size of the game board to 8x8 with 10 bombs to let our neural network start learning the blocks near the border. Until May 7 2019, the day before our project presentation, the neural network has gone through 207,421 generations of playing and has approximately 5% of chances in average to complete a game.

<img src="https://github.com/andywu0913/minesweeper-neural-network-ai/blob/master/nn_trained_model/stat.png" width="600px">
