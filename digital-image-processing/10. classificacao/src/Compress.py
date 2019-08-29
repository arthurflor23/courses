import Image as im
import numpy as np
import heapq
import pickle

class LZW:
    def __init__(self):
        self.image = None
        self.path = None
        self.output_dat = None
        self.output_info = None
        self.dictionary = None
        self.separator = "-"

    def load(self, image):
        self.image = image
        self.path = self.image.path.getPathSave(self.image.name)
        self.output_dat = self.path + "_lzw_compress.dat"
        self.output_info = self.path + "_lzw_compress.txt"
        self.dictionary = [chr(c) for c in range(256)]

    def compress(self, image):
        self.load(image)

        array = self.image.arr.ravel()
        array_str = self.separator.join(map(str, array))
        output = self.encode(array_str)

        with open(self.output_dat, 'wb') as file:
            pickle.dump(output, file, pickle.HIGHEST_PROTOCOL)
            file.close()

        print('Imagem comprimida...')
        start_bits = self.image.shapes[0] * self.image.shapes[1] * 8
        end_bits = np.sum([item.bit_length() for i, item in enumerate(output)])

        compression = start_bits/end_bits
        redundancy = 1 - (1/compression)

        file = open(self.output_info,'w')
        file.write('Start Bits: ' + str(start_bits))
        file.write('\nEnd Bits: ' + str(end_bits))
        file.write('\nTaxa de compressão: ' + str(compression))
        file.write('\nRedundância relativa: ' + str(redundancy))
        file.close() 

        return self.output_dat

    def encode(self, string):
        w, b, output = "", 0, []

        while (b < len(string)):
            k = string[b]
            wk = w+k
            if(wk in self.dictionary):
                w = wk
                b = b+1
            else:
                self.dictionary.append(wk)
                indice = self.dictionary.index(w)
                output.append(indice)
                w = k
                b = b+1

        indice = self.dictionary.index(w)
        output.append(indice)
        return output

    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            code = pickle.load(file)
            file.close()
        
        output = self.decode(code)
        matrix = np.reshape(output.split(self.separator), self.image.shapes)

        self.image.setImg(matrix)
        self.image.save(extension="lzw")
        print("Imagem descomprimida...")

    def decode(self, string):
        res = []
        i = 0
        index = string[i]
        char = self.dictionary[index]
        res.append(char)
        i+=1
        while (i < len(string)):
            n_index = string[i]
            if(n_index not in self.dictionary):
                tmp = self.dictionary[n_index]
                res.append(tmp)
                char = tmp[0]
                self.dictionary.append(self.dictionary[index] + char)
                index = n_index
                i+=1
            else:
                tmp = self.dictionary[index]
                tmp = tmp + char
                i+=1
        return ''.join(res)


class Huffman:
    def __init__(self):
        self.image = None
        self.path = None
        self.histogram = None
        self.output_dat = None
        self.output_info = None
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def load(self, image):
        self.image = image
        self.path = self.image.path.getPathSave(self.image.name)
        self.histogram = im.Histogram().getValues(self.image.arr)
        self.output_dat = self.path + "_huffman_compress.dat"
        self.output_info = self.path + "_huffman_compress.txt"

    def saveCodes(self):
        file = open((self.path + "_huffman_codes.txt"),'w')
        for x in range(len(self.codes)):
            file.write(str(x) + ' ' + str(self.codes[x]) + '\n')
        file.close()

    def compress(self, image):
        self.load(image)

        with open(self.output_dat, 'wb') as file:
            vector = self.image.arr.ravel()

            self.makeHeap(self.histogram)
            self.mergeNodes()

            self.makeCodes()
            self.saveCodes()

            encoded = self.getEncoded(vector)
            padded_encoded = self.padEncoded(encoded)

            b = self.getByteArray(padded_encoded)
            file.write(bytes(b))
            file.close()

        print('Imagem comprimida...')
        start_bits = self.image.shapes[0] * self.image.shapes[1] * 8
        end_bits = len(padded_encoded)

        compression = start_bits/end_bits
        redundancy = 1 - (1/compression)

        file = open(self.output_info,'w')
        file.write('Start Bits: ' + str(start_bits))
        file.write('\nEnd Bits: ' + str(end_bits))
        file.write('\nTaxa de compressão: ' + str(compression))
        file.write('\nRedundância relativa: ' + str(redundancy))
        file.close()

        return self.output_dat

    def makeHeap(self, histogram):
        for (i, histogram) in enumerate(histogram):
            node = HeapNode(i, histogram)
            heapq.heappush(self.heap, node)

    def mergeNodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def makeCodes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.makeCodesHelper(root, current_code)

    def makeCodesHelper(self, root, current_code):
        if(root == None):
            return
        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.makeCodesHelper(root.left, current_code + "0")
        self.makeCodesHelper(root.right, current_code + "1")

    def getEncoded(self, vector):
        encoded = ""
        for index in vector:
            encoded += self.codes[index]
        return encoded

    def padEncoded(self, encoded):
        extra_padding = 8 - len(encoded) % 8
        for _ in range(extra_padding):
            encoded += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded = padded_info + encoded
        return encoded

    def getByteArray(self, padded_encoded):
        b = bytearray()
        if(len(padded_encoded) % 8 != 0):
            exit(0)
        for i in range(0, len(padded_encoded), 8):
            byte = padded_encoded[i:i+8]
            b.append(int(byte, 2))
        return b

    def decompress(self, input_file):
        with open(input_file, 'rb') as file:
            bit_string = ""
            byte = file.read(1)

            while(len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            file.close()

        encoded = self.removePadding(bit_string)
        decompressed = self.decode(encoded)
        matrix = np.reshape(decompressed, self.image.shapes)

        self.image.setImg(matrix)
        self.image.save(extension="huffman")
        print('Imagem descomprimida...')

    def removePadding(self, padded_encoded):
        padded_info = padded_encoded[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded = padded_encoded[8:] 
        encoded = padded_encoded[:-1*extra_padding]
        return encoded

    def decode(self, encoded):
        current_code = ""
        decoded = []
        for bit in encoded:
            current_code += bit
            if(current_code in self.reverse_mapping):
                decoded.append(self.reverse_mapping[current_code])
                current_code = ""
        return decoded


class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if (other == None or not isinstance(other, HeapNode)):
            return False
        return self.freq == other.freq