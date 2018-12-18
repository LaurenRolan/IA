# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import sys
import mdp, util
import pdb

from learningAgents import ValueEstimationAgent

#  ______                   _            __ 
# |  ____|                 (_)          /_ |
# | |__  __  _____ _ __ ___ _ ___  ___   | |
# |  __| \ \/ / _ \ '__/ __| / __|/ _ \  | |
# | |____ >  <  __/ | | (__| \__ \  __/  | |
# |______/_/\_\___|_|  \___|_|___/\___|  |_|

class ValueIterationAgent(ValueEstimationAgent):
    """
    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.
    """
    
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.
        
        Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default values as 0
        "*** YOUR CODE HERE ***"
        states = mdp.getStates()
        for k in range(0, iterations):
            for state in states:
                actions = []
                for action in mdp.getPossibleActions(state):
                    trans_prob = mdp.getTransitionStatesAndProbs(state, action)
                    actions.append(sum(self.values[tp[0], k-1] * tp[1] for tp in trans_prob))
                if actions:
                    max_prob = max(actions)
                else:
                    max_prob = 0
                self.values[state, k] = mdp.getReward(state) + discount * max_prob  

    def getValue(self, state):
        """
        Returns the value of the state (computed in __init__).
        """
        return self.values[state, self.iterations-1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """ 
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
    
    def computeActionFromValues(self, state):
        """
        The policy is the best action in the given state
        according to the values currently stored in self.values.
        
        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        actions  = self.mdp.getPossibleActions(state)
        if not actions:
            return None
        max_prob = [] 
        for action in actions:
            trans_prob = self.mdp.getTransitionStatesAndProbs(state, action)
            somme = 0
            for tp in trans_prob:
                somme += self.values[tp[0], self.iterations] * tp[1]
            max_prob.append((sum(self.values[tp[0], self.iterations-1] * tp[1] for tp in trans_prob), action))
        max_tuple = max(x for x in max_prob)
        return max_tuple[1]
       

    def computeQValueFromValues(self, state, action):
        """
        Compute the Q-value of action in state from the
        value function stored in self.values.
        """
        if self.mdp.isTerminal(state):
            return self.mdp.getReward(state)
        trans_prob = self.mdp.getTransitionStatesAndProbs(state, action)
        return sum(self.values[tp[0], self.iterations-1] * tp[1] for tp in trans_prob)
