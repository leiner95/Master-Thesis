import os

def get_csv(path, condition_thick, condition_proc, condition_machine):
    filepath_names= []
    dir_path_names=[]
    j=0
    possiblemachine= ('P3', 'P6', 'P8')
    possibleproc= ('linear', 'Stege', '140', '130', '120', 'geregelt')
    for dirpath, dirnames, names in os.walk(path):         
        i = len(dirnames)
        k=0
        while k < i: 
            dirname = dirnames[k]
            if condition_thick in dirname:
                new_path = dirpath +  os.sep + dirnames[k]
                for new_dirpath, new_dirnames, filenames in os.walk(new_path):
                    if "images" in new_dirnames:
                        new_dirnames.remove ("images")
                    if 'calibrationData' in new_dirnames:
                        new_dirnames.remove ('calibrationData')
                    if condition_proc == 'all' and condition_machine == 'all':
                        for data in filenames: 
                            if data.endswith(('data.csv')):
                                filepath_csv= str(new_dirpath +  os.sep + data)
                                filepath_names.append(filepath_csv)
                                dir_path_names.append(new_dirpath)

                    elif condition_machine == 'all' and condition_proc in possibleproc:
                        for data in filenames: 
                            if data.endswith(('data.csv')) and condition_proc in new_dirpath:
                                filepath_csv= str(new_dirpath +  os.sep + data)
                                filepath_names.append(filepath_csv)
                                dir_path_names.append(new_dirpath)
                                
                    
                    elif condition_machine in possiblemachine and condition_proc in possibleproc:
                        for data in filenames: 
                            if data.endswith(('data.csv')) and condition_proc in new_dirpath and condition_machine in new_dirpath:
                                filepath_csv= str(new_dirpath +  os.sep + data)
                                filepath_names.append(filepath_csv)
                                dir_path_names.append(new_dirpath)
                    
                    elif condition_machine in possiblemachine and condition_proc == 'all':
                        for data in filenames: 
                            if data.endswith(('data.csv')) and condition_machine in new_dirpath:
                                filepath_csv= str(new_dirpath +  os.sep + data)
                                filepath_names.append(filepath_csv)
                                dir_path_names.append(new_dirpath)

                    
                k = k + 1
            else: 
                k = k + 1

        return filepath_names, dir_path_names
