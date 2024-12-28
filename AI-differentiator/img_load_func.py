import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
from sklearn.model_selection import train_test_split

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

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, validation_split=0.2, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.2f}")

# Predict on a new signature
def predict_signature(image):
    processed_image = image / 255.0
    processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension
    return "Genuine" if model.predict(processed_image) > 0.5 else "Forged"

# Example prediction
new_signature = np.random.rand(128, 128, 1)  # Replace with actual signature image
result = predict_signature(new_signature)
print(f"Prediction: {result}")