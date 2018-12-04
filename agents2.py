# -*- coding: utf-8 -*-
#
# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1
#

#
# @file agents.py
#
# @author Régis Clouard.
#

from grid import Grid
import random
from samples import *
import copy

class Agent:
    """
    Abstract class for the solvers that implements the
    Strategy design pattern.
    YOU DO NOT NEED TO CHANGE ANYTHING IN THIS CLASS, EVER.
    """
    def __init__( self ):
        self.count = 0;
        self.clock = ['|', '/', '-', '\\']

    def incrementCount( self):
        self.count += 1;
        self.displayTime()
        
    def displayTime( self ):
        print "\b\b\b" + self.clock[self.count % 4], 

    def solve( self, grid ):
        """ This is the method to implement for each specific solver."""
        raise Exception, "Invalid CSPSolver class, Solve() not implemented"

#######
####### Backtracking Search Agent
#######    
class BS( Agent ):
    """ Backtracking version of the solver based on simple
    uninformed backtracking search: recursive depth-first search."""
    
    def solve( self, grid ):
        """ Returns a solution as a dictionary of assignment
        eg: {0:'2', 1:'3', ..., 40:'5'}
        or None if no solution is found.
        @param grid a reference to the current puzzle grid."""
        domains = grid.getDomainValues()
        return self.__recursiveBacktracking(grid, domains, {})

    def __recursiveBacktracking( self, grid, domains, assignment ):
        """ Implements a recursive search.
        Returns the solution as list or None. """
        self.incrementCount()
        if len(domains) == 0: # All cells set
            if self.__isGoal(grid, assignment):
                return assignment
            return None

        variable, values =  domains.popitem()
        newAssignment = copy.deepcopy(assignment)
        for value in values:
            # Use a deep copy of domains to avoid backtracking issues.
            newAssignment[variable] = value
            solution = self.__recursiveBacktracking(grid, copy.deepcopy(domains), newAssignment)
            if solution:
                return solution
        return None

    def __isGoal( self, grid, assignment ):
        """ Tests if the assignment is a solution.
        ie. that there is not doubles in each boxes, lines and columns.
        @param assignment a dictionary with the current assignment.
        """
        for variable, value in assignment.iteritems():
            for cell in grid.getRelatedCells(variable):
                if assignment[variable] == assignment[cell]:
                    return False
        return True

def defaultHeuristic( domains, assignment, grid ):
    """ Picks the first free variable."""
    for cell, p in domains.iteritems():
        if cell not in assignment:
            return cell
                               

#  ______                   _            __ 
# |  ____|                 (_)          /_ |
# | |__  __  _____ _ __ ___ _ ___  ___   | |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  | |
# | |____ >  <  __/ | | (__| \__ \  __/  | |
# |______/_/\_\___|_|  \___|_|___/\___|  |_|

class FC( Agent ):
    def solve( self, grid, heuristicFunction = defaultHeuristic ):
        """ Forward Checking.

        Returns a solution as a dictionary of assignment, eg: {0:'2', 1:'3', ...40:'5'}
        or None if no solution is found.
        @param grid the current puzzle grid.
        @param heuristicFunction the function used to choose the next cell to considered.
        """
        return self.recursiveSearch({}, grid.getDomainValues(), grid, heuristicFunction)
        
    def recursiveSearch(self, assignment, domains, grid, heuristicFunction):
        self.incrementCount()
        if domains.keys() == assignment.keys():
            if all(domains[key] for key in assignment.keys()):
                return assignment
        current = heuristicFunction(domains, assignment, grid)
        for value in domains[current]:
            assignment[current] = value
            domains1 = self.forwardChecking(current, value, copy.deepcopy(domains), grid)
            if domains1 != None:
                result = self.recursiveSearch(assignment, domains1, grid, heuristicFunction)
                if result != None:
                    return assignment
            del assignment[current]
        return None
    
    def forwardChecking(self, var, value, domain, grid):
        list_of_dependencies = grid.getRelatedCells(var)
        for dep in list_of_dependencies:
            if value in domain[dep]:
                domain[dep].remove(value)
                if not domain[dep]:
                    return None
        return domain

#  ______                   _            ___  
# |  ____|                 (_)          |__ \ 
# | |__  __  _____ _ __ ___ _ ___  ___     ) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \   / / 
# | |____ >  <  __/ | | (__| \__ \  __/  / /_ 
# |______/_/\_\___|_|  \___|_|___/\___| |____|
 
def myHeuristic(domains, assignment, grid):
    """ The best heuristic """
    for cell, p in domains.iteritems():
        if cell not in assignment:
            if len(p) < 3:
                return cell

#  ______                   _            ____  
# |  ____|                 (_)          |___ \ 
# | |__  __  _____ _ __ ___ _ ___  ___    __) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  |__ < 
# | |____ >  <  __/ | | (__| \__ \  __/  ___) |
# |______/_/\_\___|_| \___|_|___/\___| |____/ 

class AC3( Agent ):
    def solve( self, grid, heuristicFunction = defaultHeuristic ):
        """ Arc Consistency as preprocessing.
        Returns the domain of values after applying
        the arc consistency technique.

        @param grid the current puzzle grid.
        @param heuristicFunction the function is used to choose the next cell to considered."""

        "*** YOUR CODE HERE ***"
        raise Exception, "Method not implemented: solve()"

#  ______                   _            _  _   
# |  ____|                 (_)          | || |  
# | |__  __  _____ _ __ ___ _ ___  ___  | || |_ 
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |__   _|
# | |____ >  <  __/ | | (__| \__ \  __/    | |  
# |______/_/\_\___|_|  \___|_|___/\___|    |_|  

class AC_FC( Agent ):
    def solve( self, grid, heuristicFunction = defaultHeuristic ):
        """ Forward Checking with Arc Consistency as preprocessing.
        Returns a solution as a dictionary of assignment, eg: {0:'2', 1:'3', ...40:'5'}
        or None if no solution is found.

        @param grid the current puzzle grid.
        @param heuristicFunction the function used to choose the next cell to considered."""

        "*** YOUR CODE HERE ***"
        raise Exception, "Method not implemented: solve()"

#  ______                   _            _____ 
# |  ____|                 (_)          | ____|
# | |__  __  _____ _ __ ___ _ ___  ___  | |__  
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |___ \ 
# | |____ >  <  __/ | | (__| \__ \  __/  ___) |
# |______/_/\_\___|_|  \___|_|___/\___| |____/ 
                                              
class AC_AC( Agent ):
    def solve( self, grid, heuristicFunction = defaultHeuristic ):
        """ Maintaining Arc Consistency.
        Returns a solution as a list of assignment, eg: ['2', '3', ...'5']
        for each cell of the grid.
        @param grid the current puzzle grid.
        @param heuristicFunction the function used to choose the next cell to considered."""

        "*** YOUR CODE HERE ***"
        raise Exception, "Method not implemented: solve()"
