class node:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __str__(self):
        return f"[{self.value} {self.freq}]"

    def __repr__(self):
        return f"[{self.value} {self.freq}]"

# a min heap
class heap:
    def __init__(self, list=[]):
        self.list=list
        self.list.sort(key=lambda x: x.freq)
    def push(self, node):
        self.list.append(node)
        # now sort by freq
        self.list.sort(key=lambda x: x.freq)
    def pop(self):
        return self.list.pop(0)


class huffman_encoding:
    def __init__(self):
        self.encoding = {}
        self.decoding = {}

    def build_tree(self, freq):
        # create a min heap
        h = heap(freq)
        while(len(h.list)>1):
            # pop two nodes
            n1 = h.pop()
            n2 = h.pop()
            # create a new node with freq = sum of freq of n1 and n2
            n3 = node(None, n1.freq+n2.freq)
            # make n1 and n2 as left and right child of n3
            n3.left = n1
            n3.right = n2
            # push n3 to heap
            h.push(n3)
        # return the last node in heap

        # create the encoding
        self.tree = h.pop()
        self.buildEncoding(self.tree)

    def buildEncoding(self, node, code=""):
        if(node.left == None and node.right == None):
            self.encoding[node.value] = code
            self.decoding[code] = node.value
        else:
            self.buildEncoding(node.left, code+"0")
            self.buildEncoding(node.right, code+"1")

    def encode(self, value):
        return self.encoding[value]

    def decode(self, code):
        return self.decoding[code]



# return list of nodes with value and freq
    def freq(self,list):
        freq = {}
        for i in list:
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1
        # return freq
        freq = [node(i, freq[i]) for i in freq]
        return freq

if __name__ == '__main__':
    img = [
        [7,7,3,1,1],
        [6,2,3,1,1],[4,3,0,0,7],[3,4,3,3,4],[5,5,6,2,2]
    ]
    
    h= huffman_encoding()
    f= h.freq([i for j in img for i in j])
    
    print("Frequency list :",f)
    h.build_tree(f)
    print("Encodede_dict :",h.encoding)
    
    encoded_img=[]
    for i in img:
        row=[]
        for j in i:
            row.append(h.encode(j))
        encoded_img.append(row)
    print("Encoded Image : ",encoded_img)
    
    decode_img=[]
    for i in encoded_img:
        row=[]
        for j in i:
            row.append(h.decode(j))
        decode_img.append(row)
    print("Decoded_image : ",decode_img)