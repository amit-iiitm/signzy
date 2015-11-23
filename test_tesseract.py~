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

image_file='name_extracted.tif'
im=Image.open(image_file)
imw=im.size[0]
imh=im.size[1]
print imw, imh
text = pytesseract.image_to_string(im)
print "=====output=======\n"
print text
