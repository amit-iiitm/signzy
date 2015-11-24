from PIL import Image
import ImageEnhance
import ImageFilter
import ImageOps,ImageChops
import scipy
import numpy as np
from scipy import ndimage
from scipy.misc import imsave
from numpy import ndarray
import matplotlib.pyplot as plt
import time
import os
from pytesseract import *


#tesseract fails to give the string correctly when a single character image is given it also does not recognises when a strip of name region is given at best i when i give the binarized cropped image of pan card then it recognises some of the strings


#giving single character
image_file='N.tif'
im=Image.open(image_file)
imw=im.size[0]
imh=im.size[1]
print imw, imh
pix=im.load()
#simple binarization
for k in range(imw):
   for j in range(imh):
       if pix[k,j]<110:
          im.putpixel((k,j),0)
       else:
          im.putpixel((k,j),255)
text = pytesseract.image_to_string(im)
print "=====output_character=======\n"
print text

#giving the name strip
image_file1='name_extracted.tif'
im1=Image.open(image_file1)
imw1=im1.size[0]
imh1=im1.size[1]
print imw1, imh1
pix=im1.load()
#simple binarization
for k in range(imw1):
   for j in range(imh1):
       if pix[k,j]<110:
          im1.putpixel((k,j),0)
       else:
          im1.putpixel((k,j),255)
text1 = pytesseract.image_to_string(im1)
print "=====output_namestrip=======\n"
print text1


#giving the binarized pan card
image_file2='Image2_cropped.tif'
im2=Image.open(image_file2)
imw2=im2.size[0]
imh2=im2.size[1]
print imw2, imh2
pix=im2.load()
#simple binarization
for k in range(imw2):
   for j in range(imh2):
       if pix[k,j]<110:
          im2.putpixel((k,j),0)
       else:
          im2.putpixel((k,j),255)
text2 = pytesseract.image_to_string(im2)
print "=====output_binarized_card=======\n"
print text2

#to get the text i tried 3 different portions of image but tesseract fails to give correct results It would require some more time for setting up tesseract appropriately. The other option is as already suggested to use a trained classifier that can classify between our characters but for that we need a training dataset with images of characters and labels.
