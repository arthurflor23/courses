from PIL import Image
import matplotlib.pyplot as plt
import numpy
import time
import os

def histogram(arr):
    h_arr = numpy.zeros(256)
    g_arr = ["" for x in range(256)]

    for y in range(len(arr[0])):
        for x in range(len(arr)):
            h_arr[arr[y+x]] += 1

    max_arr = max(h_arr)
    for x in range(len(h_arr)):
        g_arr[x] = (str(x) + "\t: " + str("|" * int((h_arr[x] * 100)/int(max_arr)) + "\n"))

    return [h_arr, g_arr]

def printHistogramTxt(save_path, g_arr):
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

def isValid(arr, y, x):
    if ((y >= 0 and y < len(arr)) and (x >= 0 and x < len(arr[0]))):
        return True
    else:
        return False

def getWindowAVG(arr, y, x):
    values = []

    for y2 in range(-1, 2):
        for x2 in range(-1, 2):
            temp_y = y + y2
            temp_x = x + x2

            if (isValid(arr, temp_y, temp_x)):
                values.append(arr[temp_y, temp_x])

    l_avg = [int(numpy.mean(values)), numpy.std(values)]
    return l_avg

def clear(k, g_avg, l_avg):
    if (l_avg[0] <= g_avg[0]):
        if (l_avg[1] > (g_avg[1] * k[0]) and (l_avg[1] < (g_avg[1] * k[1]))):
            return k[2]
    return 0

def darken(k, g_avg, l_avg):
    if (l_avg[0] >= g_avg[0]):
        if (l_avg[1] > (g_avg[1] * k[0]) and (l_avg[1] < (g_avg[1] * k[1]))):
            return k[2]
    return 0

def realce(img, option):
    path = "realce"
    save_path = os.path.join(path, "result_dp", img)

    im = Image.open(os.path.join(path, img), "r")
    width, height = im.size

    arr = numpy.array(im, dtype=numpy.uint8)
    n_arr = numpy.zeros((height, width), dtype=numpy.uint8)

    k = [0.1, 1, 2]
    g_avg = [numpy.mean(arr), numpy.std(arr)]
    print("Média global: " + str(g_avg[0]) + " | Desvio padrão global: " + str(g_avg[1]))

    for y in range(height):
        for x in range(width):
            l_avg = getWindowAVG(arr, y, x)

            if (option == "darken"):
                k3 = darken(k, g_avg, l_avg)
            elif (option == "clear"):
                k3 = clear(k, g_avg, l_avg)

            if (option == "darken" and k3 > 0):
                n_arr[y, x] = int(arr[y, x] / k3)
            elif (option == "clear" and k3 > 0):
                n_arr[y, x] = int(arr[y, x] * k3)
            else:
                n_arr[y, x] = arr[y, x]

            if (n_arr[y, x] < 0):
                n_arr[y, x] = 0
            elif (n_arr[y, x] > 255):
                n_arr[y, x] = 255
            
    # os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # h_arr, g_arr = histogram(arr)
    # printHistogramTxt(save_path, g_arr)
    # printHistogramGraph(save_path, h_arr)

    # h_arr, g_arr = histogram(n_arr)
    # printHistogramTxt(save_path, g_arr)
    # printHistogramGraph(save_path, h_arr)

    Image.fromarray(n_arr).show()
    # Image.fromarray(n_arr).save(save_path)

begin = time.time()
# realce("Clarear_(1).jpg", "clear")
# realce("Clarear_(2).jpg", "clear")
# realce("Clarear_(3).jpg", "clear")

# realce("Escurecer_(1).jpg", "darken")
realce("Escurecer_(2).jpg", "darken")
# realce("Escurecer_(3).jpg", "darken")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")