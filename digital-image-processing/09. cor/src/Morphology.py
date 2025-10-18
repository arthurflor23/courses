import numpy as np
import Image as im
import copy

class Morphology(object):

    def logicalOperator(self, arr1, arr2, operator):
        name = arr1.name + "_" + operator + "_" + arr2.name
        img = im.Image(name=name)
        op = operator.lower()

        if (op == "or"):
            temp = np.add(arr1.arr, arr2.arr)
            temp[temp > 0] = 1
            img.setImg(temp)

        elif (op == "and"):
            img.setImg(np.multiply(arr1.arr, arr2.arr))

        elif (op == "xor"):
            temp = np.subtract(arr1.arr, arr2.arr)
            temp[temp < 0] = 1
            img.setImg(temp)

        elif (op == "nand"):
            temp = np.add(arr1.arr, arr2.arr)
            temp[temp == 0] = 1
            temp[temp == 2] = 0
            img.setImg(temp)

        return img

    def dilate(self, image, kernel=None, side=3):
        if (kernel is None):
            kernel = np.ones((side,side))
        return self.filterMorph(image, kernel, 1, np.prod, np.multiply)
    
    def erode(self, image, kernel=None, side=3):
        if (kernel is None):
            kernel = np.ones((side,side))
        kernel = np.logical_not(kernel)
        return self.filterMorph(image, kernel, 0, np.sum, np.add)

    def filterMorph(self, image, kernel, factor, externalFunction, internalFunction):
        im = copy.deepcopy(image)
        m, n = kernel.shape
        pad_h, pad_w = (m//2), (n//2)
        H, W = image.arr.shape

        img = np.ones((H + pad_h * 2, W + pad_w * 2)) * 128
        new_img = np.ones((H + pad_h * 2, W + pad_w * 2))
        img[pad_h:-pad_h, pad_w:-pad_w] = image.arr

        for i in range(pad_h, H+pad_h):
            for j in range(pad_w, W+pad_w):
                current_window = img[i-pad_h:i+m-pad_h, j-pad_w:j+n-pad_w]
                new_img[i,j] = externalFunction(internalFunction(current_window[kernel==factor], kernel[kernel==factor]))

        new_img[new_img > 0] = 1
        im.setImg(new_img[pad_h:-pad_h,pad_w:-pad_w])
        return im

    def skeleton(self, image):
        img = copy.deepcopy(image)

        kernel = np.array([
            [1,1,1,0,0,0,1,1,1],
            [0,1,1,1,0,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,0],
        ])

        kernel2 = np.array([
            [0,1,1,1,0],
            [0,1,1,1,0],
            [0,1,1,1,0],
            [1,1,0,1,1],
            [1,0,0,0,1],
        ])

        img = self.dilate(img, kernel=kernel)
        img = self.dilate(img, kernel=kernel2)
        img = self.erode(img, kernel=kernel)
        return img

    def floodFill(self, image, start=(0,0), fill_value=1):
        im = copy.deepcopy(image)
        W, H = im.arr.shape
        orig_value = im.arr[start[0], start[1]]
        stack = set(((start[0], start[1]),))

        while stack:
            x, y = stack.pop()
            if (im.arr[x, y] == orig_value):
                im.arr[x, y] = fill_value
                if (x > 0):
                    stack.add((x - 1, y))
                if (x < (W - 1)):
                    stack.add((x + 1, y))
                if (y > 0):
                    stack.add((x, y - 1))
                if (y < (H - 1)):
                    stack.add((x, y + 1))
        return im