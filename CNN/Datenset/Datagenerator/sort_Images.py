import csv
import pandas as pd
import numpy as np
import math
from scipy.signal import savgol_filter


def float2bin(value, bits):
    bina = np.binary_repr(value, width= bits)
    return bina

def check_bit(bina, bit):
    setting = bina[bit]=='1'
    return setting

def smooth(y):
    ysmooth=savgol_filter(y, window_length=21, polyorder=4)
    return ysmooth

def gradient(emission):
    grad=np.gradient(emission)
    return grad

def threshold(grad, im_names):
    max_value= np.amax(grad)
    index= np.where(grad == max_value)
    index= index[0][0]
    return index, max_value

def moveDir(imp_csv, DIR):
    x0=0
    DIR.append(x0)
    for i in range(1,len(imp_csv)):
        xi=imp_csv.iat[i,1]
        xii=imp_csv.iat[(i-1),1]
        x= xi-xii
        yi=imp_csv.iat[i,2]
        yii=imp_csv.iat[(i-1),2]
        y= yi-yii
        if x in range(-10,10):
            movey=np.arctan(xi/y)
            dmovey=int(np.degrees(movey))
            DIR.append(dmovey)
        elif y in range(-10,10):
            movex=np.arctan(x/yi)
            dmovex=int(np.degrees(movex))
            DIR.append(dmovex)
        else:
            DIR.append('curve')
    return DIR

   

def noblackim(im_names, emission, emissionfactor, im_names_proc):
    for i in range(0, len(im_names)):
        if emission[i] > emissionfactor:
                image = str(math.trunc(im_names[i]))
                im_names_proc.append(image)
        else:
            continue
    return im_names_proc

def csv(path, cond_list, cond_type):
    imp_csv = pd.read_csv(path, sep=';', encoding= 'utf8',
        usecols=[cond_list], 
        dtype={cond_type}, 
        skiprows=[1,2],
        decimal=','
        )
    return imp_csv

