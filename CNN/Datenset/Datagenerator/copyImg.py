import glob
import os
import shutil
import math

def checkdouble(filename, im_path, new_path):
    ofile= im_path + os.sep + filename
    if os.path.exists(ofile):  
        fil= new_path+ os.sep + filename
        for f in glob.iglob(os.path.join(new_path, filename)):
            nfile= new_path+ os.sep + str('1_' + filename)
            os.rename(fil, nfile)
        shutil.copy(ofile,fil)
        if not os.path.exists(fil): 
            sleep(1)
            

def copy_images(im_names, des_path, path, classes):

    if len(im_names)>1:
        for i in range(0,len(im_names)):
            null=str(0)
            imp = im_names[i]
            im_path = str(os.path.split(path)[0] + os.sep + 'images' + os.sep + 'TcProcessLightImage')
            new_path = des_path + os.sep + classes
            try:
                os.makedirs(new_path)  
            except: 
                pass
            filename2= null + null + imp + os.extsep + 'tif'
            checkdouble(filename2,im_path,new_path)

            filename3= null + null + null + imp + os.extsep + 'tif'
            checkdouble(filename3,im_path,new_path)
        

            filename4= null + null + null + null + imp + os.extsep + 'tif'
            checkdouble(filename4,im_path,new_path)
