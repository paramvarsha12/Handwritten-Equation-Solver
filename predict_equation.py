import cv2
import numpy as np
from tensorflow.keras.models import load_model
from equation_solver import evaluate_equation

model = load_model("model.h5")

labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'divide', 'equal', 'left_paren', 'minus', 'multiply',
          'plus', 'right_paren', 'x', 'y', 'z']

symbol_map = {
    'divide': '/', 'equal': '=', 'left_paren': '(', 'minus': '-', 
    'multiply': '*', 'plus': '+', 'right_paren': ')'
}

def predict_equation(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return '', "Image not found"

    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    symbols = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:
            symbols.append((x, y, w, h))

    if not symbols:
        return '', "No symbols detected"

    symbols = sorted(symbols, key=lambda x: x[0])
    equation = ""

    for x, y, w, h in symbols:
        roi = thresh[y:y+h, x:x+w]
        roi = cv2.resize(roi, (28, 28))
        roi = roi.astype("float32") / 255.0
        roi = np.expand_dims(roi, axis=-1)
        roi = np.expand_dims(roi, axis=0)

        prediction = model.predict(roi, verbose=0)
        index = np.argmax(prediction)
        label = labels[index]
        equation += symbol_map.get(label, label)

    try:
        solution = evaluate_equation(equation)
    except:
        solution = "Invalid arithmetic expression"

    return equation, str(solution)
