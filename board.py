#!/usr/bin/python3
from random import choice
from OpenGL import GL as gl
from OpenGL import GLUT as glut

import solid_data as data
from solid_data import set_color

# Each '1' represents a wall, and '0' indicates a path or empty space
maze = [ #19x29 maze
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], 
]

# Definition of the Coin class which represents coins that can be collected by the player in the game
class Coin:
    """Class of Coin object."""

    def __init__(self, pos_x, pos_z):
        """ Constructor method of Coin class.
        :param pos_x: int, position on x axis
        :param pos_z: int, position on z axis
        """
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.radius = 0.1                    # Radius of the coin, affects its size when rendered
        self.coin_color = data.COIN_COLOR    # Color of the coin, defined in 'solid_data.py'
        self.super_coin = False              # Boolean flag indicating whether it is a super coin

    def draw(self):
        """Function to draw the coin in the OpenGL context."""
        set_color(self.coin_color)
        gl.glPushMatrix()                                       # Push the current matrix stack to save the current transformation state
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)# Translate the coin to its position in the maze
        glut.glutSolidSphere(self.radius, 10, 10)               # Render the coin as a solid sphere
        gl.glPopMatrix()                                        # Pop the matrix stack to restore the previous transformation state

class SuperCoin(Coin):
    """Class for SuperCoin object, which inherits from Coin."""

    def __init__(self, pos_x, pos_z):
        """ Constructor method of SuperCoin class.

        :param pos_x: int, position on x axis
        :param pos_z: int, position on z axis
        """

        super().__init__(pos_x, pos_z)
        self.radius = 0.25                       # Set a larger radius for the super coin
        self.coin_color = data.SUPER_COIN_COLOR  # Use a distinct color for super coins, defined in 'solid_data.py'
        self.super_coin = True                   # Set the super_coin flag to True indicating it's a super coin


class Block:
    """Class for a block of wall, an element of the board."""

    def __init__(self, pos_xw, pos_zn, walls):
        """
        Constructor method of Block class.

        :param pos_xw: int, position of the west/north corner of block on x axis
        :param pos_zn: int, position of the west/north corner of block on z axis
        :param walls: str, information about which wall should be drawn for block
                      'S' - south wall
                      'N' - north wall
                      'E' - east wall
                      'W' - west wall
        """
        self.pos_xw = pos_xw                        # Position of the west corner of the block on the x-axis
        self.pos_xe = pos_xw + 1                    # Position of the east corner of the block on the x-axis
        self.pos_zn = pos_zn                        # Position of the north corner of the block on the z-axis
        self.pos_zs = pos_zn + 1                    # Position of the south corner of the block on the z-axis
        self.walls = walls                          # String containing characters "N", "S", "E", "W" indicating which walls are present

        self.floor_color = data.FLOOR_COLOR         # Color for the floor, from 'solid_data.py'
        self.celling_color = data.CELING_COLOR      # Color for the ceiling, from 'solid_data.py'
        self.celing_level = data.CELLING_LEVEL      # Height of the ceiling, from 'solid_data.py'
        self.floor_level = data.FLOOR_LEVEL         # Height of the floor, from 'solid_data.py'

    def __str__(self):
        """String representation of the Block object."""
        return "Block with position: " + str(self.pos_xw) + "," + str(self.pos_zs) + "," + self.walls


    def _draw_vertical_square(self, axis):
        """Function to draw a vertical square on a given axis.

        :param axis: str, axis type where square will be drawn
                     if axis in "NS" - square is on X axis
                     if axis in "WE" - square is on Z axis
        """
        if axis in "NS":
            pos_z = self.pos_zn if "N" in axis else self.pos_zs             # Determine the z position based on whether the axis is 'N' or 'S'

            gl.glBegin(gl.GL_QUADS)                                         # Start drawing a polygon
            set_color(self.floor_color)                                     # Set the color for the floor part of the wall
            gl.glVertex3f(self.pos_xw,  self.floor_level, pos_z)            # Top Left vertex
            gl.glVertex3f(self.pos_xe, self.floor_level, pos_z)             # Top Right vertex
            set_color(self.celling_color)                                   # Set the color for the ceiling part of the wall
            gl.glVertex3f(self.pos_xe, self.celing_level, pos_z)            # Bottom Right
            gl.glVertex3f(self.pos_xw,  self.celing_level, pos_z)           # Bottom Left
            gl.glEnd()

        elif axis in "WE":
            pos_x = self.pos_xe if "E" in axis else self.pos_xw             # Determine the x position based on whether the axis is 'E' or 'W'

            gl.glBegin(gl.GL_QUADS)                                         # Start drawing a polygon
            set_color(self.floor_color)
            gl.glVertex3f(pos_x, self.floor_level, self.pos_zs)             # Top Left vertex
            gl.glVertex3f(pos_x, self.floor_level, self.pos_zn)             # Top Right vertex
            set_color(self.celling_color)
            gl.glVertex3f(pos_x, self.celing_level, self.pos_zn)            # Bottom Right vertex
            gl.glVertex3f(pos_x, self.celing_level, self.pos_zs)            # Bottom Left vertex
            gl.glEnd()

    def _draw_celling(self):
        """Function to draw the ceiling of the block."""
        gl.glBegin(gl.GL_QUADS)                                     # Start drawing a polygon
        set_color(self.celling_color)                               # Set the color for the ceiling

        gl.glVertex3f(self.pos_xw, self.celing_level, self.pos_zn)  # Define the first vertex
        gl.glVertex3f(self.pos_xw, self.celing_level, self.pos_zs)  # Define the second vertex
        gl.glVertex3f(self.pos_xe, self.celing_level, self.pos_zs)  # Define the third vertex
        gl.glVertex3f(self.pos_xe, self.celing_level, self.pos_zn)  # Define the fourth vertex
        gl.glEnd()  # End drawing the quadrilateral polygon

    def draw_block(self):
        """ Function draws the block."""

        self._draw_celling()                               # draw celling
        # draw back, front, left and right wall
        for wall in "NSWE":
            if wall in self.walls:                         # If the wall should be drawn
                self._draw_vertical_square(wall)           # Draw the vertical square for the wall


