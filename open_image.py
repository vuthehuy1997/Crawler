
import os
import cv2
import imghdr

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
path = 'crawl/img_url/Combine_open'
file_names = os.listdir(path)
# file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0]))
file_paths = [os.path.join(path, i) for i in file_names]
count_error = 0
for file_path in file_paths:
    # print(imghdr.what(file_path))
    try:
        if not imghdr.what(file_path) in ALLOWED_EXTENSIONS:
            print(file_path)
            print(imghdr.what(file_path))
        # exit()
            if imghdr.what(file_path) == 'gif':
                cap = cv2.VideoCapture(file_path)
                ret, img = cap.read()
                cap.release()
                cv2.imwrite(file_path, img)
            else:
                img = cv2.imread(file_path)
                cv2.imwrite(file_path, img)
    except:
        print('Error: ',file_path)
        os.remove(file_path)
        count_error += 1

print('Total: ', len(file_paths))
print('ERROR: ', count_error)