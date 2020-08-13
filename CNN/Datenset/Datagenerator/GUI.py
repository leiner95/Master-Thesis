from tkinter import *
import os
import numpy as np
from getAllCsvs import get_csv
from sort_Images import sort_images_HC, sort_images_CI
from copyImg import copy_images
from create_csv import information_csv

root = Tk()
root.title('Dataset Generator')

def create_ILPPELM(IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR, im, lp, path, process, esm, lightn, movedir):
    for i in range(0,len(im)):
        IM.append(im[i])
        LP.append(lp[i])
        PATH.append(path[i])
        PROCESS.append(process)
        ESM.append(esm[i])
        LIGHTN.append(lightn[i])
        MoveDIR.append(movedir[i])
    return IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR


def get_condition():
    # get the chossen parameter
    dd_text= distvar.get()
    dd_machine_text= machinevar.get()
    dd_Pfeature_text= processfeaturevar.get()
    thickness_text=eingabefeld_thick.get()
    parentpath_text=eingabefeld_parentp.get()
    newpath_text=eingabefeld_newp.get()
  
    possible_thick=('40', '50','60','80','100')
    if (thickness_text in possible_thick):
        start_label.config(text='Please Wait, The Dataset is Generated')
        filepath_names, dir_path_names=get_csv(parentpath_text, thickness_text, dd_Pfeature_text, dd_machine_text)

        IM=[]
        PATH=[]
        LP=[]
        PROCESS=[]
        ESM=[]
        LIGHTN=[]
        MoveDIR=[]

        for i in range(0,len(filepath_names)):
    	   
            if dd_text == 'Cut Interruption':
                im_names_PO, im_names_CI, lp_CI, lp_PO, imgpath_CI, imgpath_PO, esm_CI, esm_PO, LIGHT_CI, LIGHT_PO, DIR_CI, DIR_PO=sort_images_CI(filepath_names[i])
                if im_names_CI == []:
                    continue
                else:
                    copy_images(im_names_CI, newpath_text, filepath_names[i], 'CI')
                    IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR=create_ILPPELM(IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR, im_names_CI, lp_CI, imgpath_CI, 'CI', esm_CI, LIGHT_CI, DIR_CI)

            if dd_text == 'Process ok':
                im_names_PO, im_names_CI, lp_CI, lp_PO, imgpath_CI, imgpath_PO, esm_CI, esm_PO, LIGHT_CI, LIGHT_PO, DIR_CI, DIR_PO=sort_images_CI(filepath_names[i])

                if im_names_PO == []:
                    continue
                else:
                    copy_images(im_names_PO, newpath_text, filepath_names[i], 'PO')
                    IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR =create_ILPPELM(IM, LP, PATH, PROCESS, ESM,LIGHTN,MoveDIR, im_names_PO, lp_PO, imgpath_PO, 'PO', esm_PO, LIGHT_PO, DIR_PO)
            
            elif dd_text == 'Holder Crossing':
                im_names_HC, lp_HC, imgpath_HC, esm_HC, LIGHT_HC, DIR_HC=sort_images_HC(filepath_names[i])
                if im_names_HC == []:
                    continue
                else:
                    copy_images(im_names_HC, newpath_text, filepath_names[i],'HC' )
                    IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR=create_ILPPELM(IM, LP, PATH, PROCESS, ESM, LIGHTN,MoveDIR, im_names_HC, lp_HC, imgpath_HC, 'HC', esm_HC, LIGHT_HC, DIR_HC)


            elif dd_text == 'Holder Crossing, Cut Interruption, Process ok':
                try:
                    im_names_PO, im_names_CI, lp_CI, lp_PO, imgpath_CI, imgpath_PO, esm_CI, esm_PO, LIGHT_CI, LIGHT_PO, DIR_CI, DIR_PO=sort_images_CI(filepath_names[i])
                    if im_names_CI == []:
                        continue
                    else:
                        copy_images(im_names_CI, newpath_text, filepath_names[i], 'CI')
                        IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR=create_ILPPELM(IM, LP, PATH, PROCESS, ESM, LIGHTN,MoveDIR, im_names_CI, lp_CI, imgpath_CI, 'CI', esm_CI, LIGHT_CI, DIR_CI)

                    if im_names_PO == []:
                        continue
                    else:
                        copy_images(im_names_PO, newpath_text, filepath_names[i],'PO')
                        IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR =create_ILPPELM(IM, LP, PATH, PROCESS, ESM,LIGHTN,MoveDIR, im_names_PO, lp_PO, imgpath_PO, 'PO', esm_PO, LIGHT_PO, DIR_PO)

                    im_names_HC, lp_HC, imgpath_HC, esm_HC, LIGHT_HC, DIR_HC=sort_images_HC(filepath_names[i])
                    if im_names_HC ==[]:
                        continue
                    else:
                        copy_images(im_names_HC,newpath_text, filepath_names[i],'HC' )
                        IM, LP, PATH, PROCESS, ESM, LIGHTN, MoveDIR=create_ILPPELM(IM, LP, PATH, PROCESS, ESM, LIGHTN,MoveDIR, im_names_HC, lp_HC, imgpath_HC, 'HC', esm_HC, LIGHT_HC, DIR_HC)
                except:
                    pass
                
        print('MD', MoveDIR)
        #print('lL', len(LIGHTN))

        information_csv(IM, PATH, LP,  PROCESS, thickness_text, ESM, LIGHTN, MoveDIR)
        start_label.config(text='Generation of the dataset is done')

    # Error wrong inputs
    elif parentpath_text == '':
        start_label.config(text= 'Please enter a parent path !')
    elif newpath_text == '':
        start_label.config(text= 'Please enter a new path !')
    else:
        start_label.config(text= 'There is no data for ' + thickness_text + ' !')


