# -*- coding: utf-8; mode: python -*-

# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1

# @file agents.py
#
# @author Régis Clouard

from board import Board
from collections import deque
import random
import copy

MAX_PATH_LENGTH = 100

class Solver:
    """
    Abstract class for the solvers that implement the
    various search strategies.
    It is based on the Design Pattern Strategy (abstract
    method is search()).

    YOU DO NOT NEED TO CHANGE ANYTHING IN THIS CLASS, EVER.
    """
    def __init__( self ):
        self.count = 0

    def search( self, initial_state ):
        """ This is the method to implement for each specific searcher."""
        raise Exception, "Invalid Solver class, search() not implemented"

#######
####### Depth-First Search
#######
class DFS( Solver ):
    
    def search( self, initial_state ):
        """ Depth-First Search using a stack.
        
        It returns the path as a list of boards (states).
        """

        # Create initial stack with the initial state (the start position)
        lifo = [ [initial_state] ]
        visited = set([initial_state]) # keep already explored positions
        while lifo:
            self.count += 1
            # Get the path at the top of the stack
            current_path = lifo.pop()
            # Get the last place of that path
            current_state = current_path[-1]

            # board.display(current_path)
            # raw_input("Next")

            # Check if we have reached the goal
            if current_state.is_goal():
                return current_path
            else:
                # Check where we can go from here
                next_states = current_state.get_successors()
                # Add the new paths (one step longer) to the stack
                for state in next_states:
                    if state not in visited: # Avoid loop!
                        visited.add(state)
                        lifo.append(current_path + [state])
        return [] # No solution

#  ______                   _            __ 
# |  ____|                 (_)          /_ |
# | |__  __  _____ _ __ ___ _ ___  ___   | |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  | |
# | |____ >  <  __/ | | (__| \__ \  __/  | |
# |______/_/\_\___|_|  \___|_|___/\___|  |_|

class BFS( Solver ):
    def search( self, initial_state ):
        """ Breadth-First Search using a queue

        It returns the path as a list of boards (states).
        """
        # Create initial stack with the initial state (the start position)
        fifo = [ [initial_state] ]
        visited = set([initial_state]) # keep already explored positions
        while fifo:
            self.count += 1
            # Get the path at the top of the stack
            current_path = fifo.pop()
            # Get the last place of that path
            current_state = current_path[-1]

            # board.display(current_path)
            # raw_input("Next")

            # Check if we have reached the goal
            if current_state.is_goal():
                return current_path
            else:
                # Check where we can go from here
                next_states = current_state.get_successors()
                # Add the new paths (one step longer) to the stack
                for state in next_states:
                    if state not in visited: # Avoid loop!
                        visited.add(state)
                        fifo.insert(0, current_path + [state])
        return [] # No solution

#  ______                   _            ___  
# |  ____|                 (_)          |__ \ 
# | |__  __  _____ _ __ ___ _ ___  ___     ) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \   / / 
# | |____ >  <  __/ | | (__| \__ \  __/  / /_ 
# |______/_/\_\___|_|  \___|_|___/\___| |____|

def my_heuristic( state ):
    """ Heuristic value.
    
    """
    board = state.get_board()
    tip = 2
    value = 0
    for i in range(2, len(board)):
    	#Find tip of car
    	if board[2][i] == 'X':
    		tip = i
    	#If it is not in the exit
    	elif i > tip:
    		#If there is something between the exit and the car
    		if board[2][i] != ' ':
    			value += 5
    return value

#######
####### Greedy Best First Search
#######
class GBFS( Solver ):

    def search( self, initial_state ):
        """
        Greedy Best-First Search.
        
        It returns the path as a list of boards (states).
        """

        from utils import PriorityQueue
        priority_queue = PriorityQueue()
        h = my_heuristic(initial_state)
        priority_queue.push([initial_state], h)
        visited = set([initial_state]) # keep already explored positions

        while not priority_queue.isEmpty():
            self.count += 1
            # Get the path at the top of the queue
            current_path, cost = priority_queue.pop()
            # Get the last place of that path
            current_state = current_path[-1]

            # board.display(current_path)
            # raw_input("Next")

            # Check if we have reached the goal
            if current_state.is_goal():
                return current_path
            else:
                # Check where we can go from here
                next_states = current_state.get_successors()
                # Add the new paths (one step longer) to the queue
                for state in next_states:
                    if state not in visited: # Avoid loop!
                        visited.add(state)
                        h = my_heuristic(state)
                        priority_queue.push((current_path + [ (state) ]), h )

        return [] # No solution

#  ______                   _            ____  
# |  ____|                 (_)          |___ \ 
# | |__  __  _____ _ __ ___ _ ___  ___    __) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  |__ < 
# | |____ >  <  __/ | | (__| \__ \  __/  ___) |
# |______/_/\_\___|_|  \___|_|___/\___| |____/ 

