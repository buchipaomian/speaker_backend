import os
import uuid
base_path = "data"

def path_generater(name,type):
    folder_path = os.path.join(base_path,type)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename_temp = os.path.join(folder_path,name)
    i = 0
    while os.path.exists(filename_temp):
        filename_temp = os.path.join(folder_path,str(i)+name)
        i+=1
    filename = filename_temp
    return filename

def generate_random_file_path(type,file_type):
    folder_path = os.path.join(base_path,type)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename_temp = os.path.join(folder_path,str(uuid.uuid4())+file_type)
    while os.path.exists(filename_temp):
        filename_temp = os.path.join(folder_path,str(uuid.uuid4())+file_type)
    filename = filename_temp
    return filename