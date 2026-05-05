import numpy as np

# Grid dimensions
R, C = 6, 6
N = R * C

# Labeled cells: (row, col) -> score
CLUES = {
    (0, 1): 21, (1, 0): 21, (1, 2): 27, (1, 3): 15, (1, 4): 25, (1, 5): 9,
    (2, 0): 25, (2, 2): 27, (2, 3): 45, (2, 5): 9,
    (3, 0): 9,  (3, 2): 63, (3, 4): 45,
    (4, 0): 63, (4, 2): 9,  (4, 5): 288,
    (5, 4): 35
}

# Forbidden cells for arcs (green cells)
GREEN_CELLS = {
    (0, 0), (0, 2), (0, 4),
    (1, 0), (1, 2), (1, 4), (1, 5),
    (2, 0), (2, 2), (2, 3), (2, 5),
    (4, 0), (4, 1), (4, 5),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 5)
}

def get_adjacency_list():
    """Generates the 4-connected grid adjacency list."""
    adj = [[] for _ in range(N)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(R):
        for c in range(C):
            idx = r * C + c
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    adj[idx].append(nr * C + nc)
    return adj

def compute_region_stats(sol_masks, adj):
    """
    Computes area, perimeter, and scores for each region mask.
    Score = perimeter * area.
    """
    areas = []
    perims = []
    scores = []
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
        scores.append(per * area)
    return areas, perims, scores

def build_filled_grid(sol_masks, scores):
    """Fills grid with dominant region scores."""
    filled = np.zeros((R, C), dtype=int)
    for idx in range(N):
        r, c = divmod(idx, C)
        for rid, m in enumerate(sol_masks):
            if (m >> idx) & 1:
                filled[r, c] = scores[rid]
                break
    return filled

def verify_and_solve(sol_masks):
    """
    Verifies clue consistency, fills the grid, and computes 
    the final sum of squares for row and column sums.
    """
    adj = get_adjacency_list()
    areas, perims, scores = compute_region_stats(sol_masks, adj)
    filled = build_filled_grid(sol_masks, scores)
    
    # Verify clue consistency
    for (r, c), val in CLUES.items():
        assert filled[r, c] == val, f"Clue mismatch at ({r},{c}): got {filled[r, c]}, expected {val}"
        
    row_sums = filled.sum(axis=1)
    col_sums = filled.sum(axis=0)
    answer = sum(x**2 for x in row_sums) + sum(x**2 for x in col_sums)
    
    return filled, row_sums, col_sums, answer

if __name__ == "__main__":
    # To run the script, define the winning region bitmasks found by your solver.
    # Each integer is a 36-bit mask representing a region's cell membership.
    # sol_masks = [ ... ]
    
    print("Jane Street May 2026 solver functions defined successfully.")
    print("Call verify_and_solve(sol_masks) with your solution bitmasks.")