class AS( Solver ):

    def search( self, initial_state ):
        """
        A* Search.

        It returns the path as a list of boards (states).
        """
        from utils import PriorityQueue
        priority_queue = PriorityQueue()
        h = my_heuristic(initial_state)
        g = 0
        priority_queue.push([initial_state], h)
        visited = set([initial_state]) # keep already explored positions

        while not priority_queue.isEmpty():
            self.count += 1
            # Get the path at the top of the queue
            current_path, cost = priority_queue.pop()
            # Get the last place of that path
            current_state = current_path[-1]

            # board.display(current_path)
            # raw_input("Next")

            # Check if we have reached the goal
            if current_state.is_goal():
                return current_path
            else:
                # Check where we can go from here
                next_states = current_state.get_successors()
                # Add the new paths (one step longer) to the queue
                for state in next_states:
                    if state not in visited: # Avoid loop!
                        visited.add(state)
                        h = my_heuristic(state)
                        priority_queue.push((current_path + [ (state) ]), h + g)
                    	g += 1
        return [] # No solution
#  ______                   _            _  _   
# |  ____|                 (_)          | || |  
# | |__  __  _____ _ __ ___ _ ___  ___  | || |_ 
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |__   _|
# | |____ >  <  __/ | | (__| \__ \  __/    | |  
# |______/_/\_\___|_|  \___|_|___/\___|    |_|  

class IDS( Solver ):

    def search( self, initial_state ):
        """ Iterative Deepening Search.
        
        It returns the path as a list of boards (states).
        """
        for depth in range(2, 100):
        	explored = {}
	        lifo = [ [initial_state] ]
	        while lifo:
	            self.count += 1
	            # Get the path at the top of the stack
	            current_path = lifo.pop()
	            # Get the last place of that path
	            current_state = current_path[-1]

	            # board.display(current_path)
	            # raw_input("Next")

	            # Check if we have reached the goal
	            if current_state.is_goal():
	                return current_path
	            elif len(current_path) < depth:
	                # Check where we can go from here
	                next_states = current_state.get_successors()
	                # Add the new paths (one step longer) to the stack
	                for state in next_states:
	                    if state not in explored or explored[state] > len(current_path): # Avoid loop!
	                        explored[state] = len(current_path)
	                        lifo.append(current_path + [state])
	return [] # No solution

#  ______                   _            _____ 
# |  ____|                 (_)          | ____|
# | |__  __  _____ _ __ ___ _ ___  ___  | |__  
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |___ \ 
# | |____ >  <  __/ | | (__| \__ \  __/  ___) |
# |______/_/\_\___|_|  \___|_|___/\___| |____/ 

class UCS( Solver ):

    def search( self, initial_state ):
        """
        Uniform-Costs Search.
        
        It returns the path as a list of boards (states).
        """
        from utils import PriorityQueue
        priority_queue = PriorityQueue()
        priority_queue.push([initial_state], 0)
        visited = set([initial_state]) # keep already explored positions
        g = 0
        while not priority_queue.isEmpty():
            self.count += 1
            # Get the path at the top of the stack
            current_path, cost = priority_queue.pop()
            # Get the last place of that path
            current_state = current_path[-1]

            # Check if we have reached the goal
            if current_state.is_goal():
                return current_path
            else:
                # Check where we can go from here
                next_states = current_state.get_successors()
                # Add the new paths (one step longer) to the stack
                for state in next_states:
                    if state not in visited: # Avoid loop!
                        visited.add(state)
                        priority_queue.push(current_path + [state], g)
                g += 1
        return [] # No solution

#  ______                   _              __  
# |  ____|                 (_)            / /  
# | |__  __  _____ _ __ ___ _ ___  ___   / /_  
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ | '_ \ 
# | |____ >  <  __/ | | (__| \__ \  __/ | (_) |
# |______/_/\_\___|_|  \___|_|___/\___|  \___/ 

class IDAS( Solver ):

    def search( self, initial_state ):
        """ Iterative A* using a stack.
        
        It returns the path as a list of boards (states).
        """
        from utils import PriorityQueue
        for depth in range(2, 100): 
	        priority_queue = PriorityQueue()
	        h = my_heuristic(initial_state)
	        g = 0
	        priority_queue.push([initial_state], h)
	        explored = {}
	        while not priority_queue.isEmpty():
	            self.count += 1
	            # Get the path at the top of the queue
	            current_path, cost = priority_queue.pop()
	            # Get the last place of that path
	            current_state = current_path[-1]

	            # board.display(current_path)
	            # raw_input("Next")

	            # Check if we have reached the goal
	            if current_state.is_goal():
	                return current_path
	            elif len(current_path) < depth:
	                # Check where we can go from here
	                next_states = current_state.get_successors()
	                # Add the new paths (one step longer) to the queue
	                for state in next_states:
	                    if state not in explored or explored[state] > len(current_path): # Avoid loop!
	                        explored[state] = len(current_path)
	                        h = my_heuristic(state)
	                        priority_queue.push((current_path + [ (state) ]), h + g)
	                    	g += 1
        return [] # No solution
