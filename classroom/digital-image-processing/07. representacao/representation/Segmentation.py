import numpy as np
import Image as im
import copy

class Edge(object):
    def __init__(self):
        self.kernel = np.array([
            [0, 0,   1, 0, 0],
            [0, 1,   2, 1, 0],
            [1, 2, -16, 2, 1],
            [0, 1,   2, 1, 0],
            [0, 0,   1, 0, 0],
        ])
        self.sobel_x = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ])
        self.sobel_y = np.array([
            [ 1,  2,  1],
            [ 0,  0,  0],
            [-1, -2, -1],
        ])

    def laplaceofGaussian(self, image, line=True):
        img = copy.deepcopy(image)
        img.clear(times=img.noise)

        G_x = img.convolve(self.sobel_x)
        G_y = img.convolve(self.sobel_y)

        G = np.power(np.add(np.square(G_x), np.square(G_y)), 0.5)
        G = (G>32) * G

        (M,N) = img.shapes
        t_im = np.zeros((M,N))
        temp = np.zeros((M+2, N+2))
        temp[1:-1,1:-1] = img.convolve(self.kernel)
        around = (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)

        for i in range(1,M+1):
            for j in range(1,N+1):
                if (temp[i,j] < 0):
                    for x,y in around:
                        if (temp[i+x,j+y] > 0):
                            t_im[i-1,j-1] = 1

        img.setImg(np.logical_and(t_im, G))
        if (line):
            img.setImg(np.logical_not(img.arr))

        return img

class Thresholding(object):
    def __init__(self):
        self.hist = im.Histogram() 
        return

    def otsu(self, image, edge=False):
        img = copy.deepcopy(image)

        if (edge):
            img = Edge().laplaceofGaussian(image)
            img.setImg(np.multiply(image.arr, img.arr))
        else:
            img.clear(times=img.noise)

        hist = self.hist.getValues(img.arr)
        total = (img.shapes[0] * img.shapes[1])

        current_max, threshold = 0, 0
        sumT, sumF, sumB = 0, 0, 0

        weightB, weightF = 0, 0
        varBetween, meanB, meanF = 0, 0, 0

        for i in range(0,256):
            sumT += (i * hist[i])

        for i in range(0,256):
            weightB += hist[i]
            weightF = total - weightB
            if (weightF <= 0):
                break
            if (weightB <= 0):
                weightB = 1

            sumB += (i * hist[i])
            sumF = sumT - sumB
            meanB = sumB/weightB
            meanF = sumF/weightF
            varBetween = (weightB * weightF)
            varBetween *= (meanB-meanF) * (meanB-meanF)

            if (varBetween > current_max):
                current_max = varBetween
                threshold = i

        img.arr[img.arr <= threshold] = 0
        img.arr[img.arr > threshold] = 1
        return img