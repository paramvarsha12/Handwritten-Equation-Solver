import cv2
import numpy as np
import os


drawing = False
ix, iy = -1, -1
canvas = 255 * np.ones((400, 400), dtype=np.uint8)

def draw(event, x, y, flags, param):
    global drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(canvas, (ix, iy), (x, y), (0), thickness=12)
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


label = input("Enter label (e.g., 3, plus, equal, x): ").strip().lower()
save_dir = f"data/symbol_dataset/{label}"
os.makedirs(save_dir, exist_ok=True)

print("\n Draw your symbol on the canvas. Press:")
print("  [s] to save  |  [c] to clear  |  [q] to quit\n")

cv2.namedWindow("Draw")
cv2.setMouseCallback("Draw", draw)

count = len(os.listdir(save_dir))

while True:
    cv2.imshow("Draw", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        resized = cv2.resize(canvas, (28, 28))
        filename = os.path.join(save_dir, f"{label}_{count}.png")
        cv2.imwrite(filename, resized)
        print(f"[✔] Saved: {filename}")
        count += 1
        canvas[:] = 255  
    elif key == ord('c'):
        canvas[:] = 255
        print("[🧼] Canvas cleared")
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
