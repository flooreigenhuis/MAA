### Zo kunnen we een veld maken van zo groot als we willen, ik kom anders in de knoei met 201 als je naar links gaat.
### Dan wordt het 200, 199, 198, ... Dan denkt die dat die op de vorige rij is door 1xx. Denk dat we het zo veel makkelijker maken voor onszelf.
# @autor "Peter Markotic, Floor Eigenhuis"

import random
import numpy as np
import math

w = 5
h = 5
players = 8

#field = [[0 for x in range(w)] for y in range(h)]

# get a list of the possible locations
def getLocations (width, height):
    loc = []
    for h in range (1, height+1):
        for w in range (1, width +1):
            loc.append([h, w])
    return loc

# get the starting locations of the players
def getStartLoc(loc, players):
    playerLoc = {}
    for p in range (1, players+1):
        playerLoc[p] = random.choice(loc)
        loc.remove(playerLoc[p]) #so players don't get the same location
    return playerLoc

def mapToInBounds(x,y):
    if (x > w):
        x = x % w
    if (x < 1):
        x = w + (x % -w)

    if (y > h):
        y = y % h
    if (y < 1):
        y = h + (y % -h)
    return x,y

def move(player, A, playerLocations, width, height, epsilon, radius = 2, speed = 1):
    currentLoc = playerLocations[player]

    if random.random() <= epsilon or (np.count_nonzero(payoffs[player-1]) == 0):
        angle = random.choice(A) # explore
    else:
        angle = A[payoffs[player - 1].index(max(payoffs[player - 1]))] # exploit: get the index of the move that caused the max payoff and play that action

    angle_rad = math.radians(angle) # convert to radians, take cos for y and sin for x value
    x = math.sin(angle_rad) * speed
    y = math.cos(angle_rad) * speed

    x,y = mapToInBounds(x,y)
    currentLoc[0] += x
    currentLoc[1] += y



field = getLocations(w, h)
playerLocations = getStartLoc(field, players)
A = [0, 45, 90, 135, 180, 225, 270, 315]
payoffs = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total payoff for player for a particular move
plays = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total times player has played a move
epsilon = 0.1


print(field)
print(playerLocations)
print(mapToInBounds(0,6))


#################################################



# for x in range(-10, 10, 1):
#     list.append(x)
#
# for y in list:
#     if (y > w):
#         y = y % w
#     if (y < 1):
#         y = w + (y % -w)
#
#     if (y > h):
#         y = y % h
#     if (y < 1):
#         y = h + (y % -h)

# print(list)
# print(list2)
