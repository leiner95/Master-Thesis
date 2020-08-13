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



def copy_images(im_names, des_path, path, classes):
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
        steg= check_bit(bdi, 62)

    laservalue= imp_csv.iloc[:,[2]].max()
    laservalue= laservalue[0]
    #the signal emission is smoothed
    emismooth = smooth(emission)
   
    #the gardient of the emission is calculated
    grad = gradient(emismooth)

    plt.plot(emismooth)
    plt.plot(grad)
    plt.show()


    im_PO=[]
    im_CI=[]
    #Now the three classes are created PO CO CI
    for i in range(0,position):
        if imp_csv.iat[i,2] == laservalue and einstechen[i]==False and emission[i] > 15:
            im_PO.append(names[i])
    for i in range(position, len(names)):
        if imp_csv.iat[i,2] == laservalue and einstechen[i]==False and emission[i] > 15:
            im_CI.append(names[i])
    return im_CI, im_PO



path = 'F:/Test_Sequenzen/ST040-N2H0/0_ST040-N2H0_Rampe100-130_Standard/data.csv' #Pfad zur Data.csv
des_path= 'C:/TW565le/Uebergabe_test/CNN/images'
try:
    os.makedirs(des_path)
except:
    pass
#Adapt Position
position=435

im_CI, im_PO= getPOCI(path, position)

copy_images(im_CI, des_path, path, 'CI')
copy_images(im_PO, des_path, path, 'PO')

