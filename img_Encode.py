import cv2
import numpy as np
import types
import tkinter as tk
from tkinter import filedialog

def ToBinary(text):      # convert the input data to binary form
    if type(text)==str:
        return ''.join([format(ord(i),"08b") for i in text])
    elif type(text)== bytes or type(text)==np.ndarray:
        return [format(i,"08b")for i in text]
    elif type(text)== int or type(text)== np.uint8:
        return format(text,"08b")
    else:
        raise TypeError("Input type not supported ")

def Encode_data(image,input_text):
    no_bytes=image.shape[0] * image.shape[1] * 3 // 8
    if(len(input_text)>no_bytes):
        raise ValueError("Insufficient Bytes, provide large image or less data.")
    input_text += "$t3g@" # string works as end point and secret key to encode and decode data
    data_indx=0
    bin_input_txt=ToBinary(input_text)
    txt_len=len(bin_input_txt)
    for val in image:
        for pix in val:
            r,g,b=ToBinary(pix)
            if data_indx<txt_len:
                pix[0]=int(r[:-1]+bin_input_txt[data_indx],2) # hide the data into LSB of red pixel
                data_indx += 1
            if data_indx<txt_len:
                pix[1]=int(g[:-1]+bin_input_txt[data_indx],2) # hide the data into LSB of green pixel
                data_indx += 1
            if data_indx<txt_len:
                pix[2]=int(b[:-1]+bin_input_txt[data_indx],2) # hide the data into LSB of blue pixel
                data_indx += 1
            if data_indx >=txt_len:
                break

    return image                    

def start_encode():
    root=tk.Tk()
    root.withdraw()
    img=filedialog.askopenfilename(title='Select image File in .PNG format ') # open's browse file window
    image=cv2.imread(img)
    data=input("Enter data to be encoded ") # user input data
    if len(data)==0:
        raise ValueError('Data is empty')

    filename=input("Save file in .PNG format ")
    encoded_img=Encode_data(image,data)
    cv2.imwrite(filename,encoded_img) # file saved in current directory 

start_encode()    


