import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

def image_convert(url,threshold):
    img = plt.imread(url)
    #convert to gray_scale image by calculating the mean value for RGB value
    gray_img = np.mean(img,axis=2)
    #if>threshold, then white, otherwise black
    binary_img = np.where(gray_img > threshold,255,0).astype(np.uint8)
    return binary_img

url = "004.jpg"
binary = image_convert(url,200)
binary_img = Image.fromarray(binary)
current_directory = os.path.dirname(os.path.realpath(__file__))
binary_img.save(os.path.join(current_directory,'binary_image.jpg'))
