### 1 - Use the low quality Drunken Walk generator
 
### 2 - Generate many levels, assume one of them will be good
 
### 3 - Evaluate each level by number of steps it takes to solve them
 
### 4 - Use the Breadth First algorithm to get the number of steps for each level
 
### 5 - Sort levels on number of steps to retrieve the best level

import random

levelWidth = 55
levelHeight = 35

amountOfLevels = 100
removeBlocks = 500

### Easy Procedural Generation: Drunken Walk Algorithm

def getLevelRow():
    return ['#'] * levelWidth

def getWallLevel():
    return [getLevelRow() for _ in range(levelHeight)]

def drunkenWalkGenerator():
    drunk = {
        'removeBlocks': removeBlocks,
        'padding': 2,
        'x': int( levelWidth / 2 ),
        'y': int( levelHeight / 2 )
    }
    
    startCoordinate = [drunk['x'], drunk['y']]
    
    level = getWallLevel()
    
    x = -1
    y = -1
    
    while drunk['removeBlocks'] >= 0:
        x = drunk['x']
        y = drunk['y']
        
        if level[y][x] == '#':
            level[y][x] = '.'
            drunk['removeBlocks'] -= 1
        
        roll = random.randint(1, 4)
        
        if roll == 1 and x > drunk['padding']:
            drunk['x'] -= 1
        if roll == 2 and x < levelWidth - 1 - drunk['padding']:
            drunk['x'] += 1
        if roll == 3 and y > drunk['padding']:
            drunk['y'] -= 1
        if roll == 4 and y < levelHeight - 1 - drunk['padding']:
            drunk['y'] += 1
    
    endCoordinate = [x, y]
    
    return [level, startCoordinate, endCoordinate]

### Easy Pathfinding: Breadth-First Algorithm

def getNextMoves(x, y):
    return {
        'left':  [x-1, y], 
        'right': [x+1, y],
        'up':  [x, y-1],
        'down':  [x, y+1]
    }.values()

def getShortestPath(level, startCoordinate, endCoordinate):
    searchPaths = [[startCoordinate]]
    visitedCoordinates = [startCoordinate]
    
    while searchPaths != []:
        currentPath = searchPaths.pop(0)
        currentCoordinate = currentPath[-1]
        
        currentX, currentY = currentCoordinate
        
        if currentCoordinate == endCoordinate:
            return currentPath
        
        for nextCoordinate in getNextMoves(currentX, currentY):
            nextX, nextY = nextCoordinate
            
            if nextX < 0 or nextX >= levelWidth:
                continue
            
            if nextY < 0 or nextY >= levelHeight:
                continue
            
            if nextCoordinate in visitedCoordinates:
                continue
            
            if level[nextY][nextX] == '#':
                continue
            
            searchPaths.append(currentPath + [nextCoordinate])
            visitedCoordinates += [nextCoordinate]
    
    return []

### Improved Procedural Generation:
### Drunken Walk + Breadth First Algorithm

def generateLevels(amount):
    return [drunkenWalkGenerator() for _ in range(amount)]

def evaluateLevels(levels):
    evaluationScores = []
    
    for generatedLevel, startCoordinate, endCoordinate in levels:
        shortestSolution = getShortestPath(
            generatedLevel, 
            startCoordinate, 
            endCoordinate
        )
        
        evaluationScores.append(
            [len(shortestSolution), generatedLevel]
        )
    
    return evaluationScores

def generateBestLevel(amountOfLevels):
    levels = generateLevels(amountOfLevels)
    
    evaluationScores = evaluateLevels(levels)
    
    evaluationScores.sort()
    evaluationScores.reverse()
    
    score, bestLevel = evaluationScores.pop(0)
    
    return bestLevel

bestLevel = generateBestLevel(amountOfLevels)

for row in bestLevel:
    print( ''.join(row) )
