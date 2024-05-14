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

    Class contains all method for initialising OpenGL objects.
    Contains also all game objects as board, coins, PacMan and ghosts.
    """
    def __init__(self, maze):
        """Constructor method of Main Class.

        It initialases all object needed for start the game
        board, coins, PacMan and ghosts.
        """
        self.time_point = time()
        self.fps_no = 0

        # board creating
        self.board = board.Board(maze)

        # PacMan player creating
        self.pacman = pacman.PacMan(14, 18)

        # Ghosts
        self.ghost1 = ghost.Ghost(14, 6, "N", (1.0, 0.0, 1.0))
        self.ghost2 = ghost.Ghost(14, 6, "W", (1.0, 0.0, 0.0))
        self.ghost3 = ghost.Ghost(14, 6, "E", (0.0, 1.0, 1.0))

        self.ghosts = [self.ghost1, self.ghost2, self.ghost3]

    def key_pressed(self, key, x, y):
        """The function called whenever a key is pressed.
        Note the use of Python tuples to pass in: (key, x, y)

        :param args: string represented pushed key
        """

        if key == b'\033':
            sys.exit()

    def key_pressed_special(self, key, x, y):
        """The function called whenever a key is pressed.
        Note the use of Python tuples to pass in: (key, x, y)

        :param args: integer represented pushed key
        """
        # operation of keys in a separate function.

        if key == 100:
            self.pacman.next_direction = 'W'

        elif key == 102:
            self.pacman.next_direction = 'E'

        elif key == 101:
            self.pacman.next_direction = 'N'

        elif key == 103:
            self.pacman.next_direction = 'S'

    def key_pressed_special_up(self, key, x, y):
        """"""
        pass

    def outside_board(self, object):
        """"""

        if object.pos_x < 0:
            object.pos_x = self.board.maze_row_len-1

        elif object.pos_x > self.board.maze_row_len-1:
            object.pos_x = 0

        if object.pos_z < 0:
            object.pos_z = self.board.maze_len-1

        elif object.pos_z > self.board.maze_len-1:
            object.pos_z = 0

    def collision_pacman_coin(self, coin):
        """"""

        wall1 = self.pacman.pos_x - coin.pos_x
        wall2 = self.pacman.pos_z - coin.pos_z
        radius = self.pacman.radius + coin.radius

        if radius > hypot(wall1, wall2):
            if coin.super_coin:
                print("     SUPER COIN     ")
                print("    GHOST ARE SENSIBLE   ")
                self.board.super_coins.remove(coin)
                for one_ghost in self.ghosts:
                    one_ghost.become_eatable()
            else:
                self.board.coins.remove(coin)

    def collision_pacman_ghost(self, object):
        """"""

        wall1 = self.pacman.pos_x - object.pos_x
        wall2 = self.pacman.pos_z - object.pos_z
        radius = self.pacman.radius + object.radius

        if radius > hypot(wall1, wall2):
            if object.eatable:
                print("     PACMAN EAT GHOST    ")
                object.was_eaten_by_pacman()

            elif isinstance(object, pacman.PacMan):
                self.pacman.was_eaten = True
                print("    GHOST CATCHED PACMAN     ")

    def pacman_move(self):
        """"""
        directions = self.board.knots.get(
            (self.pacman.pos_x, self.pacman.pos_z)
        )
        if not self.pacman.was_eaten:
            if directions:
                if self.pacman.next_direction in directions:
                    self.pacman.direction = self.pacman.next_direction
                    self.pacman.move()
                elif self.pacman.direction in directions:
                    self.pacman.move()
                else:
                    pass   # PacMan no moves

            elif self.pacman.next_direction == op[self.pacman.direction]:
                self.pacman.direction = self.pacman.next_direction
                self.pacman.move()
            else:
                self.pacman.move()

    def ghost_move(self, ghost):
        """"""
        directions = self.board.knots.get(
            (ghost.pos_x, ghost.pos_z)
        )

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
                    ghost.find_path(
                        self.board.maze_graph,
                        self.board.ghost_nest_position
                    )
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

        # Clear The Screen And The Depth Buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Reset The View
        gl.glLoadIdentity()
        gl.glTranslatef(-self.board.maze_row_len/2, 10.0, -30.0)
        gl.glRotate(60, 1, 0, 0)

        self.board.draw()

        self.pacman.draw()
        self.pacman_move()
        self.outside_board(self.pacman)

        for one_ghost in self.ghosts:
            one_ghost.draw()
            one_ghost.become_not_eatable()
            self.ghost_move(one_ghost)
            self.outside_board(one_ghost)
            self.collision_pacman_ghost(one_ghost)

        for coin in self.board.coins:
            self.collision_pacman_coin(coin)

        for coin in self.board.super_coins:
            self.collision_pacman_coin(coin)

        # counts number of frames
        self.fps()

        # since this is double buffered,
        # swap the buffers to display what just got drawn.
        glut.glutSwapBuffers()

    def fps(self):
        """Function counts number of frames per second (fps)."""

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
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)        # This Will Clear The Background Color To Black
        gl.glClearDepth(1.0)                       # Enables Clearing Of The Depth Buffer
        gl.glDepthFunc(gl.GL_LESS)                 # The Type Of Depth Test To Do
        gl.glEnable(gl.GL_DEPTH_TEST)              # Enables Depth Testing
        gl.glShadeModel(gl.GL_SMOOTH)              # Enables Smooth Color Shading
        gl.glMatrixMode(gl.GL_PROJECTION)          # Reset The Projection Matrix.
        gl.glLoadIdentity()                        # Calculate The Aspect Ratio Of The Window.

        glu.gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

        gl.glMatrixMode(gl.GL_MODELVIEW)

    @staticmethod
    def re_size_gl_scene(width, height):
        """The function called when our window is resized
        (which shouldn't happen if you enable fullscreen, below)

        :param width: window width
        :param height: window height
        """
        # Prevent A Divide By Zero If The Window Is Too Small
        if height == 0:
            height = 1

        gl.glViewport(0, 0, width, height)        # Reset The Current Viewport And Perspective Transformation
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(60.0, float(width)/float(height), 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

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
    print("Hit ESC key to quit.")    # Print message to console, and kick off the main to get it rolling.
    game = Main(board.maze)
    game.main()
