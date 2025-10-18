import os
import csv
import h5py
import numpy as np
import Image as im

class Path():
    def __init__(self):
        self.resources = os.path.join("..", "data")
        self.results = os.path.join("..", "out")

    def getFileDir(self, file_name):
        return os.path.join(self.resources, file_name)

    def getNameResult(self, file_name, extension):
        if (extension is None):
            return file_name
        else:
            try:
                splitted = file_name.split(".")
                return splitted[0] + "_" + extension + "." + splitted[1]
            except:
                return file_name + "_" + extension 

    def getPathSave(self, name):
        os.makedirs(self.results, exist_ok=True)
        return os.path.join(self.results, name)

    def getFiles(self, path, folders=True):
        index = 1 if folders else 2
        return np.sort([os.path.join(path,x) for x in next(os.walk(Path().getFileDir(path)))[index]])

    def getFilesWithResources(self, folders):
        return [self.getFileDir(item) for x, item in enumerate(folders)]

class Data():
    def saveVariable(self, name, extension, value):
        if (not isinstance(value, str)):
            value = "\n".join(value)
        n = Path().getNameResult(name+".txt", extension)
        with open(Path().getPathSave(n), "w") as variable_file:
            variable_file.write(value)

    def fetchFromCSV(self, file_name):
        reader = csv.reader(open(Path().getFileDir(file_name), "rt"))
        return [[convertTypes(item) for item in row] for row in reader]

    def fetchFromH5(self, train_name, test_name):
        train_dataset = h5py.File(Path().getFileDir(train_name), "r")
        train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features
        train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

        test_dataset = h5py.File(Path().getFileDir(test_name), "r")
        test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
        test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels

        # classes = np.array(test_dataset["list_classes"][:]) # the list of classes
        classes = ('cat', 'non-cat')
        
        train_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T # The "-1" makes reshape flatten the remaining dimensions
        test_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T    # Standardize data to have feature values between 0 and 1.

        train_x = fetchH5toRGBImage(train_x_flatten.transpose())
        test_x = fetchH5toRGBImage(test_x_flatten.transpose())

        train_y = arrayBool2String(train_set_y_orig, classes[0], classes[1])
        test_y = arrayBool2String(test_set_y_orig, classes[0], classes[1])

        return train_x, train_y, test_x, test_y

    def fetchFromPath(self, path, set):
        folders = Path().getFiles(os.path.join(path, set), True)
        files = Path().getFiles(os.path.join(path, set), False)

        filesWithResources = Path().getFilesWithResources(files)
        foldersWithResources = Path().getFilesWithResources(folders)

        classes = [line.rstrip('\n') for line in open(filesWithResources[0])]
        train_x, train_y = [], []

        for y, item in enumerate(foldersWithResources):
            imgs = Path().getFiles(item, False)

            for _, img in enumerate(imgs):
                i = im.Image(img)
                train_x.append(i.arr)    
                train_y.append(classes[y])

        return train_x, train_y

def arrayBool2String(array, option1, option2):
    return list(map(lambda x: option1 if x else option2, array))

def convertTypes(s):
    s = s.strip()
    try:
        return float(s) if '.' in s else int(s)
    except ValueError:
        return s

def fetchH5toRGBImage(array):
    size = int(np.sqrt(array.shape[1]/3))
    images = np.zeros((array.shape[0], size, size, 3))

    for y in range(array.shape[0]):
        temp = array[y].reshape((size, size, 3))
        images[y] = temp
    return images