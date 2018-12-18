# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

#  ______                   _            ___        ____  
# |  ____|                 (_)          |__ \      |___ \ 
# | |__  __  _____ _ __ ___ _ ___  ___     ) | _    __) |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \   / / (_)  |__ < 
# | |____ >  <  __/ | | (__| \__ \  __/  / /_      ___) |
# |______/_/\_\___|_|  \___|_|___/\___| |____|     |____/ 

class QLearningAgent(ReinforcementAgent):
    """
    Q-Learning Agent
    
    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update
    
    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)
    
    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions for a state
    """
    
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.QValues = util.Counter()

    def getQValue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple
        """
        return self.QValues.get((state, action), 0.0)

    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        actions = self.getLegalActions(state)
        if not actions:
            return 0.0
        list_values = []
        for action in actions:
            list_values.append(self.QValues.get(state,action))
        return max(list_values)
        
    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        actions = self.getLegalActions(state)
        if not actions:
            return None
        list_values = []
        for action in actions:
            list_values.append((self.QValues.get(state,action), action))
        max_tuple = max(x for x in list_values)
        return max_tuple[1]


    def getAction(self, state):
        """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise.  Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.
        
        HINT: You might want to use util.flipCoin(prob)
        HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        actions = self.getLegalActions(state)
        if not actions:
            return None
        if util.flipCoin(self.epsilon):
            action = random.choice(actions)
        else:
            action = self.getAction(state)
        return action

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here
        
        NOTE: You should never call this function,
        it will be called on your behalf
        """
        actions = self.QValues.get(nextState)
        max_q = max(self.getQValue(nextState,action) for action in actions)
        self.QValues[state, action] = reward + self.alpha * max_q - self.QValues[state, action]


    def getPolicy(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        return self.computeValueFromQValues(state)

class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

#  ______                   _            _  _   
# |  ____|                 (_)          | || |  
# | |__  __  _____ _ __ ___ _ ___  ___  | || |_ 
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \ |__   _|
# | |____ >  <  __/ | | (__| \__ \  __/    | |  
# |______/_/\_\___|_|  \___|_|___/\___|    |_|  

class ApproximateQAgent(PacmanQAgent):
    """
    ApproximateQLearningAgent

    You should only have to overwrite getQValue
    and update.  All other QLearningAgent functions
    should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
        Should return Q(state,action) = w * featureVector
        where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
        Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        """"
        Called at the end of each game.
        """
        # call the super-class final method
        PacmanQAgent.final(self, state)
        
        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            # print self.getWeights()
            pass
