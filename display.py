# from astar import Astar
import sys
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (23, 32, 42)

SEXYBLUE = (102, 204, 255)
GRAYBLUE = (102, 153, 153)

GREEN = (130, 224, 170)
GREENDARK = (29, 131, 72)
DARKGREEN = (0, 155, 0)

ORANGE = (241, 196, 15)
REDDARK = (155, 0, 0)
RED = (255, 0, 0)
PINKZHOOON = (255, 102, 153)

FPS = 1
FPSCLOCK = pygame.time.Clock()


class Display:
    def __init__(self, node: "Astar"):
        self.matrix = node.matrix
        self.astar = node
        self.CELL_SIZE = 500 // max(len(self.matrix), len(self.matrix[0]))
        self.HEIGHT = len(self.matrix) * self.CELL_SIZE
        self.WIDTH = len(self.matrix[0]) * self.CELL_SIZE

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.CELL_WIDTH = self.CELL_SIZE
        self.CELL_HEIGHT = self.CELL_SIZE
        pygame.display.set_caption('A* - Find Shortest Path')
        pygame.init()

    def terminate(self):
        pygame.quit()
        sys.exit()

    # we use the sizes to draw as well as to do our "steps" in the loops.

    def createSquare(self, x, y, color):
        pygame.draw.rect(self.screen, color, [x, y, self.CELL_WIDTH, self.CELL_HEIGHT])

    def drawGrid(self):
        for x in range(0, self.CELL_WIDTH, self.CELL_WIDTH):  # draw vertical lines
            pygame.draw.line(self.screen, DARKGRAY, (x, 0), (x, self.CELL_HEIGHT))
        for y in range(0, self.CELL_HEIGHT, self.CELL_WIDTH):  # draw horizontal lines
            pygame.draw.line(self.screen, DARKGRAY, (0, y), (self.CELL_WIDTH, y))

    def visualizeGrid(self):
        r = 0  # we start at the top of the screen
        for row in self.matrix:
            c = 0  # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.createSquare(c, r, (171, 178, 185))
                elif item > 1:
                    self.createSquare(c, r, (146, 43, 33))
                else:
                    self.createSquare(c, r, (23, 32, 42))

                c += self.CELL_WIDTH  # for ever item/number in that row we move one "step" to the right
            r += self.CELL_HEIGHT  # for every new row we move one "step" downwards

    def drawNextCandidate(self, list_candidate, color, frame_color):
        for candidate in list_candidate:
            row = candidate.row * self.CELL_WIDTH
            col = candidate.col * self.CELL_HEIGHT

            self.createSquare(col, row, color)
            cell_frame = pygame.Rect(col + 4, row + 4, self.CELL_WIDTH - 8, self.CELL_WIDTH - 8)
            pygame.draw.rect(self.screen, frame_color, cell_frame)

    def drawCell(self, list_item, color, frame_color):
        for item in list_item:
            row = item[0] * self.CELL_WIDTH
            col = item[1] * self.CELL_HEIGHT

            self.createSquare(col, row, frame_color)
            cell_frame = pygame.Rect(col + 4, row + 4, self.CELL_WIDTH - 8, self.CELL_WIDTH - 8)
            pygame.draw.rect(self.screen, color, cell_frame)

    def show(self, clock=30):
        self.visualizeGrid()
        while True:
            for event in pygame.event.get():
                if event.type == 256:
                    self.terminate()


            if self.astar.run():
                # util not find draw visited and candidate
                if not self.astar.is_found:
                    # draw visited node
                    self.drawCell(self.astar.all_visited, (86, 101, 115), (44, 62, 80))
                    # draw next candidate
                    self.drawNextCandidate(self.astar.queue, (212, 172, 13), (244, 208, 63))
                # when find path
                else :
                    # draw answer
                    # number in tuple are rgb code , don't panic
                    self.drawCell(self.astar.path(), (23, 165, 137), (17, 120, 100))
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    text_path = font.render(f"Path Length:{len(self.astar.path())}", True, ORANGE, (0, 0, 0))
                    text_childrens = font.render(f"Created Children:{self.astar.children_counter}", True, ORANGE, (0, 0, 0))
                    textRect = text_path.get_rect()
                    textRect.center = (self.WIDTH // 2, self.HEIGHT // 2)
                    self.screen.blit(text_path, textRect)
                    textRect.center = (self.WIDTH // 2, (self.HEIGHT // 2) + self.CELL_HEIGHT)
                    self.screen.blit(text_childrens, textRect)
            # No path message
            else:
                if self.astar.is_idastar:
                    self.visualizeGrid()
                else :
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    text_nopath = font.render(f"No Path - {self.astar.children_counter} Node Visited", True, ORANGE, (0, 0, 0))
                    textRect = text_nopath.get_rect()
                    textRect.center = (self.WIDTH // 2, self.HEIGHT // 2)
                    self.screen.blit(text_nopath, textRect)

            pygame.display.update()
            FPSCLOCK.tick(clock)
