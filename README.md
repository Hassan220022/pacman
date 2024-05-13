# Pacman

Welcome to the 3D Maze Game project, a visually engaging maze exploration game powered by Python and OpenGL. In this game, players navigate Pac-Man through a 3D maze, collecting coins while avoiding walls and obstacles. The project is designed to demonstrate the use of OpenGL for creating interactive 3D environments in Python.

## Features

- **3D Maze Navigation**: Explore a complex maze in three dimensions.
- **Coin Collection**: Collect regular coins and special Super Coins throughout the maze.
- **Dynamic Obstacles**: Encounter and avoid dynamically placed obstacles within the maze.
- **OpenGL Graphics**: Experience smooth and visually appealing graphics rendered using OpenGL.

## Prerequisites

Before running the game, ensure you have the following installed:
- Python 3.6 or higher
- OpenGL libraries
- GLUT for OpenGL

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/Hassan220022/pacman.git
   cd pacman
   ```

2. **Install Python dependencies:**
   ```
   pip install PyOpenGL PyOpenGL_accelerate
   ```

## Structure

- `main.py`: Main executable script to launch the game.
- `solid_data.py`: Contains configuration data like colors and levels.
- `maze.py`: Defines the maze layout and initialization logic.
- `game_elements.py`: Includes classes for game elements such as Pac-Man, Coin, SuperCoin, and Block.
- `utils.py`: Utility functions and decorators for performance measurement.

## Usage

To start the game, navigate to the project directory and run:
```
python main.py
```
Control Pac-Man using the keyboard arrows or WASD keys to navigate through the maze and collect coins.

## How It Works

- **Maze Generation**: The maze is predefined with walls and paths where Pac-Man can move.
- **Game Elements**:
  - **Pac-Man**: Moves around the maze collecting coins.
  - **Coins**: Placed throughout the maze for Pac-Man to collect.
  - **Super Coins**: Give Pac-Man special abilities or extra points.
  - **Blocks**: Represent the walls of the maze.
- **Rendering**: The game uses OpenGL to render the maze and all interactive elements in 3D.

## Customization

You can customize the maze by modifying the `maze` array in `maze.py`. Each element of the array represents a cell in the maze where `1` is a wall and `0` is a path.
