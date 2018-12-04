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
# @author John DeNero and Dan Klein - UC Berkeley
# @version Regis Clouard.
#

from utils import manhattanDistance
from game import Directions
import random, utils

from game import Agent

def scoreEvaluationFunction( currentGameState ):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

######
###### Abstract class SearchAgent
######

class SearchAgent( Agent ):
  """
    This abstract class provides some common elements to all of your
    agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here.
  """

  def __init__( self, evalFn = 'scoreEvaluationFunction', depth = '2' ):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = utils.lookup(evalFn, globals())
    self.depth = int(depth)

  def isTerminalNode( self, gameState, depth ):
    return gameState.isLose() or gameState.isWin() or depth == 0

class MinimaxAgent1( SearchAgent ):
  """
  Minimax agent assuming that there exists only one ghost. 
  """

  def getAction( self, gameState ):
    """
    Returns the minimax action from the current gameState using self.depth
    and self.evaluationFunction.
    """
    legalActions = gameState.getLegalActions(0)
    nextStatesFromLegalActions = [gameState.generateSuccessor(0, action) for action in legalActions]
    values = [self.miniMaxValue(1, nextGameState, self.depth - 1) for nextGameState in nextStatesFromLegalActions] 

    # Get the index of all maxValue
    listOfAllMaxValues = []
    maxValue = max(values)    
    for i in range(0, len(values)):
      if values[i] == maxValue:
        listOfAllMaxValues.append(i)
        
    # Random when there is a tie
    idx = random.randint(0, len(listOfAllMaxValues) - 1)
    action = legalActions[listOfAllMaxValues[idx]]
    return action

  def miniMaxValue( self, agentIndex, gameState, depth ):
    if self.isTerminalNode(gameState, depth):
      return self.evaluationFunction(gameState)    
    else:
      legalActions = gameState.getLegalActions(agentIndex)
      nextStatesFromLegalActions = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
      if agentIndex == 0: # if it's Pacman then it's a max layer
        return max([self.miniMaxValue(1 - agentIndex, nextState, depth - 1) for nextState in nextStatesFromLegalActions])
      else: # else if it's the ghost, then it's a min layer
        return min([self.miniMaxValue(1 - agentIndex, nextState, depth - 1) for nextState in nextStatesFromLegalActions])

#  ______                   _            __ 
# |  ____|                 (_)          /_ |
# | |__  __  _____ _ __ ___ _ ___  ___   | |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  | |
# | |____ >  <  __/ | | (__| \__ \  __/  | |
# |______/_/\_\___|_|  \___|_|___/\___|  |_|

class MinimaxAgentN( SearchAgent ):
  """
  Minimax agent with n ghosts.
  """
  def getAction( self, gameState ):
    """
    Returns the minimax action from the current gameState using self.depth
    and self.evaluationFunction.
    """
    legalActions = gameState.getLegalActions(0)
    nextStatesFromLegalActions = [gameState.generateSuccessor(0, action) for action in legalActions]
    values = [self.miniMaxValue(1, nextGameState, self.depth - 1) for nextGameState in nextStatesFromLegalActions] 

    # Get the index of all maxValue
    listOfAllMaxValues = []
    maxValue = max(values)    
    for i in range(0, len(values)):
      if values[i] == maxValue:
        listOfAllMaxValues.append(i)
        
    # Random when there is a tie
    idx = random.randint(0, len(listOfAllMaxValues) - 1)
    action = legalActions[listOfAllMaxValues[idx]]
    return action

  def miniMaxValue( self, agentIndex, gameState, depth ):
    if self.isTerminalNode(gameState, depth):
      return self.evaluationFunction(gameState)    
    else:
      legalActions = gameState.getLegalActions(agentIndex)
      nextStatesFromLegalActions = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
      if agentIndex == 0:
        # if it's Pacman then it's a max layer
        return max([self.miniMaxValue(1 + agentIndex, nextState, depth - 1) for nextState in nextStatesFromLegalActions])
      else: # else if it's the ghost, then it's a min layer
        if gameState.getNumberOfAgents() - agentIndex - 1 == 0:
          return min([self.miniMaxValue(0, nextState, depth - 1) for nextState in nextStatesFromLegalActions])
        return min([self.miniMaxValue(1 + agentIndex, nextState, depth - 1) for nextState in nextStatesFromLegalActions])
    

#  ______                   _            ___  
# |  ____|                 (_)          |__ \ 
# | |__  __  _____ _ __ ___ _ ___  ___     ) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \   / / 
# | |____ >  <  __/ | | (__| \__ \  __/  / /_ 
# |______/_/\_\___|_|  \___|_|___/\___| |____|

