#reading name and date of birth from image of pan card
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

'''Notations used
   imw= image width
   imh= image height
   im.size[0] gives width of image
   im.size[1] gives height of image
'''


#binarization of image using global thresholding
def GBinarization(image,th):
  im=Image.open(image)
  im=im.convert('L')
  imw= im.size[0]
  imh= im.size[1]
  print imw
  print imh
  pix=im.load()
  hs=im.histogram()
  """th=0
  if th==-1:
   for i in range(len(hs)):
    th+=i*int(hs[i])
  th=th/(imw*imh)"""
 
  for i in range(imh):
    for j in range(imw):
        if pix[j,i]<th :
           im.putpixel((j,i),0)
        else :
	   im.putpixel((j,i),255)
  im.show()
  im.save('Image2_binarize.jpg')
  print pix
  return im
################################################################################################################

GBinarization('Image2.jpg',110)

def crop_pancard(im):
  im=im.convert('L')
  imw= im.size[0]
  imh= im.size[1]
  print imw
  print imh
  pix=im.load()
  start=0
  flag=0
  end=imh
  flag1=0
  flag2=0
  flag3=0
  left=imw
  right=0
       
  for i in range(1,imh):
      for j in range(1,imw):
         if (pix[j,i]!=255):
            flag=1
         if (flag==1):
            start=i
            break
      if (flag==1):
         break
       
  '''
  for i in range(imh-50,imh-49):
     for j in range(1,imw):
         print pix[i,j]
  '''
  for i in range(imh-1,0,-1):
      for j in range(1,imw):
          if (pix[j,i]!=255):
             flag1=1
          if (flag1==1):
             end=i
             break
      if(flag1==1):
         break
     
  for i in range(1,imh):
      flag2=0
      for j in range(1,imw):
          if (pix[j,i]!=255):
             flag2=1
             left=min(left,j)
             break
                  
  for i in range(imh-1,0,-1):
       flag3=0
       for j in range(imw-1,0,-1):
          if (pix[j,i]!=255):
             flag3=1
          if (flag3==1):
             right=max(right,j)
             break
  #print left 
  #print start
  #print right
  #print end
  box=(left,start,right,end)
  im=im.crop(box)
  im.show()
  im=im.resize((400,240),Image.ANTIALIAS)
  im.save('Image2_cropped.jpg')

crop_pancard(Image.open('Image2_binarize.jpg'))

#till now got the pancard from whole image and binarized it 
#first the task is to get the name

def locate_name(im):
  im=im.convert('L')
  imw= im.size[0]
  imh= im.size[1]
  print imw
  print imh
  pix=im.load()
  
