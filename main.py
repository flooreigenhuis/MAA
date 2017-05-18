#TODO: now only checks if the new location of the player is the location, but need to check if it is in a radius around another player -->
#TODO: make move function better and more readable (and the rest as well)
#some way to track how many times the players played a particular move -> now stored in a 2 dim array and make some nice graphs out of it; Done

import random
import numpy as np
import matplotlib.pyplot as plt


# get a list of the possible locations
def getLocations (width, height):
    loc = []
    for h in range (1, height+1):
        for w in range (1, width +1):
            loc.append((h*100) + w)
    return loc

# get the starting locations of the players
def getStartLoc(loc, players):
    playerLoc = {}
    for p in range (1, players+1):
        playerLoc[p] = random.choice(loc)
        loc.remove(playerLoc[p]) #so players don't get the same location
    return playerLoc

# move function
def move(player, A, playerLoc, height, width, epsilon,  radius = 2):
    currentLoc = playerLoc[player]
   
    #explore if random number is smaller/equal to epsilon or if the payoffs for the player are all 0 (so it's the first iteration)
    if random.random() <= epsilon or (np.count_nonzero(payoffs[player-1]) == 0): 
        move = random.choice(A)
        # print('EXPLORE')
    else:
        move = A[payoffs[player-1].index(max(payoffs[player-1]))] #get the index of the move that caused the max payoff and play that action
        # print('EXPLOIT')
    if move == 0: #straight up 
        if currentLoc < 201: #if you're at the top of the field, move up means appear at the bottom
            newLoc = currentLoc + ((height-1)*100)
        else:
            newLoc = currentLoc - 100
    elif move == 45: #right diagonal up 
        if currentLoc < 201: #check if on top of field
            if currentLoc%100 == width:  # right of field
                newLoc = currentLoc + ((height-1)*100) - width + 1 #appear at the bottom and at the left of field
            else:
                newLoc = currentLoc + ((height-1)*100) + 1
        elif currentLoc%100 == width:
            newLoc = currentLoc - 100 - width + 1
        else:
            newLoc = currentLoc - 100 + 1
    elif move == 90: #straight right
        if currentLoc%100 == width: # right of field
            newLoc = currentLoc - width + 1
        else:
            newLoc = currentLoc + 1
    elif move == 135: #right diagonal down
        if currentLoc > (height*100): #check if on bottom of field
            if currentLoc%100 == width: #check if on right of field
                newLoc = currentLoc - (height*100) + 100 - width + 1
            else: 
                newLoc = currentLoc - (height*100) + 100 + 1
        elif currentLoc%100 == width:
            newLoc = currentLoc + 100 - width + 1
        else: 
            newLoc = currentLoc + 100 + 1
    elif move == 180: #straight down
        if currentLoc > (height*100): #check if on bottom of field
            newLoc = currentLoc - (height*100) + 100 
        else: 
            newLoc = currentLoc + 100
    elif move == 225: #left diagonal down
        if currentLoc > (height*100): #check if on bottom of field
            if currentLoc%100 == 1: #check if on left of field
                newLoc = currentLoc - (height*100) + 100 - 1 + width
            else:
                newLoc = currentLoc - (height*100) + 100 - 1
        elif currentLoc%100 == 1:
            newLoc = currentLoc + 100 - 1 + width
        else:
            newLoc = currentLoc + 100 - 1
    elif move == 270: #straight left 
        if currentLoc%100 == 1: #check if on left of field
            newLoc = currentLoc - 1 + width
        else:
            newLoc = currentLoc - 1
    elif move == 315: #left diagonal up 
        if currentLoc < 201:
            if currentLoc%100 == 1: #check if on left of field
                newLoc = currentLoc + ((height-1)*100) - 1 + width #appear at bottom right
            else: 
                newLoc = currentLoc + ((height-1)*100) - 1
        elif currentLoc%100 == 1: #check if on left of field
            newLoc = currentLoc - 100 - 1 + width
        else: 
            newLoc = currentLoc - 100 -1
            
    # print( 'player: ' + str(player) + " " + 'current location: ' +  str(currentLoc) + " " + 'move: ' +  str(move) + " " + 'new location: ' +  str(newLoc) + "\n")
    plays[player-1][A.index(move)] += 1 #add move of player to the array
    flag = False
    for loc in playerLoc.values():
        temp = [loc]
        for r in range(radius):
            temp.append(loc+1*(r+1))
            temp.append(loc-1*(r+1))
            temp.append(loc-100*(r+1))
            temp.append(loc+100*(r+1))
            temp.append(loc+1*(r+1)+100*(r+1))
            temp.append(loc+1*(r+1)-100*(r+1))
            temp.append(loc-1*(r+1)+100*(r+1))
            temp.append(loc-1*(r+1)+100*(r+1))
        print(temp)
        if newLoc in temp:
            payoffs[player - 1][A.index(move)] += -1
            return
    payoffs[player-1][A.index(move)] += 2
    playerLoc[player] = newLoc
    return

width = 5
height = 5
players = 8
loc = getLocations(width, height)
playerLoc = getStartLoc(loc, players)
A = [0, 45, 90, 135, 180, 225, 270, 315]
payoffs = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total payoff for player for a particular move
plays = [[0 for x in range(players)] for y in range(players)] #2 dimensional array; [player][move] = total times player has played a move
epsilon = 0.1

average_payoffs = [[[] for x in range(players)] for y in range(players)] #2d array [move][player]


print("loc: ")
print(loc)
print("Playerloc: ")
print(playerLoc)
print("Payoffs: ")
print(payoffs)
print('test')
print(average_payoffs)
i = 0
while i < 10000:
    for player in playerLoc:
        move(player, A, playerLoc, height, width, epsilon)
    for xx in range(players):
        for yy in range(players):
            total_plays = plays[xx][yy]
            if total_plays is not 0:
                average_payoffs[xx][yy].append(payoffs[xx][yy]/plays[xx][yy])
            else:
                average_payoffs[xx][yy].append(payoffs[xx][yy])
    i+= 1


print("\n")
print("Playerloc: ")
print(playerLoc)
print("Payoffs: ")
print(payoffs)
print("Plays: ")
print(plays)
print("Average_payoffs ")
#print(average_payoffs)

labels = []
for zz in range(players):
    plt.plot(average_payoffs[zz][0])
    labels.append('Skater: ' + str(zz+1))

plt.ylabel('reward')
plt.legend(labels, ncol=players,  loc=3, bbox_to_anchor=(0., 1.02, 1., .102), mode="expand", borderaxespad=0.)
#plt.show()