class Board:
    """Class of Board object.

    Class contain all elements and method for crating and
    drawing the board, containig floor, walls and conis."""

    def __init__(self, maze):
        """Constructor method of the Board class.

        Initializes many board parameters and coin objects.
        Contains methods responsible for board drawing.

        :param maze: list of lists containing integers 0 or 1
                     0 - empty square, floor
                     1 - square with walls
        """
        self.maze_len = len(maze)                           # len of maze
        self.maze_row_len = len(maze[0])                    # width of maze
        self.super_coins_no = 5                             # number of super-coins
        self.blocks = []                                    # blocks in the board
        self.coins = []                                     # coins
        self.ghost_nest_position = 11, 14                   # position of the ghost nest
        
        self.knots = {}                                     # dict of knots, key=position, value=possible directions of move
        
        self.floor_level = data.FLOOR_LEVEL                 # height of floor
        self.floor_color = data.FLOOR_COLOR                 # floor color
        
        self._create_board_elements(maze)                   # Create board elements (blocks and coins)
        self._create_knots(maze)                            # Create knots (nodes for pathfinding)
        self.super_coins = self._create_super_coins()       # Create super coins
        self.block_positions = self._get_block_positions()  # Get positions of all blocks
        self.maze_graph = self._get_maze2graph(maze)        # Convert the maze to a graph representation

    def _get_block_positions(self):
        """Function to get positions of all blocks."""
        return set((block.pos_xw, block.pos_zn) for block in self.blocks)

    def _get_maze2graph(self, maze):
        """Function to convert the maze to a graph representation."""
        self.maze_len = len(maze)                                 # Length of the maze (number of rows)
        self.maze_row_len = len(maze[0]) if self.maze_len else 0  # Width of the maze (number of columns)

        graph = {                                                 # Create a dictionary for graph representation of the maze
            (i, j): []                                            # Each key is a coordinate tuple (i, j), and the value is an empty list for neighbors
            for j in range(self.maze_row_len)
            for i in range(self.maze_len)
            if not maze[i][j]
            }

        for row, col in graph.keys():            # Loop through each cell in the graph

            # If there is a path to the south, add the south neighbor and the north neighbor in the opposite direction
            if row < self.maze_len - 1 and not maze[row + 1][col]:
                graph[(row, col)].append(("S", (row + 1, col)))
                graph[(row + 1, col)].append(("N", (row, col)))

            # If there is a path to the east, add the east neighbor and the west neighbor in the opposite direction
            if col < self.maze_row_len - 1 and not maze[row][col + 1]:
                graph[(row, col)].append(("E", (row, col + 1)))
                graph[(row, col + 1)].append(("W", (row, col)))

        return graph

    def _create_board_elements(self, maze):
        """Method to create all objects of the board.

        Function creates a list of Coin objects as an
        attribute of Board.

        Function creates a list of Block objects as an
        attribute of Board.

        :param maze: list of lists containing integers 0 or 1
                     0 - empty square, floor
                     1 - square with walls
        """
        maze_size = len(maze) - 1                                         # Size of the maze
        coins_append = self.coins.append                                  # Shortcut for appending coins to the list
        blocks_append = self.blocks.append                                # Shortcut for appending blocks to the list
        # Loop through each row in the maze
        for row_no, row in enumerate(maze):
            row_len = len(row) - 1                                        # Length of the row
            # Loop through each square in the row
            for sq_no, square in enumerate(row):
                if not square:
                    coins_append(Coin(sq_no, row_no))                     # If the square is empty, add a coin object to the list
                else:
                    walls = []                                            # Initialize a list to store walls
                    walls_append = walls.append

                    if not all([row_no, maze[row_no - 1][sq_no]]):        # If there is a wall to the north, add 'N' to walls
                        walls_append("N")
                    if not all([sq_no, maze[row_no][sq_no - 1]]):         # If there is a wall to the west, add 'W' to walls
                        walls_append("W")
                    if sq_no == row_len or not maze[row_no][sq_no + 1]:   # If there is a wall to the east, add 'E' to walls
                        walls_append("E")
                    if row_no == maze_size or not maze[row_no + 1][sq_no]:# If there is a wall to the south, add 'S' to walls
                        walls_append("S")
                    blocks_append(Block(sq_no, row_no, ''.join(walls)))   # Create a Block object

    def _create_knots(self, maze):
        """Method to create knots for pathfinding."""
        # Loop through each row in the maze
        for row_no, row in enumerate(maze):
            # Loop through each square in the row
            for sq_no, square in enumerate(row):
                # If the square is not a wall and not at the boundary
                if not bool(square) and bool(row_no) and bool(sq_no) and row_no != self.maze_len-1 and sq_no != self.maze_row_len-1:
                    direction = ""                                             # Initialize an empty string to store the possible directions
                    if not maze[row_no-1][sq_no]:                              # If there is no wall to the north, add 'N' to directions
                        direction += "N"                                       # Add 'N' to the direction string
                    if not maze[row_no][sq_no-1]:                              # If there is no wall to the west, add 'W' to directions
                        direction += "W"                                       # Add 'W' to the direction string
                    if not maze[row_no][sq_no+1]:                              # If there is no wall to the east, add 'E' to directions
                        direction += "E"                                       # Add 'E' to the direction string
                    if not maze[row_no+1][sq_no]:                              # If there is no wall to the south, add 'S' to directions
                        direction += "S"                                       # Add 'S' to the direction string

                    self.knots[(sq_no, row_no)] = direction                    # Store the possible directions in the knots dictionary

    def _create_super_coins(self):
        """Function to create a list of SuperCoin objects as an attribute of Board."""
        return [SuperCoin(coin.pos_x, coin.pos_z) for coin in
                [choice(self.coins) for n in range(self.super_coins_no)]]

    def _draw_floor(self):
        """Function to draw the floor of the board."""
        gl.glBegin(gl.GL_QUADS)                                             # Start drawing a quadrilateral polygon
        set_color(self.floor_color)                                         # Set the color for the floor
        gl.glVertex3f(0, self.floor_level, 0)                               # Define the first vertex
        gl.glVertex3f(self.maze_row_len, self.floor_level, 0)               # Define the second vertex
        gl.glVertex3f(self.maze_row_len, self.floor_level, self.maze_len)   # Define the third vertex
        gl.glVertex3f(0, self.floor_level, self.maze_len)                   # Define the fourth vertex
        gl.glEnd()

    def draw(self):
        """ The main drawing function.

        Function draws all board elements, floor, blocks and coins.
        """

        self._draw_floor()        # draw the board floor
        for block in self.blocks:
            block.draw_block()

        # draw the coins
        for coin in self.coins:
            coin.draw()

        # draw the super_coins
        for coin in self.super_coins:
            coin.draw()
