from PIL import Image
import matplotlib.pyplot as plt
import numpy
import time
import os

def getMinMax(arr):
    # return [min(arr), max(arr)]
    return [0, 255]

def histogram(arr):
    h_arr = numpy.zeros(256)
    g_arr = ["" for x in range(256)]

    for x in range(len(arr)):
        h_arr[arr[x]] += 1

    max_arr = max(h_arr)
    for x in range(len(h_arr)):
        g_arr[x] = (str(x) + "\t: " + str("|" * int((h_arr[x] * 100)/int(max_arr)) + "\n"))

    return [h_arr, g_arr, getMinMax(arr)]

def printHistogramTxt(save_path, g_arr, p_min_max):
    with open((save_path.split(".")[0] + "_histogram.txt"), "w") as text_file:
        text_file.write("Histograma da imagem: " + save_path + "\n\n")
        for x in range(len(g_arr)):
            text_file.write(g_arr[x])

def printHistogramGraph(save_path, h_arr):
    plt.bar([x for x in range(256)], h_arr)
    plt.title("Histograma")
    plt.xlabel("Pixel")
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.savefig(save_path.split(".")[0] + "_histogram.jpg")
    plt.clf()

def no_linear(min, max, x, exp):
    a = 255/(max - min)
    return int(a*(x **(exp*2)))

def realce(img, exp):
    path = "realce"
    save_path = os.path.join(path, img)

    im = Image.open(os.path.join(path, img), "r")
    l_pixel = list(im.getdata())

    h_arr, g_arr, p_min_max = histogram(l_pixel)
    printHistogramTxt(save_path, g_arr, getMinMax(l_pixel))
    printHistogramGraph(save_path, h_arr)

    save_path = os.path.join(path, "result", img)

    for x in range(len(l_pixel)):
        pixel = no_linear(p_min_max[0], p_min_max[1], l_pixel[x], exp)

        if (pixel < p_min_max[0]):
            l_pixel[x] = p_min_max[0]
        elif (pixel > p_min_max[1]):
            l_pixel[x] = p_min_max[1]
        else:
            l_pixel[x] = pixel

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    h_arr, g_arr, p_min_max = histogram(l_pixel)
    printHistogramTxt(save_path, g_arr, getMinMax(l_pixel))
    printHistogramGraph(save_path, h_arr)

    im2 = Image.new(im.mode, im.size)
    im2.putdata(l_pixel)
    # im2.show()
    im2.save(save_path)

begin = time.time()
realce("Clarear_(1).jpg", 0.75)
realce("Clarear_(2).jpg", 0.75)
realce("Clarear_(3).jpg", 0.75)

realce("Escurecer_(1).jpg", 0.4)
realce("Escurecer_(2).jpg", 0.4)
realce("Escurecer_(3).jpg", 0.4)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")