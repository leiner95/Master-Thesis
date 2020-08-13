import cv2
import os
import glob
import shutil

def makevid(imagefolder, Path):
    os.chdir(imagefolder)
    img_array = []

    for filename in glob.iglob('*.tif'):
        print('f',filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    try:
        name= os.path.split(imagefolder)[1] + 'vid.avi'
        out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'DIVX'), 18, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
    except:
        pass
    

    for filename in glob.iglob('*.avi'):
        shutil.move(str(imagefolder+os.sep + filename),str(Path+os.sep + filename))
    


Path='C:/Masterarbeit/SchmelzschnittRCNN/nalltest/8/ESM/PO'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/ESM/CI'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)

Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/70/PO'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/70/CI'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)

Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/140/PO'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/140/CI'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)

Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/strahl/PO'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/strahl/CI'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)

Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/normal/PO'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
Path='C:/Masterarbeit/SchmelzschnittRCNN/alltest/8/normal/CI'
changedir = os.listdir(Path)
for i in range(0, len(changedir)):
    imagefolder= str(Path + os.sep + changedir[i])
    print(imagefolder)
    makevid(imagefolder, Path)