class AlphaBetaAgent(SearchAgent):
  """ 
  Your minimax agent with alpha-beta pruning.
  """
  
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    legalActions = gameState.getLegalActions(0)
    nextStatesFromLegalActions = [gameState.generateSuccessor(0, action) for action in legalActions]
    values = [self.miniMaxValue(-9999, 9999, 1, nextGameState, self.depth - 1) for nextGameState in nextStatesFromLegalActions] 

    # Get the index of all maxValue
    listOfAllMaxValues = []
    maxValue = max(values)    
    for i in range(0, len(values)):
      if values[i] == maxValue:
        listOfAllMaxValues.append(i)
        
    # Random when there is a tie
    idx = random.randint(0, len(listOfAllMaxValues) - 1)
    action = legalActions[listOfAllMaxValues[idx]]
    return action

  def miniMaxValue( self, alpha, beta, agentIndex, gameState, depth ):
    if self.isTerminalNode(gameState, depth):
      return self.evaluationFunction(gameState)    
    else:
      legalActions = gameState.getLegalActions(agentIndex)
      nextStatesFromLegalActions = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
      if agentIndex == 0:
        # if it's Pacman then it's a max layer
        return self.max_val(alpha, beta, 1 + agentIndex, nextStatesFromLegalActions, depth - 1) 
      else: # else if it's the ghost, then it's a min layer
        if gameState.getNumberOfAgents() - agentIndex - 1 == 0:  
          return self.min_val(alpha, beta, 0, nextStatesFromLegalActions, depth - 1)
        return self.min_val(alpha, beta, 1 + agentIndex, nextStatesFromLegalActions, depth - 1)

  def max_val(self, alpha, beta, agentIndex, nextStates, depth):
    v = -9999
    for state in nextStates:
      v = max(v, self.miniMaxValue(alpha, beta, agentIndex, state, depth))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v
  
  def min_val(self, alpha, beta, agentIndex, nextStates, depth):
    v = 9999
    for state in nextStates:
      v = min(v, self.miniMaxValue(alpha, beta, agentIndex, state, depth))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v
    

#  ______                   _            ____  
# |  ____|                 (_)          |___ \ 
# | |__  __  _____ _ __ ___ _ ___  ___    __) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  |__ < 
# | |____ >  <  __/ | | (__| \__ \  __/  ___) |
# |______/_/\_\___|_| \___|_|___/\___|  |____/ 

class ExpectimaxAgent( SearchAgent ):
  """
  Expectimax agent assuming random ghosts.
  """
  def getAction( self, gameState ):
    """
    Returns the minimax action from the current gameState using self.depth
    and self.evaluationFunction.
    """
    legalActions = gameState.getLegalActions(0)
    nextStatesFromLegalActions = [gameState.generateSuccessor(0, action) for action in legalActions]
    values = [self.expectiMax(1, nextGameState, self.depth - 1) for nextGameState in nextStatesFromLegalActions] 

    # Get the index of all maxValue
    listOfAllMaxValues = []
    maxValue = max(values)    
    for i in range(0, len(values)):
      if values[i] == maxValue:
        listOfAllMaxValues.append(i)
        
    # Random when there is a tie
    idx = random.randint(0, len(listOfAllMaxValues) - 1)
    action = legalActions[listOfAllMaxValues[idx]]
    return action

  def expectiMax( self, agentIndex, gameState, depth ):
    if self.isTerminalNode(gameState, depth):
      return self.evaluationFunction(gameState)    
    else:
      legalActions = gameState.getLegalActions(agentIndex)
      nextStatesFromLegalActions = [gameState.generateSuccessor(agentIndex, action) for action in legalActions]
      if agentIndex == 0:
        # if it's Pacman then it's a max layer
        return self.max_val( 1 + agentIndex, nextStatesFromLegalActions, depth - 1) 
      else: # else if it's the ghost, then it's a min layer
        if gameState.getNumberOfAgents() - agentIndex - 1 == 0:  
          return self.min_val(0, nextStatesFromLegalActions, depth - 1)
        return self.min_val( 1 + agentIndex, nextStatesFromLegalActions, depth - 1)

  def max_val(self, agentIndex, nextStates, depth):
    v = -9999
    for state in nextStates:
      v = max(v, self.expectiMax(agentIndex, state, depth))
    return v
  
  def min_val(self, agentIndex, nextStates, depth):
    v = 9999
    for state in nextStates:
      v = min(v, self.expectiMax(agentIndex, state, depth))
    return v
      
    
#  ______                   _            _  _   
# |  ____|                 (_)          | || |  
# | |__  __  _____ _ __ ___ _ ___  ___  | || |_ 
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |__   _|
# | |____ >  <  __/ | | (__| \__ \  __/    | |  
# |______/_/\_\___|_|  \___|_|___/\___|    |_|  
                                               
def betterEvaluationFunction( currentGameState ):
  """
  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
  evaluation function.
  Returns an integer that estimates the state vaue.
  """
  
  " *** YOUR CODE HERE ***"
  if currentGameState.isWin():
    return 1000
  elif currentGameState.isLose():
    return -1000

  foodEaten = currentGameState.getTotalFood() - currentGameState.getNumberOfFood()
  foodEaten *= 3
  nbKilledGhosts = 10 * currentGameState.getNumberOfKilledGhosts()
  capsEaten = currentGameState.getTotalCapsules() - currentGameState.getNumberOfCapsules()
  capsEaten *= 3

  return foodEaten + nbKilledGhosts + capsEaten
  
better = betterEvaluationFunction
