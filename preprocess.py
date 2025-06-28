import cv2
import numpy as np

def preprocess_image(image_path):
  

    
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

   
    _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    
    resized = cv2.resize(thresh, (28, 28))

    
    normalized = resized.astype("float32") / 255.0

    
    normalized = np.expand_dims(normalized, axis=-1)  

    return normalized
