import cv2
import numpy as np

class Visualizer:
    def __init__(self, n_columns, max_rows, mode):
        self.block_type = 3
        self.n_columns = self.block_type * n_columns + 1
        self.max_rows = self.block_type * max_rows + 1
        self.char_width = 10 
        self.char_height = 10
        self.interval = 20
        self.mode = 1

        self.image = np.zeros((self.max_rows * self.char_height, self.n_columns * self.char_width, 3), np.uint8)
        # self.image = np.zeros((self.n_columns * self.char_width, self.max_rows * self.char_height, 3), np.uint8)
        self.columns = np.zeros(self.n_columns, dtype=object)

    def setStorage(self, storage):
        self.storage = storage

    def drawBlock(self, char, x, y):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = self.char_width / 25
        font_color = (255, 255, 255)
        line_type = 1
        cv2.putText(self.image, char, (x, y), font, font_scale, font_color, line_type)
        return

    def drawStorage(self):
        self.image = 0*self.image
        for i in range(len(self.storage)):
            for j in range(len(self.storage[i])):
                if self.block_type == 1:
                    block = self.storage[i][j]
                    x = (i) * self.char_width
                    y = (j) * self.char_height
                    # translate to image coordinate
                    y = self.max_rows * self.char_height - y 
                    # offset to make it look better 
                    x += self.char_width // 2
                    y -= self.char_width // 2 
                    self.drawBlock(block,x, y)
                if self.block_type == 3:
                    for k in [-1, 0, 1]:
                        if k == 0:
                            block = self.storage[i][j]
                        if k == -1:
                            block = '['
                        if k == 1:
                            block = ']'
                        x = (i * self.block_type + k + 1) * self.char_width
                        y = (j) * self.char_height * 2
                        # translate to image coordinate
                        y = self.max_rows * self.char_height - y 
                        # offset to make it look better 
                        x += self.char_width // 2
                        y -= self.char_width // 2 
                        self.drawBlock(block,x, y)


    def show(self, time):
        cv2.imshow('image', self.image)
        # cv2.waitKey(self.interval)
        cv2.waitKey(time)
        cv2.destroyAllWindows()

    # def save(self, filename):
    #     cv2.imwrite(filename, self.img)
