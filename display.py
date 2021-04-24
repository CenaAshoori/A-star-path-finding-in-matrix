# from astar import Astar
import sys
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)

SEXYBLUE = (102, 204, 255)
GRAYBLUE = (102, 153, 153)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

REDDARK = (155, 0, 0)
RED = (255, 0, 0)
PINKZHOOON = (255, 102, 153)

FPS = 1
FPSCLOCK = pygame.time.Clock()


class Display:
    def __init__(self, node: "Astar"):
        self.matrix = node.matrix
        self.node = node
        self.CELL_HEIGHT = len(self.matrix) * 5
        self.CELL_WIDTH = len(self.matrix[0]) * 5
        self.HEIGHT = len(self.matrix) * 50
        self.WIDTH = len(self.matrix[0]) * 50

        self.gridDisplay = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.visualizeGrid()

    def terminate(self):
        pygame.quit()
        sys.exit()

    # we use the sizes to draw as well as to do our "steps" in the loops.

    def createSquare(self, x, y, color):
        pygame.draw.rect(self.gridDisplay, color, [x, y, self.CELL_WIDTH, self.CELL_HEIGHT])

    def drawGrid(self):
        for x in range(0, self.CELL_WIDTH, self.CELL_WIDTH):  # draw vertical lines
            pygame.draw.line(self.gridDisplay, DARKGRAY, (x, 0), (x, self.CELL_HEIGHT))
        for y in range(0, self.CELL_HEIGHT, self.CELL_WIDTH):  # draw horizontal lines
            pygame.draw.line(self.gridDisplay, DARKGRAY, (0, y), (self.CELL_WIDTH, y))

    def visualizeGrid(self):
        y = 0  # we start at the top of the screen
        for row in self.matrix:
            x = 0  # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.createSquare(x, y, (255, 255, 255))
                else:
                    self.createSquare(x, y, (0, 0, 0))

                x += self.CELL_WIDTH  # for ever item/number in that row we move one "step" to the right
            y += self.CELL_HEIGHT  # for every new row we move one "step" downwards

    def drawNextCandidate(self, list_candidate, color):
        for candidate in list_candidate:
            row = candidate.row * self.CELL_WIDTH
            col = candidate.col * self.CELL_HEIGHT

            self.createSquare(col, row, color)

    def drawCell(self, list_item, color, frame_color):
        for item in list_item:
            y = item[0] * self.CELL_WIDTH
            x = item[1] * self.CELL_HEIGHT

            self.createSquare(x, y, color)
            cell_frame = pygame.Rect(x + 4, y + 4, self.CELL_WIDTH - 8, self.CELL_WIDTH - 8)
            pygame.draw.rect(self.gridDisplay, frame_color, cell_frame)

    def show(self, clock):

        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == 256:
                    self.terminate()

            self.node.run()
            if self.node.is_found:
                # draw answer
                self.drawCell(self.node.path(), SEXYBLUE, (0, 153, 255))
            else:
                # draw next candidate
                self.drawNextCandidate(self.node.queue, PINKZHOOON)
                # draw visited node
                self.drawCell(self.node.all_visited, GRAYBLUE, (51, 204, 204))
            pygame.display.update()
            FPSCLOCK.tick(FPS * clock)
        # keeps the window open so you can see the result.


if __name__ == "__main__":
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # If alpha be more that 1 algorithm gonna be Greedy like greedo
    # If alpha be 1 the algorithm is a*
    #
    # a = Astar(9, 4, 0, 4, 1, matrix)
    #
    # display = Display(a).show()
