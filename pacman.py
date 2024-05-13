from OpenGL import GL as gl
from OpenGL import GLUT as glut

from solid_data import set_color


class PacMan:
    def __init__(self, pos_x, pos_z):
        # Setting the initial position on the x-axis
        self.pos_x = pos_x
        # Setting the initial position on the z-axis
        self.pos_z = pos_z
        # Initializing the current movement direction (N, S, W, E)
        self.direction = ''
        # Initializing the next movement direction (N, S, W, E)
        self.next_direction = ''

        # Setting the radius of Pac-Man (size of the character)
        self.radius = 0.5
        # Setting the initial rotation angle for the character's orientation
        self.rotate = 0
        # Setting the step size for each movement (distance moved per step)
        self.step = 0.1
        # Setting the color of Pac-Man (yellow)
        self.color = 1, 1, 0
        # Initializing the was_eaten flag to indicate if Pac-Man has been eaten
        self.was_eaten = False

    # Method to move Pac-Man based on the current direction
    def move(self):
        # If the direction is North, move up (decrease z-coordinate)
        if self.direction == 'N':
            self.pos_z -= self.step
            # Set the rotation angle to 0 degrees (facing North)
            self.rotate = 0

        # If the direction is South, move down (increase z-coordinate)
        elif self.direction == 'S':
            self.pos_z += self.step
            # Set the rotation angle to 180 degrees (facing South)
            self.rotate = 180

        # If the direction is West, move left (decrease x-coordinate)
        elif self.direction == 'W':
            self.pos_x -= self.step
            # Set the rotation angle to 90 degrees (facing West)
            self.rotate = 90

        # If the direction is East, move right (increase x-coordinate)
        elif self.direction == 'E':
            self.pos_x += self.step
            # Set the rotation angle to 270 degrees (facing East)
            self.rotate = 270

        # Round the position coordinates to 2 decimal places for precision
        self.pos_x, self.pos_z = round(self.pos_x, 2), round(self.pos_z, 2)

    # Method to draw Pac-Man in the 3D environment
    def draw(self):
        # Set the drawing color to Pac-Man's color
        set_color(self.color)
        # Push the current matrix stack to save the current transformation state
        gl.glPushMatrix()
        # Translate to Pac-Man's position, adding 0.5 to center within the grid cell
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)
        # Rotate Pac-Man based on the current rotation angle
        gl.glRotate(self.rotate, 0, 1, 0)
        # Draw Pac-Man as a solid sphere with the specified radius
        glut.glutSolidSphere(self.radius, 10, 10)
        # Pop the matrix stack to restore the previous transformation state
        gl.glPopMatrix()

