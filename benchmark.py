import time
from AI_Algorithms.astar import AStarSearch

grid = [[0]*100 for _ in range(100)]
start = (0, 0)
goal = (99, 99)

def is_walkable(pos):
    return True

astar = AStarSearch()
t0 = time.time()
path, stats = astar.find_path(grid, start, goal, is_walkable)
t1 = time.time()

print(f"Time: {t1-t0}s")
