#!/usr/bin/python3
import sys
from time import time
from math import hypot

from OpenGL import GL as gl
from OpenGL import GLUT as glut
from OpenGL import GLU as glu

import board
import pacman
import ghost
from solid_data import OPPOSITE_MOVES as op
from utils import time_fn

class Main:
    """
    Main class of the PacMan game.

    This class contains all methods for initializing OpenGL objects.
    It also contains all game objects such as the board, coins, PacMan, and ghosts.
    """
    def __init__(self, maze):
        """Constructor method of the Main Class.

        Initializes all objects needed to start the game:
        board, coins, PacMan, and ghosts.
        """
        self.time_point = time()                               # Initialize the time point for FPS calculation
        self.fps_no = 0                                        # Initialize the frame counter

        # Create the game board
        self.board = board.Board(maze)

        # Create the PacMan player
        self.pacman = pacman.PacMan(14, 18)

        # Create the ghosts
        self.ghost1 = ghost.Ghost(14, 6, "N", (1.0, 0.0, 1.0))
        self.ghost2 = ghost.Ghost(14, 6, "W", (1.0, 0.0, 0.0))
        self.ghost3 = ghost.Ghost(14, 6, "E", (0.0, 1.0, 1.0))

        self.ghosts = [self.ghost1, self.ghost2, self.ghost3]  # Store the ghosts in a list

    def key_pressed(self, key, x, y):
        """Function called whenever a key is pressed.

        :param key: string representing the pressed key
        :param x: x-coordinate of the mouse
        :param y: y-coordinate of the mouse
        """
        #TODO to make it work
        if key == b'\033':  # If the ESC key is pressed
            sys.exit()      # Exit the game

    def key_pressed_special(self, key, x, y):
        """Function called whenever a special key is pressed.

        :param key: integer representing the pressed key
        :param x: x-coordinate of the mouse
        :param y: y-coordinate of the mouse
        """
        #TODO to make it work
        if key == 100:                          # Left arrow key
            self.pacman.next_direction = 'W'
        elif key == 102:                        # Right arrow key
            self.pacman.next_direction = 'E'
        elif key == 101:                        # Up arrow key
            self.pacman.next_direction = 'N'
        elif key == 103:                        # Down arrow key
            self.pacman.next_direction = 'S'

    def key_pressed_special_up(self, key, x, y):
        """Function called when a special key is released.

        :param key: integer representing the released key
        :param x: x-coordinate of the mouse
        :param y: y-coordinate of the mouse
        """
        pass

    def outside_board(self, object):
        """Function to check if an object is outside the board and wrap it around if necessary.

        :param object: object to check
        """
        if object.pos_x < 0:
            object.pos_x = self.board.maze_row_len-1

        elif object.pos_x > self.board.maze_row_len-1:
            object.pos_x = 0

        if object.pos_z < 0:
            object.pos_z = self.board.maze_len-1

        elif object.pos_z > self.board.maze_len-1:
            object.pos_z = 0

    def collision_pacman_coin(self, coin):
        """Function to check for collisions between PacMan and coins.

        :param coin: Coin object to check
        """
        wall1 = self.pacman.pos_x - coin.pos_x
        wall2 = self.pacman.pos_z - coin.pos_z
        radius = self.pacman.radius + coin.radius

        if radius > hypot(wall1, wall2):             # Check if PacMan is close enough to collect the coin
            if coin.super_coin:
                print("     SUPER COIN     ")
                print("    GHOSTS ARE VULNERABLE   ")
                self.board.super_coins.remove(coin)  # Remove the super coin from the board
                for one_ghost in self.ghosts:
                    one_ghost.become_eatable()       # Make all ghosts eatable
            else:
                self.board.coins.remove(coin)        # Remove the coin from the board

    def collision_pacman_ghost(self, object):
        """Function to check for collisions between PacMan and ghosts.

        :param object: Ghost object to check
        """
        wall1 = self.pacman.pos_x - object.pos_x
        wall2 = self.pacman.pos_z - object.pos_z
        radius = self.pacman.radius + object.radius

        if radius > hypot(wall1, wall2):              # Check if PacMan is close enough to collide with the ghost
            if object.eatable:
                print("     PACMAN ATE THE GHOST    ")
                object.was_eaten_by_pacman()          # Handle ghost being eaten by PacMan
            elif isinstance(object, pacman.PacMan):
                self.pacman.was_eaten = True
                print("    GHOST CAUGHT PACMAN     ")

    def pacman_move(self):
        """Function to move PacMan based on the current and next direction."""
        directions = self.board.knots.get((self.pacman.pos_x, self.pacman.pos_z))
        if not self.pacman.was_eaten:
            if directions:
                if self.pacman.next_direction in directions:
                    self.pacman.direction = self.pacman.next_direction
                    self.pacman.move()
                elif self.pacman.direction in directions:
                    self.pacman.move()
                else:
                    pass  # PacMan does not move
            elif self.pacman.next_direction == op[self.pacman.direction]:
                self.pacman.direction = self.pacman.next_direction
                self.pacman.move()
            else:
                self.pacman.move()

    def ghost_move(self, ghost):
        """Function to move a ghost based on its current direction and available paths.

        :param ghost: Ghost object to move
        """
        directions = self.board.knots.get((ghost.pos_x, ghost.pos_z))
        if not ghost.was_eaten:
            if directions:
                if len(directions) > 1:
                    if ghost.next_direction in directions:
                        ghost.direction = ghost.next_direction
                        ghost.choice_next_direction()
                        ghost.move()
                    elif ghost.direction in directions:
                        ghost.move()
                    else:
                        ghost.choice_next_direction()
                elif len(directions) == 1:
                    ghost.direction = directions
                    ghost.choice_next_direction()
                    ghost.move()
            else:
                ghost.move()
        else:
            if ghost.the_way:
                if directions:
                    ghost.direction = ghost.the_way[0]
                    ghost.move()
                    ghost.the_way = ghost.the_way[1:]
                else:
                    ghost.move()
            else:
                if directions:
                    ghost.find_path(self.board.maze_graph, self.board.ghost_nest_position)
                    ghost.direction = ghost.the_way[0]
                    ghost.move()
                    ghost.the_way = ghost.the_way[1:]
                else:
                    ghost.move()
            if (ghost.pos_z, ghost.pos_x) == self.board.ghost_nest_position:
                ghost.start_from_nest()
  
    @time_fn
    def draw_scene(self):
        """The function draws all game elements."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)        # Clear The Screen And The Depth Buffer
        gl.glLoadIdentity()                                                # Reset The View                             
        gl.glTranslatef(-self.board.maze_row_len / 2, 10.0, -30.0)         # Translate the view
        gl.glRotate(60, 1, 0, 0)                                           # Rotate the view

        self.board.draw()                                                  # Draw the board
        self.pacman.draw()                                                 # Draw PacMan
        self.pacman_move()                                                 # Move PacMan
        self.outside_board(self.pacman)                                    # Check if PacMan is outside the board


        for one_ghost in self.ghosts:
            one_ghost.draw()                                               # Draw the ghost
            one_ghost.become_not_eatable()                                 # Check if the ghost should become not eatable
            self.ghost_move(one_ghost)                                     # Move the ghost
            self.outside_board(one_ghost)                                  # Check if the ghost is outside the board
            self.collision_pacman_ghost(one_ghost)                         # Check for collisions with PacMan
        for coin in self.board.coins:
            self.collision_pacman_coin(coin)                               # Check for collisions with coins
        for coin in self.board.super_coins:
            self.collision_pacman_coin(coin)                               # Check for collisions with super coins

        self.fps()                                                         # Calculate and display FPS
        glut.glutSwapBuffers()                                             # Swap the buffers to display the drawn scene

    def fps(self):
        """Function to calculate and display the number of frames per second (FPS)."""
        if time() - self.time_point > 1.0:
            print("FPS - ", self.fps_no)
            self.time_point, self.fps_no = time(), 0
        else:
            self.fps_no += 1

    @staticmethod
    def init_gl(width, height):
        """A general OpenGL initialization function.

        Sets all of the initial parameters.
        This is called right after our OpenGL window is created.
        :param width: window width
        :param height: window height
        """
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)                                 # This Will Clear The Background Color To Black
        gl.glClearDepth(1.0)                                                # Enables Clearing Of The Depth Buffer
        gl.glDepthFunc(gl.GL_LESS)                                          # The Type Of Depth Test To Do
        gl.glEnable(gl.GL_DEPTH_TEST)                                       # Enables Depth Testing
        gl.glShadeModel(gl.GL_SMOOTH)                                       # Enables Smooth Color Shading
        gl.glMatrixMode(gl.GL_PROJECTION)                                   # Reset The Projection Matrix.
        gl.glLoadIdentity()                                                 # Calculate The Aspect Ratio Of The Window.

        glu.gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)  # Set the perspective

        gl.glMatrixMode(gl.GL_MODELVIEW)                                    # Set the model view matrix

    @staticmethod
    def re_size_gl_scene(width, height):
        """The function called when our window is resized
        :param width: window width
        :param height: window height
        """
        if height == 0:
            height = 1  # Prevent a divide by zero error

        # Reset The Current Viewport And Perspective Transformation
        gl.glMatrixMode(gl.GL_PROJECTION)                                   # Set the projection matrix
        gl.glLoadIdentity()                                                 # Load the identity matrix
        glu.gluPerspective(60.0, float(width) / float(height), 0.1, 100.0)  # Set the perspective
        gl.glMatrixMode(gl.GL_MODELVIEW)                                    # Set the model view matrix

    def main(self):
        """Main function responsible for run the game."""

        glut.glutInit(sys.argv)

        # Select type of Display mode:
        #  Double buffer
        #  RGBA color
        # Alpha components supported
        # Depth buffer
        glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE | glut.GLUT_DEPTH)

        glut.glutInitWindowSize(1000, 800)                 # get a 640 x 480 window
        glut.glutInitWindowPosition(0, 0)                  # the window starts at the upper left corner of the screen
        glut.glutCreateWindow("PacMan")                    # Asign name of the window
        glut.glutKeyboardFunc(self.key_pressed)            # Register the function called when the keyboard is pressed.
        glut.glutSpecialFunc(self.key_pressed_special)
        glut.glutSpecialUpFunc(self.key_pressed_special_up)

        glut.glutDisplayFunc(self.draw_scene)              # Register the drawing function with glut.

        # Uncomment this line to get full screen.
        # glut.glutFullScreen()

        glut.glutIdleFunc(self.draw_scene)                 # When we are doing nothing, redraw the scene.
        glut.glutReshapeFunc(self.re_size_gl_scene)        # Register the function called when our window is resized.
        self.init_gl(640, 480)                             # Initialize our window.
        glut.glutMainLoop()                                # Start Event Processing Engine


if __name__ == "__main__":
    print("Hit ESC key to quit.")  # Print a message to the console
    game = Main(board.maze)        # Create the game instance
    game.main()                    # Run the main game loop
