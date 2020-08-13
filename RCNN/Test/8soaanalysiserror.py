from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as pd
from numpy import asarray
import matplotlib.pyplot as plt
from PIL import Image
import math
from pathlib import Path
import os
import glob
from keras_video import VideoFrameGenerator



def float2bin(value, bits):
    bina = np.binary_repr(value, width= bits)
    return bina

def check_bit(bina, bit):
    setting = bina[bit]=='1'
    return setting

def SOA(path, trainpath):
    listeSOA=[]
    imp_csv = pd.read_csv(path, sep=';', encoding= 'utf8',
                usecols=['TcFrameID',
                    'm_cuttingState.m_controlFeedVelocity.m_cuttingState'], 
                dtype={'TcFrameID':float, 'm_cuttingState.m_controlFeedVelocity.m_cuttingState':np.int64}, 
                skiprows=[1,2],
                decimal=',')
    for i in range(len(imp_csv)):
        cs= imp_csv.iat[i,1]
        bcs= float2bin(cs, 64)
        ss= check_bit(bcs, 35)
        searchfor= '*'+str(math.trunc(imp_csv.iat[i,0]))+'*'
        for path in Path(trainpath).rglob(searchfor):
            if ss == True:
                listeSOA.append(0)
            elif ss == False:
                listeSOA.append(1)
    return listeSOA
#Testbilder
def error(BS, globname, model):
    classes = [i.split(os.path.sep)[1] for i in glob.glob('normal/*')]
    classes.sort()
    # some global params
    SIZE = (150, 150)
    CHANNELS = 3
    NBFRAME = 5
    # pattern to get videos and classes
    glob_pattern=globname
    # Create video frame generator
    train = VideoFrameGenerator(
        classes=classes, 
        glob_pattern=glob_pattern,
        nb_frames=NBFRAME,
        #split=0.5, 
        shuffle=False,
        batch_size=BS,
        target_shape=SIZE,
        nb_channel=CHANNELS
        #transformation=none
        #use_frame_cache=True
        )
    sample_test_images, labels = next(train)
    prediction = model.predict(sample_test_images)
    class_names = ['CI', 'PO']
    #print(prediction)
    pred=[]
    pred.append(1)
    pred.append(1)
    pred.append(1)
    pred.append(1)
    pred.append(1)
    for ix in range(0,BS): 
        #for higher confidence
        '''
        if prediction[ix,1] > 0.8:
            pred.append(1)
        else:
            pred.append(0) 
        '''
        P = np.argmax(prediction[ix])
        pred.append(P)
 
    #pred.reverse()     
    return pred
### Generate error image
def eim(prediction, name, posCI, listeSOA):
    b3=2300
    b4=3300
    a3=1100
    a4=2200
    w= int(len(prediction)*300)
    o1=0
    o2=1000
    array = np.zeros([b4, w, 3], dtype=np.uint8)
    # Real Line
    array[0:o2,0:(posCI*300)] = [127, 255, 0] #PO grun1
    array[0:o2,(posCI*300):w] = [69, 139, 0] #CI grun2
    # SOA Line
    a2=0
    for i in range(len(listeSOA)):
        a1=a2
        a2= int(a1 + 300)
        
        if  listeSOA[i] == 1:
                array[a3:a4,a1:a2] = [127, 255, 0] #PO grun1
        elif listeSOA[i] == 0:
                array[a3:a4,a1:a2] = [69, 139, 0] #CI grun2

    # Prediction Line
    b2=0
    for i in range(0,len(prediction)):
        b1= b2
        b2= int(b1 + 300)
        
        if prediction[i] == 1:
            array[b3:b4,b1:b2] = [127, 255, 0] #PO grun1
        elif prediction[i] == 0:
            array[b3:b4,b1:b2] = [69, 139, 0] #CI grun2
        
    img = Image.fromarray(array, 'RGB')
    img.save(name)


model= load_model('RCNNmodel.h5')


POdir='F:/DataRCNN/Test/confusion/8/normal/PO'
CIdir='F:/DataRCNN/Test/time/8/normal/CI'
BS=len(os.listdir(CIdir)) + len(os.listdir(POdir))-5
posCI=len(os.listdir(POdir))
soatest_dir = 'F:/DataCNN/Test/confusion/8/normal'
datadir= 'F:/Test_Sequenzen/ST080-N2H0/1_ST080N2H0_Rampe100-130_Standard/data.csv'
pred = error(BS, 'normal/{classname}/*.avi', model)
listeSOA= SOA(datadir, soatest_dir)
eim(pred,'8normal.png',posCI, listeSOA)

POdir='F:/DataRCNN/Test/confusion/8/ESM/PO'
CIdir='F:/DataRCNN/Test/time/8/ESM/CI'
BS=len(os.listdir(CIdir)) + len(os.listdir(POdir))-5
posCI=len(os.listdir(POdir))
soatest_dir = 'F:/DataCNN/Test/confusion/8/ESM'
datadir= 'F:/Test_Sequenzen/ST080-N2H0/1_ST080N2H0_Rampe100-130_ESM+0.5/data.csv'
pred = error(BS, 'ESM/{classname}/*.avi', model)
listeSOA= SOA(datadir, soatest_dir)
eim(pred,'8ESM.png',posCI, listeSOA)

POdir='F:/DataRCNN/Test/confusion/8/140/PO'
CIdir='F:/DataRCNN/Test/time/8/140/CI'
BS=len(os.listdir(CIdir)) + len(os.listdir(POdir))-5
posCI=len(os.listdir(POdir))
soatest_dir = 'F:/DataCNN/Test/confusion/8/140'
datadir= 'F:/Test_Sequenzen/ST080-N2H0/3_ST080N2H0_Rampe100-130_Pq140/data.csv'
pred = error(BS, '140/{classname}/*.avi', model)
listeSOA= SOA(datadir, soatest_dir)
eim(pred,'8140.png',posCI, listeSOA)

POdir='F:/DataRCNN/Test/confusion/8/strahl/PO'
CIdir='F:/DataRCNN/Test/time/8/strahl/CI'
BS=len(os.listdir(CIdir)) + len(os.listdir(POdir))-5
posCI=len(os.listdir(POdir))
soatest_dir = 'F:/DataCNN/Test/confusion/8/strahl'
datadir= 'F:/Test_Sequenzen/ST080-N2H0/4_ST080N2H0_Rampe100-130_Strahlaußermittigkeit/data.csv'
pred = error(BS, 'strahl/{classname}/*.avi', model)
listeSOA= SOA(datadir, soatest_dir)
eim(pred,'8strahl.png',posCI, listeSOA)

POdir='F:/DataRCNN/Test/confusion/8/70/PO'
CIdir='F:/DataRCNN/Test/time/8/70/CI'
BS=len(os.listdir(CIdir)) + len(os.listdir(POdir))-5
posCI=len(os.listdir(POdir))
soatest_dir = 'F:/DataCNN/Test/confusion/8/70'
datadir= 'F:/Test_Sequenzen/ST080-N2H0/2_ST080N2H0_Rampe100-130_Pq70/data.csv'
pred = error(BS, '70/{classname}/*.avi', model)
listeSOA= SOA(datadir, soatest_dir)
eim(pred,'870.png',posCI, listeSOA)

