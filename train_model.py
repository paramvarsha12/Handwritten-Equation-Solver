import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

data_dir = "data/symbol_dataset"
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'divide', 'equal', 'left_paren', 'minus', 'multiply',
          'plus', 'right_paren', 'x', 'y', 'z']

X, y = [], []

for idx, label in enumerate(labels):
    path = os.path.join(data_dir, label)
    if not os.path.exists(path):
        continue
    for img_name in os.listdir(path):
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, (28, 28))
        X.append(img)
        y.append(idx)

X = np.array(X).reshape(-1, 28, 28, 1).astype("float32") / 255.0
y = to_categorical(y, num_classes=len(labels))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=32)

model.save("model.h5")
