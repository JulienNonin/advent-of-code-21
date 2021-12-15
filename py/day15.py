# %%
import bisect
import matplotlib.pyplot as plt
import numpy as np

# %%
class ArrayExpanded():
    def __init__(self, arr, N, M):
        assert arr.ndim == 2, "Must be a 2d array"
        self.arr = np.copy(arr)
        self.n, self.m = self.arr.shape
        self.N, self.M = N, M

    @property
    def shape(self):
        return self.n * self.N, self.m * self.M

    def _check_index(self, index):
        assert isinstance(index, tuple) and len(index) == 2, "two indeces are required"
        i, j = index
        assert type(i) == int and type(j) == int, "only integers are valid indeces"
        if not (0 <= i < self.shape[0]):
            raise IndexError(f"index {i} is out of bounds for axis 0 with size {self.shape[0]}")
        if not (0 <= j < self.shape[1]):
            raise IndexError(f"index {j} is out of bounds for axis 1 with size {self.shape[1]}")
        return index

    def __getitem__(self, index):
        i, j = self._check_index(index)
        i, j = index
        δi, δj = i // self.n, j // self.m
        ii, jj = i % self.n, j % self.m
        value = self.arr[ii, jj] + δi + δj
        return (value - 1) % 9 + 1

# %%
def expand(A, N, M):
    n, m = A.shape
    B = np.tile(A, (N, M))
    for i in range(n * N):
        for j in range(m * M):
            δi, δj = i // n, j // m
            B[i,j] = B[i,j] + δi + δj
            B[i,j] = (B[i,j] - 1) % 9 + 1
    return B

def expand_no_memory(A, N, M):
    return ArrayExpanded(A, N, M)

def neighbors(i, j, n, m):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < n - 1:
        yield i + 1, j
    if j < m - 1:
        yield i, j + 1

# %%
def lowest_risk_path(risk):
    n, m = risk.shape
    NOT_VISITED = -1
    cost = np.zeros(risk.shape) + NOT_VISITED
    cost[0, 0] = 0
    queue = [(0, 0, 0)]
    predecessor = {}

    while queue:
        current_cost, x, y = queue.pop(0)
        # if x == n - 1 and y == m - 1:
            # return current_cost
        for i, j in neighbors(x, y, n, m):
            if cost[i, j] == NOT_VISITED:
            # if not (i, j) in predecessor:
                new_cost = risk[i, j] + current_cost
                cost[i, j] = new_cost
                bisect.insort(queue, (new_cost, i, j))
                predecessor[(i, j)] = (x, y)
    return cost, predecessor
#%%
def get_xy(prec, n, m):
    e = (n-1, m-1)
    x, y = [m-1], [n-1]
    while e in prec:
        e = prec[e]
        x.append(e[1])
        y.append(e[0])
    return x, y
# %%
# if __name__ == "__main__":
with open("../data/day15.txt", "r") as f:
    chitons_map = np.array([list(map(int, list(line))) for line in f.read().splitlines()])
# chitons_map = np.array([[4, 1, 20, 1, 1, 1], [5, 1, 20, 1, 20, 1], [5, 1, 20, 1, 20, 1], [5, 1, 1, 1, 20, 1]])

part1, pred1 = lowest_risk_path(chitons_map)
xx = expand_no_memory(chitons_map, 5, 5)
part2, pred2 = lowest_risk_path(xx)


plt.figure(figsize=(16, 8))
plt.subplot(121)
plt.imshow(np.where(part1 == -1, np.nan, part1), cmap="inferno")
plt.plot(*get_xy(pred1, *chitons_map.shape), '-', c="white")
plt.axis("off")

plt.subplot(122)
plt.imshow(np.where(part2 == -1, np.nan, part2), cmap="inferno")
plt.plot(*get_xy(pred2, *xx.shape), '-', c="white")
plt.axis("off")
plt.tight_layout()

plt.savefig("../img/day15.svg"),  #bbox_inches='tight')
plt.show()


# print("Part 1 —", part1)
# print("Part 2 —", part2)

# %%