def sort_images_CI(path):
    try:
        imp_csv = pd.read_csv(path, sep=';', encoding= 'utf8',
            usecols=['TcEinstellmass', 'TcFrameID', 'TcLaserPowerSet', 'TcActualXPosition', 'TcActualYPosition',
                'm_cuttingState.m_controlFeedVelocity.m_cuttingState',
                'TcSHActualExpTimeF2Set',
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission', 
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_resultState'], 
            dtype={'TcEinstellmass':np.int16, 'TcFrameID':float,
                'TcActualXPosition':np.int32, 'TcActualYPosition':np.int32,
                'TcSHActualExpTimeF2Set':np.int16,
                'm_cuttingState.m_controlFeedVelocity.m_cuttingState':np.int64, 
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission':np.int16, 
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_resultState':np.int32}, 
            skiprows=[1,2],
            decimal=',')
        #print('csv', imp_csv.iloc[0])
        # TCFrame ID : imp_csv.iat[,0]
        # cuttingstate : imp_csv.iat[,1]
        # emission : imp_csv.iat[,2]

        im_names=[]
        emission=[]
        bin_cutting_state=[]
        laser_power=[]
        lp_PO=[]
        lp_CI= []
        imgpath=[]
        imgpath_CI=[]
        imgpath_PO=[]
        esm=[]
        esm_CI=[]
        esm_PO=[]
        LIGHT=[]
        LIGHT_PO=[]
        LIGHT_CI=[]
        DIR=[]
        DIR_CI=[]
        DIR_PO=[]
        im_names_PO=[]
        im_names_CI=[]

        #Cutting State value to binary
        for i in range(0,len(imp_csv)): 
            cs= imp_csv.iat[i,6]
            bcs= float2bin(cs, 64)
            di= imp_csv.iat[i,8]
            bdi= float2bin(di, 64)

            # parameter for 'good', HC images
            process_undefined= check_bit(bcs, 16)
            start= check_bit(bcs, 62)
            laser=check_bit(bcs, 56)
            einstechen= check_bit(bcs, 55)
            beam= check_bit(bcs, 60)
            steg= check_bit(bdi, 62)
            if start == False and laser == False and einstechen==False and steg==False and process_undefined == False and beam == False: 
                im_n = imp_csv.iat[i,0]
                emi = imp_csv.iat[i,7]
                laserp = imp_csv.iat[i,4]
                ESM= imp_csv.iat[i,3]
                light = imp_csv.iat[i,5]
                emission.append(emi)
                im_names.append(im_n)
                laser_power.append(laserp)
                imgpath.append(path)
                esm.append(ESM)
                LIGHT.append(light)
            else:
                continue
        DIR = moveDir(imp_csv, DIR)
        # Parameter to devide between CI and PO
        emismooth = smooth(emission)
        grad = gradient(emismooth)
        index, max_value = threshold(grad, im_names)

        sfactor_CO= int(len(im_names)/100*3)
        sfactor_PO= int(len(im_names)/100*10)
   

        for i in range(0,index-sfactor_PO):
            if emission[i] > 1:
                image = str(math.trunc(im_names[i]))
                lp = laser_power[i]
                lp_PO.append(lp)
                im_names_PO.append(image)
                im_path_PO = imgpath[i]
                imgpath_PO.append(im_path_PO)
                esm_PO.append(esm[i])
                LIGHT_PO.append(LIGHT[i])
                DIR_PO.append(DIR[i])
            else:
                continue
    
        for i in range(index+sfactor_CO, len(im_names)):
            if emission[i] > 150:
                image = str(math.trunc(im_names[i]))
                im_names_CI.append(image)
                lp = laser_power[i]
                lp_CI.append(lp)
                im_path_CI = imgpath[i]
                imgpath_CI.append(im_path_CI)
                esm_CI.append(esm[i])
                LIGHT_CI.append(LIGHT[i])
                DIR_CI.append(DIR[i])
            else:
                continue
    except: 
        print('error', path)
        lp_PO=[]
        lp_CI= []
        imgpath=[]
        imgpath_CI=[]
        imgpath_PO=[]
        esm_CI=[]
        esm_PO=[]
        LIGHT_PO=[]
        LIGHT_CI=[]
        DIR_CI=[]
        DIR_PO=[]
        im_names_PO=[]
        im_names_CI=[]
    return im_names_PO, im_names_CI, lp_CI, lp_PO, imgpath_CI, imgpath_PO, esm_CI, esm_PO, LIGHT_CI, LIGHT_PO, DIR_CI, DIR_PO

def sort_images_HC(path):
    try:
        imp_csv = pd.read_csv(path, sep=';', encoding= 'utf8',
            usecols=['TcEinstellmass', 'TcFrameID', 'TcLaserPowerSet',
                'TcSHActualExpTimeF2Set', 'TcActualXPosition', 'TcActualYPosition',
                'm_cuttingState.m_controlFeedVelocity.m_cuttingState', 
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission', 
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_resultState'], 
            dtype={'TcEinstellmass':np.int16 ,'TcFrameID':float,
                'TcSHActualExpTimeF2Set':np.int16,'TcActualXPosition':np.int32, 'TcActualYPosition':np.int32,
                'm_cuttingState.m_controlFeedVelocity.m_cuttingState':np.int64,
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_rawImg_amountOfProcessEmission':np.int16,
                'm_cuttingState.m_controlFeedVelocity.m_imageProc.m_results.m_resultState':np.int32}, 
            skiprows=[1,2],
            decimal=',')

        # TCFrame ID : imp_csv.iat[,0]
        # cuttingstate : imp_csv.iat[,1]
        # emission : imp_csv.iat[,2]

        im_names=[]
        im_names_HC=[]
        emission=[]
        bin_cutting_state=[]
        laser_power=[]
        lp_HC=[]
        imgpath=[]
        imgpath_HC=[]
        esm=[]
        esm_HC=[]
        LIGHT=[]
        LIGHT_HC=[]
        DIR=[]
        DIR_HC=[]

        #Cutting State value to binary
        for i in range(0,len(imp_csv)): 
            cs= imp_csv.iat[i,6]
            bcs= float2bin(cs, 64)
            di= imp_csv.iat[i,8]
            bdi= float2bin(di, 64)

            # parameter for 'good', HC images
            process_undefined= check_bit(bcs, 16)
            start= check_bit(bcs, 62)
            laser=check_bit(bcs, 56)
            einstechen= check_bit(bcs, 55)
            beam= check_bit(bcs, 60)
            steg= check_bit(bdi, 62)
            if start == False and laser == False and einstechen==False and steg==True and process_undefined == False and beam == False: 
                im_n = imp_csv.iat[i,0]
                emi = imp_csv.iat[i,7]
                laserp = imp_csv.iat[i,4]
                ESM= imp_csv.iat[i,3]
                light = imp_csv.iat[i,5]
                emission.append(emi)
                im_names.append(im_n)
                laser_power.append(laserp)
                imgpath.append(path)
                esm.append(ESM)
                LIGHT.append(light)
            else:
                continue
        DIR = moveDir(imp_csv, DIR)

        for i in range(0, len(im_names)):
            if emission[i] > 1:
                    image = str(math.trunc(im_names[i]))
                    im_names_HC.append(image)
                    lp_HC.append(laser_power[i])
                    imgpath_HC.append(imgpath[i])
                    esm_HC.append(esm[i])
                    LIGHT_HC.append(LIGHT[i])
                    DIR_HC.append(DIR[i])
            else:
                continue

    except:
        print('error', path)
        im_names_HC=[]
        lp_HC=[]
        imgpath_HC=[]
        esm_HC=[]
        LIGHT_HC=[]
        DIR_HC=[]
    
    
    return im_names_HC, lp_HC, imgpath_HC, esm_HC, LIGHT_HC, DIR_HC
