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
                listeSOA.append(2)
    return listeSOA
#Testbilder
def error(model, dir):

    batch_size =1000 # Erhöhen wenn größere Datenmenge
    IMG_HEIGHT = 150
    IMG_WIDTH = 150
    test_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data
    test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
                                                                directory=test_dir,
                                                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                class_mode='binary', 
                                                                shuffle= False)
    sample_test_images, labels = next(test_data_gen)
    prediction = model.predict(sample_test_images)
    print(prediction)
    #print(len(prediction))
    class_names = ['CI', 'HC', 'PO']

    pred=[]
    for ix in range(0,len(prediction)): 
        P = np.argmax(prediction[ix])
        #print(prediction[ix])
     
        pred.append(P)
      
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
        
        if  listeSOA[i] == 2:
                array[a3:a4,a1:a2] = [127, 255, 0] #PO grun1
        elif listeSOA[i] == 0:
                array[a3:a4,a1:a2] = [69, 139, 0] #CI grun2

    # Prediction Line
    b2=0
    for i in range(0,len(prediction)):
        b1= b2
        b2= int(b1 + 300)
        
        if prediction[i] == 2:
            array[b3:b4,b1:b2] = [127, 255, 0] #PO grun1
        elif prediction[i] == 0:
            array[b3:b4,b1:b2] = [69, 139, 0] #CI grun2
        elif prediction[i]== 1:
            array[b3:b4,b1:b2] = [148, 0, 211] # PO-HC violet
    img = Image.fromarray(array, 'RGB')
    img.save(name)


model= load_model('100_Alexnet_model.h5')
POdir='F:/DataCNN/Test/time/10/70/PO'
posCI=len(os.listdir(POdir))
test_dir = 'F:/DataCNN/Test/time/10/70'
datadir= 'F:/Test_Sequenzen/ST100-N2H0/2_ST100N2H0_Rampe100-130_Pq70/data.csv'
pred = error(model, test_dir)
listeSOA= SOA(datadir, test_dir)
eim(pred,'1070.png',posCI, listeSOA)

POdir='F:/DataCNN/Test/time/10/140/PO'
posCI=len(os.listdir(POdir))
test_dir = 'F:/DataCNN/Test/time/10/140'
datadir= 'F:/Test_Sequenzen/ST100-N2H0/3_ST100N2H0_Rampe100-130_Pq140/data.csv'
pred = error(model, test_dir)
listeSOA= SOA(datadir, test_dir)
eim(pred,'10140.png',posCI, listeSOA)

POdir='F:/DataCNN/Test/time/10/normal/PO'
posCI=len(os.listdir(POdir))
test_dir = 'F:/DataCNN/Test/time/10/normal'
datadir= 'F:/Test_Sequenzen/ST100-N2H0/0_ST100N2H0_Rampe100-130_Standard/data.csv'
pred = error(model, test_dir)
listeSOA= SOA(datadir, test_dir)
eim(pred,'10normal.png',posCI, listeSOA)

POdir='F:/DataCNN/Test/time/10/strahl/PO'
posCI=len(os.listdir(POdir))
test_dir = 'F:/DataCNN/Test/time/10/strahl'
datadir= 'F:/Test_Sequenzen/ST100-N2H0/4_ST100N2H0_Rampe100-130_Strahlaußermittigkeit/data.csv'
pred = error(model, test_dir)
listeSOA= SOA(datadir, test_dir)
eim(pred,'10strahl.png',posCI, listeSOA)

POdir='F:/DataCNN/Test/time/10/ESM/PO'
posCI=len(os.listdir(POdir))
test_dir = 'F:/DataCNN/Test/time/10/ESM'
datadir= 'F:/Test_Sequenzen/ST100-N2H0/1_ST100N2H0_Rampe100-130_ESM+0.5/data.csv'
pred = error(model, test_dir)
listeSOA= SOA(datadir, test_dir)
eim(pred,'10ESM.png',posCI, listeSOA)

