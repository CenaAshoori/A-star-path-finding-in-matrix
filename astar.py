from display import Display


class Node:
    parent: "Node"
    row: int
    col: int
    g: int
    h: float
    f: float

    def __init__(
            self,
            parent: "Node", row: int, col: int, row_goal: int, col_goal: int, g: int, alpha: float):
        self.parent = parent
        self.row = row
        self.col = col
        self.g = g
        self.h = ((abs(row_goal - row) ** 2) + abs(col_goal - col) ** 2) ** .5

        # Alpha is the diffrence between Greedy and A*
        self.f = (2 - alpha) * self.g + alpha * (self.h)
        # self.f = self.g + self.h


class Astar:
    queue: list["Node"] = []
    matrix: list[list[int]]
    map_height: int
    map_width: int
    children_counter = 0
    all_visited: set["Node"] = set()
    answer_node: "Node"
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, matrix, alpha, conected=True, eight_direction=False, is_idastar=False, iterate=2):
        if eight_direction:
            self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        self.matrix = matrix
        # find start point
        self.row_start, self.col_start = self.find_node(2)
        # find end point
        self.row_goal, self.col_goal = self.find_node(3)
        self.alpha = alpha
        self.map_height = len(matrix)
        self.map_width = len(matrix[0])
        self.is_found = False
        self.is_connected = conected
        self.start_node = Node(None, self.row_start, self.col_start, self.row_goal, self.col_goal, 0, self.alpha)
        self.queue.append(self.start_node)

        # ida star addon
        self.is_idastar = is_idastar
        self.found_idastar = False
        self.iterate = iterate
        self.max_f = 1

    def find_node(self, num):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                if self.matrix[row][col] == num:
                    return row, col

    def find_best_node(self) -> "Node":
        j = 0
        for i in range(len(self.queue)):
            if self.queue[i].f <= self.queue[j].f:
                j = i
        return self.queue.pop(j)

    def create_children(self, node: "Node"):
        self.all_visited.add((node.row, node.col))
        for dirs in self.directions:
            row_new = node.row + dirs[0]
            col_new = node.col + dirs[1]
            if self.is_connected:
                row_new = (node.row + dirs[0]) % self.map_height
                col_new = (node.col + dirs[1]) % self.map_width
            if 0 <= row_new < self.map_height and 0 <= col_new < self.map_width and (
                    row_new, col_new) not in self.all_visited:
                if self.matrix[row_new][col_new] != 1:
                    node_new = Node(node, row_new, col_new, self.row_goal, self.col_goal, node.g + 1, self.alpha)
                    if self.is_idastar:
                        if node_new.f <= self.max_f:
                            self.children_counter += 1
                            self.queue.append(node_new)
                            self.all_visited.add((row_new, col_new))
                        else:
                            self.found_idastar = True
                    else:
                        self.children_counter += 1
                        self.queue.append(node_new)
                        self.all_visited.add((row_new, col_new))

    def path(self) -> list[(int, int)]:
        ans = []
        node = self.answer_node
        while node != None:
            ans.append((node.row, node.col))
            node = node.parent
        return ans

    def print_path(self):
        set_path = set()
        node = self.answer_node
        while node != None:
            set_path.add((node.row, node.col))
            node = node.parent
        for row in range(self.map_height):
            for col in range(self.map_width):
                if (row, col) in set_path:
                    print(1, end=" ")
                else:
                    print(0, end=" ")

    def run(self):

        if len(self.queue):
            # while len(self.queue)>=1 :
            # num -= 10
            # TODO ADD SORTING queue to speedup access to the best node
            # find_best_node return a tuple with (index , node)
            best_node = self.find_best_node()
            # best_node = self.queue.pop(0)
            if best_node.row == self.row_goal and best_node.col == self.col_goal:
                # print(self.children_counter)
                self.is_found = True
                self.answer_node = best_node
                self.queue.clear()
                self.print_path()
                return True
            self.create_children(best_node)
            return True
        else:
            if self.is_idastar:
                if self.found_idastar :
                    self.found_idastar = False
                    self.all_visited.clear()
                    self.queue.append(self.start_node)
                    self.max_f += self.iterate

                else :
                    self.is_idastar = False
            return False


if __name__ == "__main__":
    matrix = [
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 3, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 2, 1, 1, 1, 0, 0],
    ]
    # matrix = [
    #     [0, 0, 0, 1, 3],
    #     [0, 1, 0, 1, 1],
    #     [0, 1, 0, 1, 0],
    #     [0, 0, 0, 1, 0],
    #     [2, 1, 0, 0, 0],
    # ]

    # If alpha be more that 1 algorithm gonna be Greedy like greedo
    # If alpha be 1 the algorithm is a*

    a = Astar(matrix, 1, conected=True, eight_direction=False, is_idastar=True, iterate=1)
    Display(a).show(clock=20)
