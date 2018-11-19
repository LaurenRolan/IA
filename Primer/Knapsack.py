import math
import os

def knapsack (items, sizeLeft):
    '''Items are a list of tuples[(name, size, value), ...]
    Returns value is tuple([name, name, name], total_value)'''
    if items == []:
        #No more things left to pack
        return ([], 0)
    elif items[0][1] > sizeLeft:
        #Next item is too large
        return knapsack(items[1:], sizeLeft)
    else:
        #Case 1: do not pack this item
        items1, value1 = knapsack(items[1:], sizeLeft)
        #Case 2: do pack this item
        items2, value2 = knapsack(items[1:], sizeLeft - items[0][1])
        if value1 > value2 + items[0][2]:
            return (items1, value1)
        else:
            return ([items[0][0]] + items2, value2+items[0][2])

def manhattan(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def rectangleDiagonal(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def combination(domains, assignements):
    if len(domains) == 0:
        print(assignements + ", ", end='')
    else:
        for character in domains[0]:
            combination(domains[1:], assignements+character)

def createLabyrinth(labyrinth, positions):
    for i in range(0, len(labyrinth)):
        for j in range(0, len(labyrinth[0])):
            if(labyrinth[i][j] == 0):
                print("##", end='')
            elif((j,i) in positions):
                print(". ", end='')
            else:
                print("  ", end='')
        print("")

def get_sucessor_states(x,y,labyrinth):
    sucessor = []
    if y < len(labyrinth[0]) - 1 and labyrinth[y + 1][x] == 1:
        sucessor.append((x, y + 1))
    if y > 0 and labyrinth[y - 1][x] == 1:
        sucessor.append((x, y - 1))
    if x < len(labyrinth) - 1 and labyrinth[y][x + 1] == 1:
        sucessor.append((x + 1, y))
    if x > 0 and labyrinth[y][x - 1] == 1:
        sucessor.append((x - 1, y))
    return sucessor

def depth_first_search( labyrinth, startx, starty, endx, endy ):
    '''Depth-first algorithm using a stack'''
    #Create initial stack with the initial state (the start position)
    initial_state = (startx, starty)
    print("INITIAL" + str(initial_state))
    stack = [[initial_state]]
    visited = [[initial_state]]
    #While the stack is not empty, go on...
    while stack:
        #Get the path at the top of the stack
        current_path = stack.pop()
        #Get the last place of that path
        current_state = current_path[-1]
        visited.append(current_state)
        #Check if we hqve reqched the goal
        if current_state[0] == endx and current_state[1] == endy:
            print("Goal!!" + str(current_state))
            createLabyrinth(labyrinth, current_path[1:])
            return current_path[1:]
        else:
            #Check where you can go from here
            print("")
            next_states = get_sucessor_states(current_state[0], current_state[1], labyrinth)
            next_states = [x for x in next_states if x not in visited]
            createLabyrinth(labyrinth, next_states)
            #Add the new paths (one step longer) to the stack
            for state in next_states:
                #Perform some check here
                stack.append(current_path + [state])
    return visited

def breadth_first_search( labyrinth, startx, starty, endx, endy ):
    '''Depth-first algorithm using a stack'''
    #Create initial stack with the initial state (the start position)
    initial_state = (startx, starty)
    print("INITIAL" + str(initial_state))
    stack = [[initial_state]]
    visited = [[initial_state]]
    #While the stack is not empty, go on...
    while stack:
        #Get the path at the top of the stack
        current_path = stack.pop()
        #Get the last place of that path
        current_state = current_path[-1]
        visited.append(current_state)
        #Check if we hqve reqched the goal
        if current_state[0] == endx and current_state[1] == endy:
            print("Goal!!" + str(current_state))
            createLabyrinth(labyrinth, current_path[1:])
            return current_path[1:]
        else:
            #Check where you can go from here
            print("")
            next_states = get_sucessor_states(current_state[0], current_state[1], labyrinth)
            next_states = [x for x in next_states if x not in visited]
            createLabyrinth(labyrinth, next_states)
            #Add the new paths (one step longer) to the stack
            for state in next_states:
                #Perform some check here
                stack.insert(0, current_path + [state])
    return visited
'''
print(knapsack([("A",3,4),("B",2,2),("C",2,3)],3))
print(knapsack([("A",3,4),("B",2,2),("C",2,3)],4))
print(knapsack([("A",3,4),("B",2,2),("C",2,3)],5))
print(knapsack([("A",3,4),("B",2,2),("C",2,3)],6))
print(knapsack([("A",3,4),("B",2,2),("C",2,3)],7))

print(manhattan((2, 3), (4, 7)))

print(rectangleDiagonal((0,0), (2,2)))
print(rectangleDiagonal((3,2), (5,3)))

domains = [['a','b','c'], ['a'], ['s','d', 'b']]
combination(domains, "")
'''
labyrinth =\
[[0,0,0,0,0,0,1,0],
 [0,1,0,1,1,1,1,0],
 [0,1,1,1,0,1,0,0],
 [0,1,0,0,0,0,0,0],
 [0,1,1,0,1,1,1,0],
 [0,0,1,1,1,0,0,0],
 [0,1,1,0,1,1,1,0],
 [0,1,0,0,0,0,0,0]]
visited =\
[(0,6), (1,6), (1,5),
 (1,4), (1,3), (2,3),
 (2,2), (2,1), (3,1),
 (4,1), (4,2), (5,2),
 (6,2), (6,1), (7,1)]

createLabyrinth(labyrinth, visited)
print(get_sucessor_states(1, 1, labyrinth))
print(get_sucessor_states(6, 1, labyrinth))

#print("Depth-First Search")
#print(depth_first_search(labyrinth, 6, 0, 1, 7))
print("")
print("Breadth-First Search")
print(breadth_first_search(labyrinth, 6, 0, 1, 7))

