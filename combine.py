
# import tqdm
import os
import shutil
import cv2 
import imghdr

path = './visa/raw/'

save_path = './visa/raw/Combine'

list_dir = ['Vietnam Visa', 
            'Vietnam Visa for foreigners', 
            'Visa', 
            'Visa Việt Nam']
list_name = ['vietnamvisa', 
            'vietnamvisaforforeigners', 
            'visa', 
            'visavietnam']
# list_dir = ['9_dash_line_crawl_data_sprint2']

for lv0, lv0_name in zip(list_dir, list_name):
    folder = os.path.join(path, lv0)
    if os.path.exists(folder):
        out_folder = os.path.join(save_path)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder, exist_ok=True)

        filenames = os.listdir(folder)
        for filename in filenames:
            print(filename)
            in_path  = os.path.join(folder, filename)
            out_path = os.path.join(out_folder, lv0_name + '_' + filename)
            shutil.copyfile(in_path, out_path)


 
