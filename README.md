# DEEP NEURAL NETWORK TO PLAY CAR RACING GAME

### Goals

- Implement a 2D Car Racing game environment using Pygame with possible play mode and ai mode.
- Implement a Deep Q Network agent to play the game using Keras with mean square errors loss function.

### Libraries

- Pygame
- Pandas
- Numpy
- Keras

### Tools and programming languages

- Python3
- Jupyter Notebook

### Installation

- Make sure python3 and all libraries mentioned above are installed
- Clone this repo
- Navigate into the folder
- Open terminal, start python3
```
python3
```
- Then import the Game class
```
from main import Game
```
- Then initialize the game environment
```
env = Game()
```
- Then run the ai model named ```model0999.h5``` to play the game
```
env.play_model("model0999.h5")
```

### Implementing your own Deep Neural Network

Open dqn.ipynb using Jupyter Notebook
You can play around with hyper parameters, change the loss function, change the reward logic