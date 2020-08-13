import csv
import pandas as pd
import numpy as np
import math
import glob
import os
import shutil
import time
import cv2
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def float2bin(value, bits):
    # Converts in64 to bin64
    bina = np.binary_repr(value, width= bits)
    return bina

def check_bit(bina, bit):
    # Checks if certain bit in the binary is set to 1
    setting = bina[bit]=='1'
    return setting

def smooth(y):
    # Smoothes a signal
    ysmooth=savgol_filter(y, window_length=21, polyorder=0)
    return ysmooth

def gradient(emission):
    # gradient of a signal is calculated
    grad=np.gradient(emission)
    return grad


def makevid(imagefolder, Path):
    # from the images in the subfolders, videos are created
    os.chdir(imagefolder)
    img_array = []

    for filename in glob.iglob('*.tif'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    try:
        name= os.path.split(imagefolder)[1] +  'vid.avi'
        out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'DIVX'), 18, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
    except:
        pass
    

    for filename in glob.iglob('*.avi'):
        shutil.move(str(imagefolder+os.sep + filename),str(Path+os.sep + filename))

def vid_copy_images(des_path, path, classes):
    # The images (im-names) are copied in subfolders containing 5 images
    im_names= os.listdir(str(path + os.sep + classes))
    for i in range(5,len(im_names)):
        pathpath= des_path + os.sep  + classes + os.sep + str(i) 
        try:
            os.makedirs(pathpath)
        except:
            pass
        filename4= im_names[i]
        filename3= im_names[i-1]
        filename2= im_names[i-2]
        filename1= im_names[i-3] 
        filename0= im_names[i-4] 
        opath4=str(path) + os.sep + classes + os.sep + str(filename4)
        opath3=str(path) + os.sep + classes + os.sep +str(filename3)
        opath2=str(path) + os.sep +classes + os.sep + str(filename2)
        opath1=str(path) + os.sep + classes + os.sep +str(filename1)
        opath0=str(path) + os.sep + classes + os.sep +str(filename0)
        shutil.copy(opath4, (pathpath+ os.sep + str(filename4)))
        shutil.copy(opath3, (pathpath+ os.sep + str(filename3)))
        shutil.copy(opath2, (pathpath+ os.sep + str(filename2)))
        shutil.copy(opath1, (pathpath+ os.sep + str(filename1)))
        shutil.copy(opath0, (pathpath+ os.sep + str(filename0)))
    

def copy_images(im_names, des_path, path, classes):
    #images are copied to a the class folder
    cpath= str(des_path + os.sep + classes)
    try:
        os.makedirs(cpath)
    except:
        pass
    for i in range(len(im_names)):
        try:
            filename= str(0) + str(0)+ im_names[i] + os.extsep + 'tif'
            opath=str(os.path.split(path)[0] + os.sep + 'images' + os.sep + 'TcProcessLightImage' + os.sep + filename)
            shutil.copy(opath, cpath + os.sep +  str(filename))
        except:
            pass
        try:
            filename= str(0)+ str(0) + str(0)+ im_names[i] + os.extsep + 'tif'
            opath=str(os.path.split(path)[0] + os.sep + 'images' + os.sep + 'TcProcessLightImage' + os.sep + filename)
            shutil.copy(opath, cpath + os.sep +  str(filename))
        except:
            pass
        try:
            filename= str(0) + str(0)+ str(0) + str(0)+ im_names[i] + os.extsep + 'tif'
            opath=str(os.path.split(path)[0] + os.sep + 'images' + os.sep + 'TcProcessLightImage' + os.sep + filename)
            shutil.copy(opath, cpath + os.sep +  str(filename))
        except:
            pass

       

def getPOCI(path, position):
    #image list PO and CI is created
    imp_csv = pd.read_csv(path, sep=';', encoding= 'utf8',
        usecols=['TcEinstellmass', 'TcFrameID', 'TcLaserPowerSet',
            'm_cuttingState.m_controlFeedVelocity.m_cuttingState',
            'TcSHActualExpTimeF2Set',
            'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission'], 
        dtype={'TcEinstellmass':np.int16, 'TcFrameID':float,
            'TcSHActualExpTimeF2Set':np.int16,
            'm_cuttingState.m_controlFeedVelocity.m_cuttingState':np.int64, 
            'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission':np.int16,}, 
        skiprows=[1,2],
        decimal=',')
    names=[]
    einstechen=[]
    emission=[]
    for i in range(len(imp_csv)):
        cs= imp_csv.iat[i,4]
        bcs= float2bin(cs, 64) #Convert to 64bit
        emission.append(imp_csv.iat[i,5])
        einstechen.append(check_bit(bcs, 55))
        names.append(str(math.trunc(imp_csv.iat[i,0]))) #Image Name
    #the signal emission is smoothed
    emismooth = smooth(emission)
    #the gardient of the emission is calculated
    grad = gradient(emismooth)
    plt.plot(emismooth)
    plt.plot(grad)
    plt.show()

    im_PO=[]
    im_CI=[]
    laservalue= imp_csv.iloc[:,[2]].max()
    laservalue= laservalue[0]
    #Now the three classes are created PO CO CI
    for i in range(0,position):
        if imp_csv.iat[i,2] == laservalue and einstechen[i]==False and emission[i] > 15:
            im_PO.append(names[i])
    for i in range(position, len(names)):
        if imp_csv.iat[i,2] == laservalue and einstechen[i]==False and emission[i] > 15:
            im_CI.append(names[i])
    return im_CI, im_PO


#Change Pathnames
path = 'F:/Test_Sequenzen/ST040-N2H0/5_ST040-N2H0_Rampe100-130_Pq70/data.csv' #Path to Data.csv
des_path= 'C:/TW565le/Uebergabe_test/RCNN/images' #Path were single images are saved, can be deleted in the end
vidpath= 'C:/TW565le/Uebergabe_test/RCNN/videos'
PathPO='C:/TW565le/Uebergabe_test/RCNN/videos/PO'
PathCI='C:/TW565le/Uebergabe_test/RCNN/videos/CI'

try:
    os.makedirs(des_path)
except:
    pass
#Change the Position of CI
position=1100
im_CI, im_PO= getPOCI(path, position)
# Copy single images
copy_images(im_CI, des_path, path, 'CI')
copy_images(im_PO, des_path, path, 'PO')
# Copy always 5 images together
vid_copy_images(vidpath, des_path, 'CI')
vid_copy_images(vidpath, des_path, 'PO')
#make videos PO
changedir = os.listdir(PathPO)
ifPO=[]
for i in range(0, len(changedir)):
    imagefolder= str(PathPO + os.sep + changedir[i])
    ifPO.append(imagefolder)
    makevid(imagefolder, PathPO)

# deletes the created folders, if multiplication is desired, comment out
try:
    for i in range(len(ifPO)):
        shutil.rmtree(ifPO[i])
except:
    pass
#make videos CI
changedir = os.listdir(PathCI)
ifCI=[]
for i in range(0, len(changedir)):
    imagefolder= str(PathCI + os.sep + changedir[i])
    ifCI.append(imagefolder)
    makevid(imagefolder, PathCI)
# deletes the created folders, if multiplication is desired, comment out
try:
    for i in range(len(ifCI)):
        shutil.rmtree(ifCI[i])
except:
    pass

# To delete the created image folder
shutil.rmtree(des_path)
