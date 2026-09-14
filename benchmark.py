import time
from AI_Algorithms.astar import AStarSearch
from AI_Algorithms.bfs import BreadthFirstSearch

grid = [[0]*50 for _ in range(50)]
start = (0, 0)
goal = (49, 49)

def is_walkable(pos):
    return True

astar = AStarSearch()
t0 = time.time()
for _ in range(10):
    astar.find_path(grid, start, goal, is_walkable)
t1 = time.time()
print("AStar find_path took:", t1 - t0)

bfs = BreadthFirstSearch()
t0 = time.time()
for _ in range(10):
    bfs.find_path(grid, start, goal, is_walkable)
t1 = time.time()
print("BFS find_path took:", t1 - t0)
