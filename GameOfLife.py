import os
from pprint import pprint
import copy
import time
import random

### World is indexed like this:
###  012 x
### 0...
### 1...
### 2...
### y

### Cell value meaning
### The constant var LIVE sets a cell to alive
### The constant var DEAD sets a cell to dead

def clearConOutput():
    os.system( 'cls' )

def seedTheWorld(w):
    for y in range(len(w)):
        for x in range(len(w[y])):
            w[y][x] = random.choice([DEAD, LIVE])

    return w

def setUpWorld():
    # return [[1 , 2 , 3 , 4 , 5],
    #         [6 , 7 , 8 , 9 , 10],
    #         [11, 12, 13, 14, 15],
    #         [16, 17, 18, 19, 20],
    #         [21, 22, 23, 24, 25]]

    ## Tests the 2 neighbor, cell must live
    # return [[LIVE, DEAD, DEAD, DEAD, DEAD],
    #         [LIVE, LIVE, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD]]

    ## Tests the 3 neighbor, cell must live
    # return [[LIVE, DEAD, DEAD, DEAD, DEAD],
    #         [LIVE, LIVE, DEAD, DEAD, DEAD],
    #         [LIVE, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD]]

    ## Tests the 1 neighbor, cell must die
    # return [[LIVE, DEAD, DEAD, DEAD, DEAD],
    #         [LIVE, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD]]

    # # Tests the 4 neighbor, cell must die
    # return [[DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, LIVE, DEAD],
    #         [DEAD, DEAD, LIVE, LIVE, LIVE],
    #         [DEAD, DEAD, DEAD, LIVE, DEAD]]

    ## Tests the 4+ neighbor, cell must die
    # return [[LIVE, LIVE, DEAD, DEAD, DEAD],
    #         [LIVE, LIVE, DEAD, DEAD, DEAD],
    #         [LIVE, LIVE, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD],
    #         [DEAD, DEAD, DEAD, DEAD, DEAD]]

    w = [[None for x in range(X_LEN)] for y in range(Y_LEN)]
    w = seedTheWorld(w)
    return w

## make sure y and x isn't out of bound. If any of the y or x is out of bound, return None.
## the y and x are assumed to be zero indexed
def safeGetCellFromWorld(y, x, world):
    # if y >= Y_LEN:
    #     y = Y_LEN - 1
    # elif y < 0:
    #     y = 0

    # if x >= X_LEN:
    #     x = X_LEN - 1
    # elif x < 0:
    #     x = 0

    if y >= Y_LEN or y < 0 or x >= X_LEN or x < 0:
        return None

    return world[y][x]

def getNeighbor(y, x, world):
    neibr = []

    ## top left
    neibr_y = y-1
    neibr_x = x-1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))
    ## top
    neibr_y = y-1
    neibr_x = x
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))
    ## top right
    neibr_y = y-1
    neibr_x = x+1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))


    ## left
    neibr_y = y
    neibr_x = x-1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))
    ## right
    neibr_y = y
    neibr_x = x+1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))


    ## bottom left
    neibr_y = y+1
    neibr_x = x-1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))
    ## bottom
    neibr_y = y+1
    neibr_x = x
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))
    ## bottom right
    neibr_y = y+1
    neibr_x = x+1
    neibr.append(safeGetCellFromWorld(neibr_y, neibr_x, world))


    return neibr

def liveOrDie(world):
    w = copy.deepcopy(world)

    for y in range(len(w)):
        for x in range(len(w[y])):
            cell = world[y][x]
            neibr = getNeighbor(y, x, world)
            live_count = neibr.count(LIVE)
            # print(f"{world[y][x]}:\t{neibr}\t {live_count}" )
            if cell == LIVE and (live_count == 2 or live_count == 3):
                ## Cell is alive and will survive
                pass
            elif cell == DEAD and live_count == 3:
                ## Cell is revived due to reproduction by neighboring cells
                w[y][x] = LIVE
            else:
                ## Cell dies due to overpopulation: live_count > 3
                ## Cell dies due to underpopulation: live_count < 2
                w[y][x] = DEAD

    return w

def chkGameOver(w):
    game_over = True

    for y in range(len(w)):
        for x in range(len(w[y])):
            if w[y][x] == LIVE:
                game_over = False

    return game_over

def chkGameStalemate(w, old_w):
    stale_mate = True

    for y in range(len(w)):
        for x in range(len(w[y])):
            if w[y][x] != old_w[y][x]:
                stale_mate = False

    return stale_mate

def main():
    world = setUpWorld()
    last_world = None
    initial_world = copy.deepcopy(world)
    i = 1

    ## Game cycle
    # for i in range(1):
    while(True):
        print(i)
        pprint(world)

        if last_world is not None: ## In the first iteration, don't check for stalemate
            if chkGameStalemate(world, last_world):
                print('You have achieved world peace!')
                print('It was with this configuration:')
                pprint(initial_world)
                break
        if chkGameOver(world):
            print('Your race has died out!')
            print('It was with this configuration:')
            pprint(initial_world)
            break

        last_world = copy.deepcopy(world)
        world = liveOrDie(world)

        time.sleep(1)
        clearConOutput()
        i+=1
    # pprint(f_world)
    # print()
    # pprint(world)


if __name__ == '__main__':
    X_LEN = 5
    Y_LEN = 5

    LIVE = 1
    DEAD = 0

    main()