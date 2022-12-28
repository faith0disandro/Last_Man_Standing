import itertools
import random
import string
import pytest

from time import sleep
from IPython.display import clear_output


def check_bounds(position, size):
    """Check whether the position of a bot
         is within the bound of a grid.
         
    Parameters
    ----------
    position: lst
        The position of a bot
    size: int
        The size of a grid board (int x int)
        
    Returns
    -------
    True or False
        The result of whether the bot is between the 
        bounds of the grid.
    """
    
    for item in position:
        if item < 0 or item == size:
            return False
        
    return True


def add_lists(list1, list2):
    """Adds two lists together.
    
    Parameters
    ----------
    list1: lst
        The first list to be added
    list2: lst
        The second list to be added
        
    Returns
    -------
    output: lst
        The result of a new list with the 
        items of list1 and list2 added together
    """
    
    output = []
    
    for item1, item2 in zip(list1, list2):
        output.append(item1 + item2)
        
    return output


def remove_bot(bots, num_steps):
    """Removes a bot from the list of bots if
        a two bots have the same position.
        
    Parameters
    ----------
    bots: Bot() type or list of Bot() type
        One or more bots to be be removed from the board
    num_steps: int
        Number of moves that each bot has made.
    """
    
    for bot_1, bot_2 in itertools.combinations(bots, 2):
            if bot_1 in bots:
                if num_steps > 1 and bot_1.position == bot_2.position:
                    bots.remove(bot_1)


def obstacle_avoidance(bots, obstacles, num_steps):
    """Makes a bot go back a position if an obstacle
        and the bot have the same position.
        
    Parameters
    ----------
    bots: Bot() type or list of Bot() type
        One or more bots to be be moved
    obstacles: Obstacle() type or list of Obstacle() type
        One or more obstacles to interact with a bot
    num_steps: int
        Number of moves that each bot has made.
    """
    
    for obstacle in obstacles:
        for bot in bots:
            if num_steps != 0 and bot.position == obstacle.position:
                bot.position = bot.last_position



def play_board(bots, num_obstacles, grid_size = 6, sleep_time = .8):
    """Generate a board that includes bots and obstacles. Counts the
        number of moves made by the bots and returns it.
    
    Parameters
    ----------
    bots : Bot() type or list of Bot() type
        One or more bots to be be played on the board
    num_obstacles : int
        Number of obstacles to be placed on the board
    grid_size : int, optional
        Board size. default = 6
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.8.
    """
    
    # Make sure the list contains only Bot objects
    for bot in bots:
        if not isinstance(bot, Bot):
            raise ValueError("Please enter all Bot object.")
    
    # Make sure there is a number for the number of obstacles
    if not isinstance(num_obstacles, int):
        raise ValueError("Please enter an integer for the number of obstacles.")
    
    num_bots = len(bots)
    num_steps = 0
    obstacles_iterator = 0
    obstacles = []
    
    # Make sure there are at least two bots in the list
    if num_bots < 2:
        raise ValueError("Please enter at least two Bots")
    
    # Create the grid
    grid_list = [[' '] * grid_size for ncols in range(grid_size)]
    
    # If input is a single bot, put it in a list so that procedures work
    if not isinstance(bots, list):
        bots = [bots]
    
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size
        
    # Add obstacles to a list if there are obstacles to be added to the board
    if num_obstacles != 0:
        while obstacles_iterator < num_obstacles:
            obstacles.append(Obstacle(grid_size))
            obstacles_iterator += 1
            
        # Update each obstacle to know about the grid_size they are on
        for obstacle in obstacles:
            obstacle.grid_size = grid_size
    
    # Run the board as long as there is more than one bot on the board
    while num_bots > 1:

        # Create the grid
        grid_list = [['.'] * grid_size for ncols in range(grid_size)]
        
        
        # Add bot(s) to the grid
        for bot in bots:
            grid_list[bot.position[0]][bot.position[1]] = bot.character   
       
        # Add obstacle(s) to the grid if there are obstacles to be added
        if num_obstacles != 0:
            for obstacle in obstacles:
                grid_list[obstacle.position[0]][obstacle.position[1]] = obstacle.character    
                
                # At the start of the board if an obstacle has the same position as a bot move the obstacle
                while num_steps == 0 and (obstacle.position == [0,0] or obstacle.position == [1,1] 
                                          or obstacle.position == [2,2]):
                    obstacle.position = [random.choice(range(grid_size)), random.choice(range(grid_size))]
                    grid_list[obstacle.position[0]][obstacle.position[1]] = obstacle.character 
                
        # Remove a bot from the board if two bots have the same position        
        remove_bot(bots, num_steps)
        
        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(lst) for lst in grid_list]))
        sleep(sleep_time)
                
        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()
        
        # Move a bot to its previous position if it interacts with an obstacle
        if num_obstacles != 0:
            obstacle_avoidance(bots, obstacles, num_steps)
        
        # Update the number of bots 
        num_bots = len(bots)
        
        # Update the number of moves
        num_steps += 1
    
    # Print out the number of moves the winning bot has made
    print("Moves: " + str(num_steps))



