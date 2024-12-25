import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from tensorflow.keras.preprocessing.image import load_img, img_to_array


data_dir = r"C:\Users\chestor"
genuine_dir = os.path.join(data_dir, "genuine")
forged_dir = os.path.join(data_dir, "forged")



def load_data(data_dir, label , img_size = (128, 128)):


    

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
        return np.array(images), np.array(labels)
    
    return load_images_from_folder(data_dir, label)

gen_signatures, gen_labels = load_data(genuine_dir,1)
forged_signatures, forged_labels = load_data(forged_dir,0)


all_images = np.concatenate((gen_signatures, forged_signatures), axis=0)
all_labels = np.concatenate((gen_labels, forged_labels), axis=0)

from sklearn.utils import shuffle
all_images, all_labels = shuffle(all_images, all_labels, random_state=42)

all_images = all_images / 255.0

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(all_images, all_labels, test_size=0.2, random_state=42)

print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")