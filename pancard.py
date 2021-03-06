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
import os


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

#GBinarization('Image2.jpg',110)

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

#crop_pancard(Image.open('Image2_binarize.jpg'))

#till now got the pancard from whole image and binarized it 
#first the task is to get the name

##################################################################################
def DetermineY(img):
 imw=img.size[0]
 imh=img.size[1]
 pix=img.load()
 thd=150
 insideImg=0
 count1=0
 count2=0
 EdgCount = ndarray((imh,),int)
 for i in range(imh):
   EdgCount[i]=0
   for j in range((imw/2)-1):
      if  abs(pix[j,i]-pix[j+1,i])>thd :
         EdgCount[i]+=1
   #print ("%d : %d"%(i,EdgCount[i]))
 return EdgCount
###################################################################################

def locate_name(im):
  im=im.convert('L')
  imw= im.size[0]
  imh= im.size[1]
  print imw
  print imh
  pix=im.load()
  imw=im.size[0]
  imh=im.size[1]
  pix=im.load()
  #simple binarization
  for k in range(imw):
     for j in range(imh):
         if pix[k,j]<110:
            im.putpixel((k,j),0)
         else:
            im.putpixel((k,j),255)
  #determine the row number i.e. Y axis points which have maximum heuristic measure 
  #heuristic measure is chosen to be the number of edges i.e. the sharp change in intensity value from one pixel to another
  X=ndarray((imh,),int)
  for i in range(imh):
     X[i]=i
  #print X
  Y=DetermineY(im)
  #print Y
  for i in range(imh):
     print X[i],  Y[i]
  plt.plot(X,Y)
  plt.show()
  #plot the edges against line no. to get a feel of peaks observed 
  #get the strip of name of person using geometrical analysis we observe that for a size 0f 240 vector the row containing name is after the 55th row
  #for locating the date of birth we need to change this threshold to 100
  start=0
  end=0
  for i in range(55,imh):
     if Y[i]>=5:
	start=i
	break;
  for i in range(start,imh):
     if Y[i]==0:
	end=i
	break;
  print "printing the borders of the name"
  print start, end
  box=(10,start-2,150,end+2)
  im=im.crop(box)
  #im=im.resize((100,20),Image.ANTIALIAS)
  im.save('name_extracted.jpg')
  im.show()
#locate_name(Image.open('Image2_cropped.jpg'))


#locate_name gives the strip containing the name of person now i need to perform a connected component approach to get the individual characters in a single frame for recognition
lf=1000
rt=-1
up=1000
dn=-1
def find_char(x,y,pix,col,im):
   global lf
   lf=1000
   global rt
   rt=-1
   global up
   up=1000
   global dn
   dn=-1
   findchar(x,y,pix,col,im)
   imw=im.size[0]
   imh=im.size[1]
   box = (max(0,lf),max(0, up), min(imw,rt), min(imh,dn))
   #box = (max(0,lf),max(0,0), min(imw,rt), min(imh,imh))
   imnw=im.crop(box)
   #if imw*0.1 >rt-lf>10 and  imh*0.9>dn-up>20:
   imnw.show()
   return imnw
   #else  :
   #  return -1

def findchar(x,y,pix,col,im):
   col[x,y]=1
   imw=im.size[0]
   imh=im.size[1]
   global lf
   lf=min(x,lf)
   global up
   up=min(up,y)
   global rt
   rt=max(rt,x)
   global dn
   dn=max(dn,y)
   if(x>0 and col[x-1,y]==0 and pix[x-1,y]==0):
       findchar(x-1,y,pix,col,im)
   if(y>0 and col[x,y-1]==0 and pix[x,y-1]==0):
       findchar(x,y-1,pix,col,im)
   if(x<imw-1 and col[x+1,y]==0 and pix[x+1,y]==0):
       findchar(x+1,y,pix,col,im)
   if(y<imh-1 and col[x,y+1]==0 and pix[x,y+1]==0):
       findchar(x,y+1,pix,col,im)

#segmentation part
def segment_char(im):
  imw=im.size[0]
  imh=im.size[1]
  pix=im.load()
  #simple binarization
  for k in range(imw):
     for j in range(imh):
         if pix[k,j]<110:
            im.putpixel((k,j),0)
         else:
            im.putpixel((k,j),255)
  im.show()
  imnew=im.copy()
  col=ndarray((imw,imh),int)
  count_black=0
  for j in range(imw):
      for m in range(imh):
          col[j,m]=0
	  print pix[j,m]
          if pix[j,m]==0:
		count_black+=1
          imnew.putpixel((j,m),255)
  print "printing the no. of black pixels", count_black
  m=imh/2
  imlist=[]
  for j in range(imw):
       if pix[j,m]==0 and col[j,m]==0 :
              imlist.append(find_char(j,m,pix,col,im))
              
  i="name_segment"
  j=0
  for pic in imlist:
       dest=str(i)+"/"
       if not os.path.exists(dest):
           os.makedirs(dest)
       try:
        pic.save(dest+str(j)+".jpg")
       except:
        continue
       j+=1
segment_char(Image.open('name_extracted.jpg'))

#till now got the segmented image of individual characters"""


#For the recognition of individual characters i tried tresseract but it failed after that tried another method using knn classifier with data from uci repository containing the label of images and their 14 features Training is done on that dataset but for our images we need to extract features from the character image which i cant do because of lack of time. Future scope includes extracting these features and then classifying them using knn or svm classifier. The details of features are specified in opencv_knn.py file

