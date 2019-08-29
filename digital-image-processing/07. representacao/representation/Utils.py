import os

class Path():
    def __init__(self):
        self.resources = os.path.join("..", "images")
        self.results = os.path.join("results")

    def getFileDir(self, file_name):
        return os.path.join(self.resources, file_name)

    def getNameResult(self, file_name, extension):
        if (extension is None):
            return file_name
        else:
            return file_name.replace(".", ("_"+extension+"."))

    def getPathSave(self, name):
        os.makedirs(self.results, exist_ok=True)
        return os.path.join(self.results, name)

class Data():

    def saveVariable(self, name, extension, value):
        n = Path().getNameResult(name+".txt", extension)
        with open(Path().getPathSave(n), "w") as variable_file:
            variable_file.write(value)