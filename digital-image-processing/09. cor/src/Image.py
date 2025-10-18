import matplotlib.pyplot as plt
import numpy as np
import Utils as utl

class Image():
    def __init__(self, img=None, type="png", name="image", gray=False):
        self.path = utl.Path()
        self.name = name
        self.type = type
        self.arr = None
        self.shapes = None

        if (isinstance(img, str)):
            self.name = img
            self.arr = np.array(plt.imread(self.path.getFileDir(self.name + "." + self.type)), dtype=float)
        else:
            self.arr = np.asarray(img, dtype=float)

        self.shapes = self.arr.shape
        self.normalize()
        if gray: self.imageToGray()

    def setImg(self, image, convert=False):
        self.arr = np.asarray(image, dtype=float)
        self.shapes = self.arr.shape
        if convert:
            self.imageToGray()

    def show(self, mode="Greys_r"):
        plt.imshow(self.arr, cmap=mode)
        plt.show()

    def save(self, extension=None, mode="Greys_r"):
        name = self.path.getNameResult(self.name+"."+self.type, extension)
        plt.imsave(self.path.getPathSave(name), self.arr, cmap=mode)

    def imageToGray(self):
        if (len(self.arr.shape) == 3):
            self.setImg(np.array(np.dot(self.arr[...,:3], [0.299, 0.587, 0.114]), dtype=float))

    def normalize(self):
        self.arr = np.divide(self.arr, 255) 

    def light(self, h=1, s=1, i=1):
        self.arr = np.apply_along_axis(self.rgb2hsv, 2, self.arr)
        self.arr = np.apply_along_axis(np.multiply, 2, self.arr, [h, s, i])
        self.arr = np.apply_along_axis(self.hsv2rgb, 2, self.arr)
        self.arr[self.arr < 0] = 0
        self.arr[self.arr > 1] = 1

    def rgb2hsv(self, pixel):
        r, g, b = pixel
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc
        if minc == maxc:
            return 0.0, 0.0, v
        s = (maxc-minc) / maxc
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0+rc-bc
        else:
            h = 4.0+gc-rc
        h = (h/6.0) % 1.0
        return h, s, v

    def hsv2rgb(self, pixel):
        h, s, v = pixel
        if s == 0.0:
            return v, v, v
        i = int(h*6.0)
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def rgb2hsi(self, pixel):
        r = pixel[0] 
        g = pixel[1] 
        b = pixel[2]
        
        num = 0.5 * ((r-g) + (r-b))
        den = np.sqrt(((r-g) * (r-g)) + (r-b) * (g-b))
        
        ind = np.zeros(shape=r.shape, dtype=bool)
        theta = np.zeros(shape=r.shape, dtype=float)

        ind = (den != 0)
        h = np.zeros(shape=r.shape, dtype=float)        
        h[ind] = np.arccos(num[ind]/den[ind]) / (2*np.pi)

        ind = (b > g)
        h[ind] = 1 - theta[ind]

        i = (r + g + b) / 3
        
        s = np.zeros(shape=r.shape, dtype=float)
        ind = (i != 0)
        s[ind] = 1 - np.minimum(np.minimum(r, g), b)[ind] / i[ind]

        return h,s,i

    def hsi2rgb(self, pixel):
        h = pixel[0] * 2 * np.pi
        s = pixel[1]
        i = pixel[2]

        r = np.zeros(shape=h.shape, dtype=float)
        g = np.zeros(shape=h.shape, dtype=float)
        b = np.zeros(shape=h.shape, dtype=float)

        # RG
        ind = np.logical_and(0 <= h, h < np.radians(120))
        b[ind] = i[ind]*(1 - s[ind])
        r[ind] = i[ind]*(1 + (s[ind]*np.cos(h[ind])) / np.cos(np.radians(60) - h[ind]))
        g[ind] = 3*i[ind] - (r[ind] + b[ind])

        # GB
        ind = np.logical_and(np.radians(120) <= h, h < np.radians(240))
        h_gb = h - np.radians(120)
        r[ind] = i[ind]*(1 - s[ind])
        g[ind] = i[ind]*(1 + (s[ind]*np.cos(h_gb[ind]) / np.cos(np.radians(60) - h_gb[ind])))
        b[ind] = 3*i[ind] - (r[ind] + g[ind])
        
        # RB
        ind = np.logical_and(np.radians(240) <= h, h <= np.radians(360))
        h_rb = h - np.radians(240)
        g[ind] = i[ind]*(1 - s[ind])
        b[ind] = i[ind]*(1 + (s[ind]*np.cos(h_rb[ind]) / np.cos(np.radians(60) - h_rb[ind])))
        r[ind] = 3*i[ind] - (g[ind] + b[ind])

        return r,g,b

    def clear(self, factor="gray", kernel=None, times=2, side=7, median=False, gauss=False):
        if (len(self.shapes) == 3):
            if (factor == "rgb"):
                for x in range(3):
                    self.__clear__(kernel=kernel, times=times, side=side, median=median, gauss=gauss, index=x)
            else:
                if (factor == "hsv"):
                    funcIn = self.rgb2hsv
                    funcOut = self.hsv2rgb
                elif (factor == "hsi"):
                    funcIn = self.rgb2hsi
                    funcOut = self.hsi2rgb

                self.arr = np.apply_along_axis(funcIn, 2, self.arr)
                self.__clear__(kernel=kernel, times=times, side=side, median=median, gauss=gauss)
                self.arr = np.apply_along_axis(funcOut, 2, self.arr)    
        else:
            self.__clear__(kernel=kernel, times=times, side=side, median=median, gauss=gauss)

        self.arr[self.arr < 0] = 0
        self.arr[self.arr > 1] = 1
        
        extension = factor
        if (median): extension += "_median"
        if (gauss): extension += "_gauss"
        extension += "_"+str(side)+"x"+str(side)+"_("+str(times)+"x)"
        return extension

    def __clear__(self, kernel, times, side, median, gauss, index=0):
        gaussian_filter = np.array([[1/16, 1/8, 1/16],[1/8,  1/4, 1/8],[1/16, 1/8, 1/16]])
        if (kernel is None): kernel = np.ones((side, side))

        if (median):
            for _ in range(times):
                self.arr = self.windowConvolve(kernel, np.median, index)
        if (gauss):
            for _ in range(times):
                self.arr = self.windowConvolve(gaussian_filter, np.sum, index)

    def convolve(self, kernel, index=0):
        return self.windowConvolve(kernel, np.sum, index)

    def windowConvolve(self, kernel, function, index):
        rgb = (len(self.shapes) == 3)
        arr_copy = self.arr
        m, n = kernel.shape
        pad_h, pad_w = (m//2), (n//2)

        arr = arr_copy[:,:,index] if (rgb) else arr_copy
        H, W = arr.shape
        
        img = np.ones((H + pad_h * 2, W + pad_w * 2)) * 128
        new_img = np.ones((H + pad_h * 2, W + pad_w * 2))
        img[pad_h:-pad_h, pad_w:-pad_w] = arr

        for i in range(pad_h, H+pad_h):
            for j in range(pad_w, W+pad_w):
                new_img[i,j] = function(np.multiply(img[i-pad_h:i+m-pad_h, j-pad_w:j+n-pad_w], kernel))

        n_arr = new_img[pad_h:-pad_h,pad_w:-pad_w]

        if (rgb):
            arr_copy[:,:,index] = n_arr[:,:]
        else:
            arr_copy = n_arr

        return arr_copy

    def features(self):
        n00 = self.momentCentral(self.arr, 0, 0)
        n11 = self.momentCentral(self.arr, 1, 1) / (n00 ** 2)
        n12 = self.momentCentral(self.arr, 1, 2) / (n00 ** 2.5)
        n21 = self.momentCentral(self.arr, 2, 1) / (n00 ** 2.5)
        n02 = self.momentCentral(self.arr, 0, 2) / (n00 ** 2)
        n03 = self.momentCentral(self.arr, 0, 3) / (n00 ** 2.5)
        n20 = self.momentCentral(self.arr, 2, 0) / (n00 ** 2)
        n30 = self.momentCentral(self.arr, 3, 0) / (n00 ** 2.5)
        
        mi1 = n20 + n02
        mi2 = (n20 - n02)**2 + 4*((n11)**2)
        mi3 = (n30 - (3*n12))**2 + ((3*n21) - n03)**2
        mi4 = (n30 + n12)**2 + (n21 - n03)**2
        mi5 = (n30 - (3*n12))*(n30 + n12)*((n30+n12)**2 - 3*((n21+n03)**2)) + ((3*n21) - n03)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)
        mi6 = (n20 - n02)*( ((n30+n12)**2) - (n21 + n03)**2 ) + 4*n11*(n30 + n12)*(n21 + n03)
        mi7 = ((3*n21) - n03)*(n30 + n12)*(((n30 + n12)**2) - 3*((n21 + n03)**2)) + ((3*n12) - n30)*(n21 + n03)*(3*((n30 + n12)**2) - (n21 + n03)**2)

        return [mi1, mi2, mi3, mi4, mi5, mi6, mi7]

    def momentCentral(self, arr, p, q):
        momCen, momPQ = 0, [0, 0, 0]

        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                momPQ[0] += (x**0) * (y**0) * arr[y, x]
                momPQ[1] += (x**1) * (y**0) * arr[y, x]
                momPQ[2] += (x**0) * (y**1) * arr[y, x]
        
        moment = [momPQ[1]/momPQ[0], momPQ[2]/momPQ[0]]

        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                momCen += ((x - moment[0])**p) * ((y - moment[1])**q) * arr[y, x]
        return momCen

class Histogram():
    def __init__(self):
        self.path = utl.Path()

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
        name = self.path.getNameResult(name, extension)
        x_arr = [x for x in range(256)]

        plt.bar(x_arr, y_arr, width=1, color=color)
        plt.plot(x_arr, y_arr, color=color)
        plt.title("Histograma")
        plt.xlabel("Pixel")
        plt.ylabel("Frequência")
        plt.savefig(self.path.getPathSave(name))
        plt.close()