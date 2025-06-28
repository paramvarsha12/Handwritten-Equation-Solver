import cv2
import numpy as np
import os

canvas = np.ones((400, 1000), dtype=np.uint8) * 255
drawing = False
ix, iy = -1, -1

def draw(event, x, y, flags, param):
    global ix, iy, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(canvas, (ix, iy), (x, y), (0), thickness=12)
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

save_path = "data/test_images"
os.makedirs(save_path, exist_ok=True)

cv2.namedWindow("Draw Equation", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Draw Equation", draw)

print("Draw your full equation. Press:")
print("[s] Save   [c] Clear   [q] Quit")

count = len(os.listdir(save_path))

while True:
    cv2.imshow("Draw Equation", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = os.path.join(save_path, f"eq{count}.png")
        cv2.imwrite(filename, canvas)
        print(f"Saved: {filename}")
        count += 1
        canvas[:] = 255
    elif key == ord('c'):
        canvas[:] = 255
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
