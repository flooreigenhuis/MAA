### Zo kunnen we een veld maken van zo groot als we willen, ik kom anders in de knoei met 201 als je naar links gaat.
### Dan wordt het 200, 199, 198, ... Dan denkt die dat die op de vorige rij is door 1xx. Denk dat we het zo veel makkelijker maken voor onszelf.
# @autor "Peter Markotic, Floor Eigenhuis"

import random
import numpy as np
import math
import matplotlib.pyplot as plt

width = 10
height = 10
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
    if (x > width):
        x = x % width
    if (x < 1):
        x = width + (x % -width)

    if (y > height):
        y = y % height
    if (y < 1):
        y = height + (y % -height)
    return x,y

def radiusCheck(origin,r):
    temp = []
    for x in range(origin[0] - r, origin[0] + r+1):
        for y in range(origin[1] - r, origin[1] + r+1):
            if (math.pow ((x - origin[0]) , 2) + math.pow ((y - origin[1]), 2) <= r ** 2):
                temp.append([x,y])
    return temp


def move(player, A, playerLocations, width, height, epsilon, radius = 1, speed = 3):
    currentLoc = playerLocations[player]

    if random.random() <= epsilon or (np.count_nonzero(payoffs[player-1]) == 0):
        angle = random.choice(A) # explore
    else:
        angle = A[payoffs[player - 1].index(max(payoffs[player - 1]))] # exploit: get the index of the move that caused the max payoff and play that action

    angle_rad = math.radians(angle) # convert to radians, take cos for y and sin for x value
    #x = math.cos(angle_rad) * speed #zonder afronden
    #y = (math.sin(angle_rad) * -1) * speed

    x = round(math.cos(angle_rad) * speed) #met afronden
    y = round((math.sin(angle_rad) * -1) * speed)

    x += currentLoc[0]
    y += currentLoc[1]

    x,y = mapToInBounds(x,y)

    newLoc = [x,y]  #@TODO: Kijken of we moeten afronden en dus met patches moeten werken, of niet?

    plays[player - 1][A.index(angle)] += 1  # add move of player to the array

    # if(newLoc in playerLocations.values()):
    #     payoffs[player - 1][A.index(angle)] += -50
    #     return


    for loc in playerLocations.values():
        coords = radiusCheck(loc, radius)
        for i in range(len(coords)):
            coords[i][0], coords[i][1] = mapToInBounds(coords[i][0], coords[i][1])
        if newLoc in coords:
            payoffs[player -1][A.index(angle)] += -5
            #print('Collision; didnt move')
            return

    #x,y = mapToInBounds(x,y)
    #newLoc = [x,y]

#    print(player)
#    print('current location: ')
#    print(currentLoc)
#    print ('move: ')
#    print(angle)
#    print('new location: ')
#    print(newLoc)

    payoffs[player - 1][A.index(angle)] += 1
    playerLocations[player] = newLoc
    return


field = getLocations(width, height)
playerLocations = getStartLoc(field, players)
A = [0, 45, 90, 135, 180, 225, 270, 315]
payoffs = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total payoff for player for a particular move
plays = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total times player has played a move
epsilon = 0.1
#delta = 1
average_payoffs = [[[] for x in range(players)] for y in range(players)] #2d array, but now for every timestep
test = [[] for x in range(players)]

print("field: ")
print(field)
print("Playerloc: ")
print(playerLocations)
print("Payoffs: ")
print(payoffs)
print('test')
print(test)

i = 0
while i < 100000:
    if(i % 1000 == 0):
        #delta+=1
        print(i)
        print(payoffs)
    for player in playerLocations:
        move(player, A, playerLocations, height, width, epsilon)

    for n in range(players): #for each angle
        average = 0
        for m in range(players): #for each player
            average += payoffs[m][n]      # add [player][move] payoff to average
        average = round(average/players)
        test[n].append(average)
    #     for m in range(players):
    #         total_plays = plays[n][m]
    #         if total_plays is not 0:
    #             #average_payoffs[n][m].append(payoffs[n][m]/plays[n][m])
    #             # print(average_payoffs[xx][yy])
    #         else:
    #             #average_payoffs[n][m].append(payoffs[n][m])
    #             # print(average_payoffs[xx][yy])
    i += 1

print("\n")
print("Playerloc: ")
print(playerLocations)
print("Payoffs: ")
print(payoffs)
print("Plays: ")
print(plays)


labels = []
# for i in range(players):
#     plt.plot(average_payoffs[i][0])
#     labels.append('Skater: ' + str(i+1))

for i in range(players):
    plt.plot(test[i])
    labels.append('Angle: ' + str(A[i]) + '°')

plt.ylabel('Average payoff over all players at time t')
plt.legend(labels, ncol=players,  loc=3, bbox_to_anchor=(0., 1.02, 1., .102), mode="expand", borderaxespad=0.)
plt.show()

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
