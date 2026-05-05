# Jane Street Puzzle: Arch Madness (May 2026)

[Official Puzzle Page](https://www.janestreet.com/puzzles/arch-madness-index/)

## Problem Description

A 6x6 grid contains white and green cells. 90-degree arcs (radius 1) can be placed in some white cells. The arcs partition the grid into regions with integer areas.
For each region, its score is defined as:
$$\text{Score} = K \times A$$
where $K$ is the number of smooth (continuously differentiable) perimeter pieces and $A$ is the region's area.

Cells labeled with a number indicate the score of the region containing at least half of that cell. Once the grid is complete, un-numbered cells are filled with the score of their dominant region.
The goal is to compute:
$$\sum R_i^2 + \sum C_j^2$$
where $R_i$ and $C_j$ are the row and column sums of the completed score grid.

## Core Strategy

### 1. Area Integration Constraint
Each 90° arc splits a cell into a large lobe ($L = 1 - \frac{\pi}{4}$) and a small lobe ($S = \frac{\pi}{4}$). For a region to have an integer area:
$$A = n + k \cdot L + m \cdot S \in \mathbb{Z}$$
which requires $k = m$ (the number of large and small lobes inside any valid region must be balanced).

### 2. Constraint Solving
* **Green cells**: Fixed mask of 18 cells where arcs are forbidden.
* **No dangling arcs**: The two lobes of any arc-containing cell must belong to distinct regions.
* **Clue consistency**: Labeled cell values must match the score of the region owning at least 50% of the cell.

## Final Answer

Row sums and column sums whose squares sum to:
**9,719,868**

*Script: [`solver.py`](./solver.py)*