class Obstacle:
    # Obstacle that blocks a bot
    
    def __init__(self, grid_size):
        """Initializes the Obstacle class with a character and position.
        
        Attributes
        ----------
        character: chr
            Gives the obstacle an image
        position: lst
            Gives the obstacle a random position
        """
        
        self.character = chr(9619)
        self.position = [random.choice(range(grid_size)), random.choice(range(grid_size))]



class Bot:
    # Bot that moves 
    
    def __init__(self, character):
        """Initializes the Bot class with a character, certain range of moves,
            and grid_size.
        
        Attributes
        ----------
        character: chr
            Gives the obstacle an image
        moves: lst of lst
            Allowable moves the bot can take
        grid_size: None
            The size of the playing board
        """
        
        self.character = chr(character)
        self.moves = [[-1, 0], [1,0], [0,1], [0,-1]]
        self.grid_size = None




class WanderBot(Bot):
    # Bot that moves up, down, right, or left and inherits from the Bot class
    
    def __init__(self, character = 9815):
        """Initializes the WanderBot class with attributes from the Bot class
            as well as the bot's position.
        
        Attributes
        ----------
        position: lst
            Position of the bot at square [1, 1] on the board
        """
        
        super().__init__(character)
        self.position = [1, 1]
        
    def wander(self):
        # Moves the bot up, down, left, or right by randomization
        # Returns the new position to the bot
        
        has_new_pos = False
        
        # Move the bot to a new postion either up, down, right, or left
        while not has_new_pos:
            move = random.choice(self.moves)
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
            
        return new_pos
    
    def move(self):
        # Saves the last position of the bot and gives the bot a 
        # new position
        
        self.last_position = self.position
        self.position = self.wander()





class ExploreBot(Bot):
    # Bot that can continue in the same direction that inherits from
    # the Bot class.
    
    def __init__(self, character = 9814, move_prob = .25):
        """Initializes the ExploreBot class with attributes from the Bot class
            as well as a move probability, the bot's position, and the bot's last move.
        
        Attributes
        ----------
        move_prob: float
            Probability that the bot will use it's last move
        position: lst
            Position of the bot at square [2, 2] on the board
        last_move: lst
            Last move the bot used
        """
        
        super().__init__(character)
        self.move_prob = move_prob
        self.position = [2, 2]
        self.last_move = None
        
    def biased_choice(self):
        # Returns the move the bot will take whether it is the 
        # same as it's last move or not
        
        move = None
        
        if self.last_move != None:
            if random.random() < self.move_prob:
                move = self.last_move
                
        if move == None:
            move = random.choice(self.moves)
            
        return move
    
    def explore(self):
        # Returns the bot's position based on the move it will take
        
        has_new_pos = False
        
        while not has_new_pos:
            move = self.biased_choice()
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
            self.last_move = move
            
        return new_pos
    
    def move(self):
        # Saves the last position of the bot and gives the bot a 
        # new position
        
        self.last_position = self.position
        self.position = self.explore()






class TeleportBot(Bot):
    # Bot that can teleport that inherits from the Bot class
    
    def __init__(self, character = 9812, tele_prob = .5):
        """Initializes the TeleportBot class with attributes from the Bot class
            as well as a teleport probability and the bot's position.
        
        Attributes
        ----------
        tele_prob: float
            Probability that the bot will teleport
        position: lst
            Position of the bot at square [0, 0] on the board
        """
        
        super().__init__(character)
        self.tele_prob = tele_prob
        self.position = [0, 0]
        
    def wander(self):
        # Moves the bot up, down, left, or right by randomization
        # Returns the new position to the bot
        
        has_new_pos = False
        
        # Move the bot to a new postion either up, down, right, or left
        while not has_new_pos:
            move = random.choice(self.moves)
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
            self.last_move = move
            
        return new_pos  
        
    def teleport(self):
        # Randomly selects a position on the board
        
        self.lst = [random.choice(range(self.grid_size)), random.choice(range(self.grid_size))]
        
        return self.lst
                
    def move(self):
        # Saves the last position of the bot and gives the bot a 
        # new position whether the bot teleports or not
        
        if random.random() < self.tele_prob:
            self.last_position = self.position
            self.position = self.teleport()
        else:
            self.last_position = self.position
            self.position = self.wander()







def test_bots():
           
    bots = [TeleportBot(), WanderBot(), ExploreBot()]
    obstacles = 5
    
    play_board(bots, obstacles)
    
    
test_bots()