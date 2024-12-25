import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from tensorflow.keras.preprocessing.image import load_img, img_to_array


data_dir = r"C:\Users\chestor"
genuine_dir = os.path.join(data_dir, "genuine")
forged_dir = os.path.join(data_dir, "forged")



def load_data(data_dir, img_size = (128, 128)):


    

    images = []
    labels = []
    

    def load_images_from_folder(folder, label):
        for filename in os.listdir(folder):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                filepath = os.path.join(folder, filename)
            img = load_img(filepath, target_size=img_size, color_mode="grayscale")
            img_array = img_to_array(img)  
            images.append(img_array)
            labels.append(label)  
        return img_array
    
    return load_images_from_folder(data_dir,1)

gen_sign = load_data(genuine_dir)
forged_sign = load_data(forged_dir)


print(gen_sign)
print(forged_sign)
