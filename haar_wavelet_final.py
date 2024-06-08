import cv2
import numpy as np
from Huffman_alg import huffman_encoding
# Load an image
image = cv2.imread('wolf.jpg', cv2.IMREAD_GRAYSCALE)  # Load the image in grayscale
# Haar Wavelet transformation
class Haar_Decomposition:
    def __init__(self,data,block_size):
        self.data = data
        self.block_size = block_size
    
    def haar_transform(self,block):
        
        rows,cols = block.shape 
        iteration = int(np.log2(rows))
        transformed_block = np.zeros((rows,cols),dtype = 'float64')
        
        for itter in range(iteration):
            # row-wise transformation
            r = rows//(2**itter)
            c = cols//(2**(itter))
            for i in range(r):
                row = block[i][:c]
                updated_row = np.zeros(len(row))
                k = len(row)//2
                t = 0
                j = 0
                while j<len(row):
                    updated_row[t] = (row[j]+row[j+1])/2
                    # print(t,j)
                    updated_row[t+k] = row[j]-updated_row[t]
                    j = j + 2
                    t = t + 1
                row  = updated_row
                transformed_block[i][:c] = row
            
            # print(transformed_block)
            # column-wise transformation
            c = cols//(2**(itter+1))
            for j in range(c):
                colm = transformed_block[:r,j]
                # print(colm)
                updated_colm = np.zeros(len(colm))
                k = len(colm)//2
                t = 0
                m = 0
                while m<len(colm):
                    updated_colm[t] = (colm[m]+colm[m+1])/2
                    # print(t,j)
                    updated_colm[t+k] = colm[m]-updated_colm[t]
                    m = m + 2
                    t = t + 1
                colm  = updated_colm
                transformed_block[:r,j] = colm
                
            block = transformed_block
        return block
    
    def quantization(self,block):
        quantization_step = 16
        quantized_block = np.round(block / quantization_step).astype(np.int32)
        return quantized_block

    def transformed_data(self):
        image_row,image_col = self.data.shape
        num_blocks_row = image_row // self.block_size
        num_blocks_col = image_col // self.block_size
        transformed_blocks = []
        for i in range(num_blocks_row):
            for j in range(num_blocks_col):
                block = self.data[i*self.block_size:(i+1)*self.block_size, j*self.block_size:(j+1)*self.block_size]
                transformed_block = self.haar_transform(block)
                quantized_block = self.quantization(transformed_block)
                transformed_blocks.append(quantized_block)
                
        return transformed_blocks
    
patch_size = 4
obj = Haar_Decomposition(image, patch_size)
transformed_image = obj.transformed_data()
encoded_strings = []
Decoded_image = []
bits = []
for img in transformed_image:

    h= huffman_encoding()
    f= h.freq([i for j in img for i in j])
    
    # print("Frequency list :",f)
    h.build_tree(f)
    Encodede_dict = h.encoding
    bit = 0
    for key,value in zip(Encodede_dict.keys(),Encodede_dict.values()):
        if value != '':
            bit = bit + int(key)*(int(value)/(patch_size**2))
        
    bits.append(bit)
    
    
    encoded_string = ''
    for string in Encodede_dict.values():
        encoded_string += string
        
    encoded_img=[]
    for i in img:
        row=[]
        for j in i:
            row.append(h.encode(j))
        encoded_img.append(row)
    # print("Encoded Image : ",encoded_img)
    
    decode_img=[]
    for i in encoded_img:
        row=[]
        for j in i:
            row.append(h.decode(j))
        decode_img.append(row)
    # print("Decoded_image : ",decode_img)
    Decoded_image.append(decode_img)
    encoded_strings.append(encoded_string)
            
    
    
    
Decoded_image = np.array(Decoded_image)
encoded_strings = np.array(encoded_strings)
bits = np.array(bits)
original_bits = (patch_size**2)*(len(transformed_image))*8
reduced_bits = np.sum(bits)
compression_ratio = original_bits/reduced_bits
print(compression_ratio)
#compression_ratio = ( reduced_bits)/original_bits