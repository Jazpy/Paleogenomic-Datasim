from itertools import combinations
from numpy import percentile
from statistics import median

# Aux functions
def _file_similarity(filename0, filename1):
        shared = 0
        f0_total = 0
        f1_total = 0
        with open(filename0, 'r') as f0, open(filename1, 'r') as f1:
            l0 = f0.readline()
            l1 = f1.readline()
            f0_total += 1
            f1_total += 1

            while l0 and l1:
                s0 = int(l0.split()[2])
                s1 = int(l1.split()[2])

                if s0 == s1:
                    shared += 1
                    l0 = f0.readline()
                    l1 = f1.readline()
                    f0_total += 1
                    f1_total += 1
                elif s0 < s1:
                    l0 = f0.readline()
                    f0_total += 1
                elif s0 > s1:
                    l1 = f1.readline()
                    f1_total += 1

        if f0_total == 0 and f1_total == 0:
            return 0.0

        return shared / float(max(f0_total, f1_total)) * 100.0

# Graph classes
class FileGraph:

    def __init__(self, filenames):
        self.cases = len(filenames)
        self.matrix = AdjMatrix(self.cases)
        
        # Build graph by calculating similarities between all files
        weight_list = []
        for f0, f1 in combinations(filenames, 2):
            weight = _file_similarity(f0, f1)
            f0_id = int(f0.split('/')[-1].split('.')[0].split('_')[-1]) - 1
            f1_id = int(f1.split('/')[-1].split('.')[0].split('_')[-1]) - 1

            weight_list.append(weight)
            self.matrix.add_edge(f0_id, f1_id, weight)

        prune_threshold = percentile(weight_list, 75)
        self.matrix.prune_weight(prune_threshold)

    def k_cliques(self, k, top):
        # First, build 2-cliques (i. e. all edges)
        cliques = [{x, y} for x, y in self.matrix.get_edges()]
        curr_k = 2

        while cliques and curr_k < k:
            k_1_cliques = set()

            for x, y in combinations(cliques, 2):
                sym_diff = x ^ y
                if len(sym_diff) == 2 and self.matrix.is_neighbor(*sym_diff):
                    k_1_cliques.add(tuple(x | sym_diff))

            cliques = list(map(set, k_1_cliques))
            curr_k += 1

        # Should switch to quickselect instead of sorting
        cliques = sorted(cliques, key=self.matrix.clique_min_weight, reverse=True)

        if len(cliques) < top:
            return cliques

        return cliques[0:top]

    def print(self):
        self.matrix.print()

class AdjMatrix:

    def __init__(self, n):
        self.matrix = [[0.0 for x in range(n)] for y in range(n)]
        self.size = n

    def add_edge(self, n1, n2, w):
        self.matrix[n1][n2] = self.matrix[n2][n1] = w

    def get_edge(self, n1, n2):
        return self.matrix[n1][n2]

    def is_neighbor(self, n1, n2):
        return self.matrix[n1][n2] > 0.0

    def print(self):
        for row in self.matrix:
            print(*row, sep='\t')

    def prune_weight(self, weight):
        # All possible edge nodes
        for x, y in combinations(range(self.size), 2):

            # Remove all edges below threshold
            if self.matrix[x][y] < weight:
                self.matrix[x][y] = self.matrix[y][x] = 0.0

    # Return smallest weight in a clique
    def clique_min_weight(self, clique):
        min_cell = 100.0

        for x, y in combinations(clique, 2):

            curr_cell = self.matrix[x][y]
            if curr_cell < min_cell:
                min_cell = curr_cell

        return min_cell

    # Generator for all neighbors of a given node
    def get_neighbors(self, n):

        for i in range(self.size):
            cell = self.matrix[n][i]

            if cell > 0:
                yield i

    # Generator for all edges
    def get_edges(self):
        # All possible edge nodes
        for x, y in combinations(range(self.size), 2):

            # Yield only connected nodes
            if self.matrix[x][y] > 0.0:
                yield x, y
