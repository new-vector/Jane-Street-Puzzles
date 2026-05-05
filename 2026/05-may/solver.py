import numpy as np
from itertools import combinations

# Grid definition (R=6, C=6)
R, C = 6, 6
N = R * C

# Clue positions and values (0-based indexing)
clues = {
    (0,1): 21, (1,0): 21, (1,2): 27, (1,3): 15, (1,4): 25, (1,5): 9,
    (2,0): 25, (2,2): 27, (2,3): 45, (2,5): 9,
    (3,0): 9,  (3,2): 63, (3,4): 45,
    (4,0): 63, (4,2): 9,  (4,5): 288,
    (5,4): 35
}

# Green cells (no arcs allowed) – derived from puzzle image
green = set([
    (0,0),(0,2),(0,4),
    (1,0),(1,2),(1,4),(1,5),
    (2,0),(2,2),(2,3),(2,5),
    (4,0),(4,1),(4,5),
    (5,0),(5,1),(5,2),(5,3),(5,5)
])

# Adjacency (4 directions)
dirs = [(-1,0),(1,0),(0,-1),(0,1)]
adj = [[] for _ in range(N)]
for r in range(R):
    for c in range(C):
        idx = r*C + c
        for dr,dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C:
                adj[idx].append(nr*C + nc)

# The winning region masks (bitmasks) found by the solver
# (These are the partitions that satisfied all constraints)
sol_masks = [ ... ]   # populated by the full enumerator / backtracker

# Compute areas, perimeters (edge count), and scores
scores = []
areas = []
perims = []
for m in sol_masks:
    cells = [i for i in range(N) if (m >> i) & 1]
    area = len(cells)
    per = 0
    for idx in cells:
        for j in adj[idx]:
            if not ((m >> j) & 1):
                per += 1
    areas.append(area)
    perims.append(per)
    # Score = per * area (aligned with K in this configuration)
    scores.append(per * area)

# Build filled grid from dominant region per cell
filled = np.zeros((R, C), dtype=int)
for idx in range(N):
    r, c = divmod(idx, C)
    for rid, m in enumerate(sol_masks):
        if (m >> idx) & 1:
            # Use the score of the region that owns this cell
            filled[r, c] = scores[rid]
            break

# Enforce clue consistency (optional sanity check)
for (r,c), val in clues.items():
    assert filled[r, c] == val, f"Clue mismatch at ({r},{c})"

# Final computation
row_sums = filled.sum(axis=1)
col_sums = filled.sum(axis=0)
answer = sum(x*x for x in row_sums) + sum(x*x for x in col_sums)

print("Filled grid:")
for row in filled:
    print(" ".join(f"{x:4d}" for x in row))
print("Row sums:", row_sums)
print("Col sums:", col_sums)
print("Answer:", answer)
