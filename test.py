import numpy as np
import pyautogui
from mss import mss
import cv2
from PIL import *

# with mss() as sct:
# 	img = np.array(sct.grab(sct.monitors[0]))
# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 	edges = cv2.Canny(gray, 200, 255, apertureSize = 3)
# 	lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength=80, maxLineGap=0)
# 	for line in lines:
# 		x1, y1, x2, y2 = line[0]
# 		cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
# 		print(line[0])

# 	cv2.imshow('image1', img)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()

resolution_scale = 2

img = Image.open(open('img_recognition_sample/tl.png', 'rb'))
img = img.resize((resolution_scale * x for x in img.size), Image.BILINEAR)
tl_x, tl_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
print(img)
print((tl_x, tl_y))

img = Image.open(open('img_recognition_sample/tr.png', 'rb'))
img = img.resize((resolution_scale * x for x in img.size), Image.BILINEAR)
tr_x, tr_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
print(img)
print((tr_x, tr_y))

img = Image.open(open('img_recognition_sample/bl.png', 'rb'))
img = img.resize((resolution_scale * x for x in img.size), Image.BILINEAR)
bl_x, bl_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
print(img)
print((bl_x, bl_y))

img = Image.open(open('img_recognition_sample/br.png', 'rb'))
img = img.resize((resolution_scale * x for x in img.size), Image.BILINEAR)
br_x, br_y = pyautogui.locateCenterOnScreen(img, grayscale=True, confidence=0.95)
print(img)
print((br_x, br_y))


print(bl_x == tl_x)
print(br_x == tr_x)
print(bl_y == br_y)
print(tr_y == tl_y)

start_x = tl_x + 10 * resolution_scale
start_y = tl_y + 46 * resolution_scale
print((start_x, start_y))

end_x = br_x - 10 * resolution_scale
end_y = br_y - 10 * resolution_scale
print((end_x, end_y))


