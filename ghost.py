from random import choice
from time import time

from OpenGL import GL as gl
from OpenGL import GLUT as glut

from pacman import PacMan
from heapq import heappop, heappush
from solid_data import MOVES, OPPOSITE_MOVES, set_color

# Class Ghost inherits from PacMan class
class Ghost(PacMan):
    def __init__(self, pos_x, pos_z, direction, color):
        # Constructor for the Ghost class
        super().__init__(pos_x, pos_z)             # Calling the constructor of the parent class (PacMan)
        self.primary_color = color                 # Setting the primary color of the ghost
        self.step = 0.1                            # Setting the step size for the ghost's movement
        self.eatable_time = 0                      # Initializing the time when the ghost becomes eatable
        self.eatable = False                       # Initializing the eatable state of the ghost
        self.the_way = None                        # Initializing the path for the ghost to follow
        self.direction = ""                        # Initializing the current direction of the ghost
        self.next_direction = direction            # Setting the next direction for the ghost

    def choice_next_direction(self):
        """Randomly choose the next direction for the ghost."""
        self.next_direction = choice(              # Choose a random direction excluding the opposite of the current direction
            MOVES.replace(OPPOSITE_MOVES[self.direction], "")
        )

    def draw(self):
        """Draw the ghost in the OpenGL context."""
        set_color(self.color)
        gl.glPushMatrix()                                          # Push the current matrix stack to save the current transformation state
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)   # Translate the ghost to its position in the maze
        gl.glRotate(self.rotate, 0, 1, 0)                          # Rotate the ghost based on its current rotation value
        glut.glutSolidSphere(self.radius, 10, 10)                  # Render the ghost as a solid sphere
        gl.glPopMatrix()                                           # Pop the matrix stack to restore the previous transformation state

    def was_eaten_by_pacman(self):
        """Set the ghost's state to indicate it was eaten by Pac-Man."""
        self.color = 0.5, 0.5, 0.5                             # Set the color of the ghost to gray
        self.was_eaten = True                                  # Set the was_eaten flag to True

    def start_from_nest(self):
            self.eatable_time = 0                              # Initializing the time when the ghost becomes eatable to zero
            self.eatable = False                               # Boolean flag to indicate whether the ghost is eatable
            self.the_way = None                                # Path that the ghost will follow, initially set to None
            self.was_eaten = False                             # Reset the was_eaten flag to False
            self.color = self.primary_color                    # Restor the ghost's orignal color
            self.next_direction = "N"                          # Set the next direction to North
    def become_eatable(self):
        """Make the ghost eatable and change its color."""
        if not self.eatable:
            self.eatable, self.color = True, (0.75, 0.75, 0.75)# Set the ghost to be eatable and change its color to light gray
        self.eatable_time = time()                             # Record the time as the start of the eatable period

    def become_not_eatable(self):
        """Revert the ghost to its non-eatable state after a set time."""
        if time() - self.eatable_time >= 10 and not self.was_eaten:# If the eatable time has passed 10 seconds and the ghost has not been eaten
            self.eatable, self.color = False, self.primary_color
            self.eatable_time = 0                              # Reset the eatable time to zero

    @staticmethod
    def heuristic(cell, goal):
        """Calculate the heuristic (Manhattan distance) between two cells."""
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) # Return the sum of the absolute differences between the cell and goal coordinates

    def find_path(self, maze_graph, goal_position):
        """Find the shortest path to the goal using the A* algorithm."""
        start, goal = (self.pos_z, self.pos_x), goal_position   # Define the start position (current position) and goal position
        pr_queue = []                                           # Initialize the priority queue
        heappush(                                               # Push the start node into the priority queue with its priority (cost + heuristic), cost, path, and position
                pr_queue,
                (0 + self.heuristic(start, goal), 0, "", start)
        )        
        visited = set()                                          # Initialize the set of visited nodes
        graph = maze_graph                                       # Reference to the maze graph

        # Loop until the priority queue is empty
        while pr_queue:
            _, cost, path, current = heappop(pr_queue)            # Pop the node with the lowest priority from the queue
            if current == goal:
                self.the_way = path
                break                       # If the curent node is the goal, set the path and break the loop
            if current in visited:
                continue                    # If the current nod has been visited, skip it
            visited.add(current)            # Mark the current node as visited
            for direction, neighbour in graph[current]:                
                # Push the neighboring nodes into the priority queue with updated cost and path
                heappush(
                    pr_queue,
                    (cost + self.heuristic(neighbour, goal),
                     cost + 1, path + direction, neighbour)
                )
