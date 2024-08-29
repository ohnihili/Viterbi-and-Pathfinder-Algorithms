import sys

from collections import deque
from math import sqrt

#function to read the txt map file
def mapReader(textFile):
    with open(textFile, 'r') as textFile:
        rows, cols = textFile.readline().split()
        rows = int(rows)
        cols = int(cols)
        startx, starty = textFile.readline().split()
        start= (int(startx)-1, int(starty)-1)
        goalx, goaly = textFile.readline().split()
        goal= (int(goalx)-1, int(goaly)-1)
        map = []
        for line in textFile:
            row = []
            for element in line.split():
                    row.append(element)
            map.append(row)
    return rows, cols, start, goal, map
    
#bfs search function
def bfs(start, goal, map, rows, cols):
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    queue = deque([(start, [])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == goal:
            map[goal[0]][goal[1]]= '*'
            for cell in path:
                map[cell[0]][cell[1]] = '*'
            return 1
        
        for each_move in directions:
            next_cell = (current[0] + each_move[0], current[1] + each_move[1])
            r, c = next_cell
            exists = 0 <= r < rows and 0 <= c < cols and map[r][c] != 'X'
            if next_cell in visited or not exists:
                continue
            visited.add(next_cell)
            queue.append((next_cell, path + [current]))

    return None

def ucs(start, goal, map, rows, cols):
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cost = 0
    elevation = int(map[start[0]][start[1]])
    queue = [(start, [], cost, elevation)]
    visited = set()
    while queue:
        current, path, cost, elevation = queue[0]
        queue.pop(0)
        visited.add(current)
        if current == goal:
            map[goal[0]][goal[1]]= '*'
            for cell in path:
                map[cell[0]][cell[1]] = '*'
            return 1
        
        for each_move in movements:
            next_cell = (current[0] + each_move[0], current[1] + each_move[1])
            r, c = next_cell
            exists = 0 <= r < rows and 0 <= c < cols and map[r][c] != 'X'
            if next_cell in visited or not exists:
                continue

            new_elevation = int(map[next_cell[0]][next_cell[1]])
            new_cost=cost
            if new_elevation - elevation > 0:
                new_cost += new_elevation - elevation
            new_cost += 1 
            queue.append((next_cell, path + [current], new_cost, new_elevation))
            queue.sort(key= lambda queue:queue[2])
    return None
    
def euclidean_distance(current, goal):
    return sqrt((goal[0] - current[0]) ** 2 + (goal[1] - current[1]) ** 2)

def manhattan_distance(current, goal):
    return abs(goal[0] - current[0]) + abs(goal[1] - current[1])

def astar(start, goal, map, rows, cols, heuristic):
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cost = 0
    if heuristic == 'euclidean':
        estimate = euclidean_distance(start, goal) 
    else:
        estimate = manhattan_distance(start, goal)
    elevation = int(map[start[0]][start[1]])

    queue = [(start, [], cost, elevation, estimate)]
    visited = set()
    while queue:
        current, path, cost, elevation, estimate = queue[0]
        visited.add(current)
        queue.pop(0)

        if current == goal:
            map[goal[0]][goal[1]]= '*'
            for cell in path:
                map[cell[0]][cell[1]] = '*'
            return 1
        
        for each_move in movements:
            next_cell = (current[0] + each_move[0], current[1] + each_move[1])
            r, c = next_cell
            exists = 0 <= r < rows and 0 <= c < cols and map[r][c] != 'X'
            if next_cell in visited or not exists:
                continue

            new_elevation = int(map[next_cell[0]][next_cell[1]])
            new_cost=cost
            if new_elevation - elevation > 0:
                new_cost += new_elevation - elevation
            new_cost += 1 

            if heuristic == 'euclidean':
                new_estimate = new_cost + euclidean_distance(next_cell, goal)
            else:
                new_estimate = new_cost + manhattan_distance(next_cell, goal)
            queue.append((next_cell, path + [current], new_cost, new_elevation, new_estimate))
            queue.sort(key= lambda x:x[4])
    return None 

#main function
mapGrid = sys.argv[1]
alg = sys.argv[2]

if len(sys.argv) == 4:
    heuristic = sys.argv[3]

rows, cols, start, goal, map = mapReader(mapGrid)

if alg == "bfs":
    path = bfs(start, goal, map, rows, cols)
    if path:
        for i in range(len(map)):
            for j in range(len(map[0])):
                print(map[i][j], end=" ")
            print()
    else:
        print("null")
elif alg == "ucs":
    path = ucs(start, goal, map, rows, cols)
    if path:
        for i in range(len(map)):
            for j in range(len(map[0])):
                print(map[i][j], end=" ")
            print()
    else:
        print("null")
elif alg == "astar":
    path = astar(start, goal, map, rows, cols, heuristic)
    if path:
        for i in range(len(map)):
            for j in range(len(map[0])):
                print(map[i][j], end=" ")
            print()
    else:
        print("null")
else:
    print("null")