import cv2
import numpy as np
import types
import tkinter as tk
from tkinter import filedialog

def ToBinary(text):
    if type(text)==str:
        return ''.join([format(ord(i),"08b") for i in text])
    elif type(text)== bytes or type(text)==np.ndarray:
        return [format(i,"08b")for i in text]
    elif type(text)== int or type(text)== np.uint8:
        return format(text,"08b")
    else:
        raise TypeError("Input type not supported ")

def Decode_data(image):
    bin_data=""
    for val in image:
        for pix in val:
            r,g,b=ToBinary(pix)
            bin_data+=r[-1]  #extracting data from the LSB of red pixel
            bin_data+=g[-1]  #extracting data from the LSB of green pixel
            bin_data+=b[-1]  #extracting data from the LSB of blue pixel

    data_bytes=[bin_data[i:i+8] for i in range(0,len(bin_data),8)]
    decoded_data=""
    for byte in data_bytes:
        decoded_data+=chr(int(byte,2))
        if decoded_data[-5:]=="$t3g@":  # string works as end point and secret key to encode and decode data
            break
    return decoded_data[:-5]            

def start_decode():
    root=tk.Tk()
    root.withdraw()
    img=filedialog.askopenfilename(title='Select PNG image File to decode')  # open's browse file window
    image=cv2.imread(img)
    txt=Decode_data(image)
    print(txt) # decoded text

start_decode()    