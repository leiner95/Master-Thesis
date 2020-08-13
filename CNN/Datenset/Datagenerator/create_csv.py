import csv
import os


def machine(string, im_path, Mac):
    if string in im_path: 
        Mac=string
    return Mac


def information_csv(im_names, path, laser_pow, process, thickness_text, ESM, LIGHTN, MoveDir):
    name = 'im_infos'+ str(thickness_text)+ str(process[0]) + os.extsep + 'csv'
    with open(name, 'w') as csvfile:
        examwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        header =('Name', 'Laser Power', 'Process', 'Machine', 'Thickness', 'ESM', 'Lightning', 'Direction of Movement')
        examwriter.writerow(header)
        for i in range(0, len(im_names)):
            im_path = path[i]
            im_name = im_names[i]
            proc = process[i]
            esm=ESM[i]
            light=LIGHTN[i]
            movedir=MoveDir[i]
            # Maschine 
            Mac=[]
            try:
                Mac = machine('P8', im_path, Mac)
            except:
                continue
            try:
                Mac = machine('P6', im_path, Mac)
            except:
                continue
            try:
                Mac = machine('P3', im_path, Mac)
            except:
                continue
            thickness= thickness_text
            laser_power = laser_pow[i]
            listrow = [(im_name), (laser_power), (proc), (Mac), (thickness), (esm), (light), (movedir)]
            examwriter.writerow(listrow)
    print('done')