#Choices
machinevar = StringVar(root)
distvar = StringVar(root)
processfeaturevar=StringVar(root)
choice_Pfeature= ('all', 'linear', 'Stege', '140', '130', '120', 'geregelt')
choice_machine= ('all', 'P8','P6','P3')
choice_dist=('Cut Interruption', 'Process ok', 'Holder Crossing', 'Holder Crossing, Cut Interruption, Process ok')
machinevar.set('') # set the default option
distvar.set('') # set the default option
processfeaturevar.set('')

#Labels
Label(root, text= 'Parent Path').grid(row=0, column=0, sticky=W, pady=4)
Label(root, text= 'New Path').grid(row=1, column=0, sticky=W, pady=4)
Label(root, text= 'Workpiece Thickness').grid(row=3, column=0, sticky=W, pady=4)
Label(root, text= 'Distinctive Feature').grid(row=4, column=0, sticky=W, pady=4)
Label(root, text= 'Machine Name').grid(row=5, column=0, sticky=W, pady=4)
Label(root, text= 'Process Feature').grid(row=6, column=0, sticky=W, pady=4)
start_label=Label(root, text = 'To generate a dataset press start')
start_label.grid(row=7, column=0, sticky=W, pady=4)

# Eingabefelder
eingabefeld_parentp = Entry(root)
eingabefeld_newp = Entry(root)
eingabefeld_thick=Entry(root)

eingabefeld_parentp.grid(row=0, column=1)
eingabefeld_newp.grid(row=1, column=1)

eingabefeld_thick.grid(row=3, column=1)

#Dropdown
OptionMenu(root, distvar, *choice_dist).grid(row=4, column=1)
OptionMenu(root,machinevar, *choice_machine).grid(row=5, column=1)
OptionMenu(root, processfeaturevar, *choice_Pfeature).grid(row=6, column = 1)

#Button
Button(root, text = 'start', command = get_condition).grid(row=8, column=0,pady=4)
Button(root, text = 'exit', command = root.quit).grid(row=8, column=1, pady=4)




root.mainloop()