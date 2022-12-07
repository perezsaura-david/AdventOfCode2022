import cv2
import numpy as np

class Visualizer:
    def __init__(self, n_columns, max_rows, mode):
        print(f'columns: {n_columns}, rows: {max_rows}')
        self.n_columns = n_columns + 1
        self.max_rows = max_rows + 1
        self.char_width = 20 
        self.char_height = 20
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
        for i in range(len(self.storage)):
            for j in range(len(self.storage[i])):
                block = self.storage[i][j]
                # print(f'block: {block}')
                x = (i) * self.char_width
                y = (j) * self.char_height
                y = self.max_rows * self.char_height - y # translate to image coordinate
                # offset to make it look better 
                x += self.char_width // 2
                y -= self.char_width // 2 
                # print(f'image: {self.image.shape}')
                # print(f'x: {x}, y: {y}')

                self.drawBlock(block,x, y)


    def show(self):
        cv2.imshow('image', self.image)
        # cv2.waitKey(self.interval)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # def save(self, filename):
    #     cv2.imwrite(filename, self.img)
