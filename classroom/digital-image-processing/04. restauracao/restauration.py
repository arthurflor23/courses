from matplotlib import pyplot as plt
from random import gauss
import numpy as np
import os

class Filter():
    def do(self, image):
        img = Image(image)
        hist = Histogram()

        h_original = hist.getValues(img.arr)
        hist.save(h_original, img.name, "h_original")

        ### Mean ###
        extension = "7x7_media"
        mean = Image(self.mean(img.arr), img.name)
        mean.save(extension)
        
        h_restored = hist.getValues(mean.arr)
        hist.save(h_restored, img.name, (extension+"_h_restored"))

        h_diff = hist.diff(h_original, h_restored)
        hist.save(h_diff, img.name, (extension+"_h_diff"))

        ### Median ###
        extension = "7x7_mediana"
        median = Image(self.median(img.arr), img.name)
        median.save(extension)

        h_restored = hist.getValues(median.arr)
        hist.save(h_restored, img.name, (extension+"_h_restored"))

        h_diff = hist.diff(h_original, h_restored)
        hist.save(h_diff, img.name, (extension+"_h_diff"))

    def mean(self, arr, kernel=None):
        return self.convolve(self.__mean, arr, kernel)

    def median(self, arr, kernel=None):
        return self.convolve(self.__median, arr, kernel)

    def __mean(self, arr, kernel):
        return np.average(arr, weights=kernel)
    
    def __median(self, arr, kernel):
        return np.median(np.multiply(arr, kernel))

    def convolve(self, function, arr, kernel=None):
        if (kernel is None):
            kernel = np.ones((7, 7))

        m, n = kernel.shape
        pad_h, pad_w = (m//2), (n//2)
        H, W = arr.shape

        img = np.ones((H + pad_h * 2, W + pad_w * 2)) * 128
        new_img = np.ones((H + pad_h * 2, W + pad_w * 2))
        img[pad_h:-pad_h, pad_w:-pad_w] = arr

        for i in range(pad_h, H+pad_h):
            for j in range(pad_w, W+pad_w):
                new_img[i,j] = function(img[i-pad_h:i+m-pad_h, j-pad_w:j+n-pad_w], kernel)

        return new_img[pad_h:-pad_h,pad_w:-pad_w]


class Noise():
    def __init__(self, uni_p=0.15, bi_p=0.10, g_mean=10, g_sigma=30, g_n=100):
        self.uni_p = uni_p
        self.bi_p = bi_p
        self.gauss_mean = g_mean
        self.gauss_sigma = g_sigma
        self.gauss_n = g_n
        self.gauss = None
        self.gaussianGenerate()

    def do(self, image):
        img = Image(image)
        matrix_uni = self.unipolar(img.shapes)
        matrix_bi = self.bipolar(img.shapes)
        matrix_gauss = self.gaussian(img.shapes)

        img_uni = Image(np.add(img.arr, matrix_uni), img.name)
        img_bi = Image(np.add(img.arr, matrix_bi), img.name)
        img_gauss = Image(np.add(img.arr, matrix_gauss), img.name)

        img_uni.save("(noise)_unipolar")
        img_bi.save("(noise)_bipolar")
        img_gauss.save("(noise)_gauss")

    def unipolar(self, shapes):
        return np.random.choice([-255,0], size=(shapes[0], shapes[1]), p=[self.uni_p, (1-self.uni_p)])

    def bipolar(self, shapes):
        return np.random.choice([-255,0,255], size=(shapes[0], shapes[1]), p=(0.05, 0.9, 0.05))

    def gaussian(self, shapes):
        return np.random.choice(self.gauss, size=(shapes[0], shapes[1]))
    
    def gaussianGenerate(self):
        self.gauss = [gauss(self.gauss_mean, self.gauss_sigma) for i in range(self.gauss_n)]

class Histogram():
    def getValues(self, arr, show=False):
        y_arr = np.zeros(256, dtype=int)
        for y in range(len(arr)):
            for x in range(len(arr[0])):
                y_arr[int(arr[y,x])] += 1
        if (show):
            plt.show()
        return y_arr

    def diff(self, original, result):
        y_arr = np.subtract(original, result)
        y_arr[y_arr < 0] = 0
        return y_arr

    def save(self, y_arr, name, extension="histogram", color="black"):
        x_arr = [x for x in range(256)]
        plt.bar(x_arr, y_arr, width=1, color=color)
        plt.plot(x_arr, y_arr, color=color)
        plt.title("Histograma")
        plt.xlabel("Pixel")
        plt.ylabel("Frequência")
        plt.savefig(Utils().getPathToSave(name, extension))
        plt.close()


class Image():
    def __init__(self, img=None, name="image"):
        self.name = name
        self.arr = None
        self.shapes = None
        self.load(img)

    def load(self, img):
        if (isinstance(img, str)):
            self.name = img
            self.arr = np.array(plt.imread(os.path.join(Utils().path, img)))
            self.convertToGray()
        else:
            self.arr = np.asarray(img, dtype=float)
        self.shapes = self.arr.shape

    def show(self, mode="Greys_r"):
        plt.imshow(self.arr, cmap=mode, vmin=0, vmax=255)
        plt.show()

    def save(self, extension=None, mode="Greys_r"):
        plt.imsave(Utils().getPathToSave(self.name, extension), self.arr, cmap=mode, vmin=0, vmax=255)

    def convertToGray(self):
        if (len(self.arr.shape) == 3):
            self.arr = np.dot(self.arr[...,:3], [0.299, 0.587, 0.114])


class Utils():
    def __init__(self):
        self.path = "images"

    def getName(self, name, extension):
        return name.replace(".", ("_" + extension + "."))

    def getPathToSave(self, name="image.jpg", extension="result"):
        path = os.path.join(self.path, name.split(".")[0])
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, self.getName(name, extension))


### Main ###
def main():

    ### 1ª questão
    Noise().do("image_(1).jpg")

    ### 2ª questão
    Filter().do("image_(2).jpg")
    Filter().do("image_(3).jpg")
    Filter().do("image_(4).jpg")
            
if __name__ == "__main__":
    main()