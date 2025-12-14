import cv2
import numpy as np

img = cv2.imread("baby.png")

# 定义锐化卷积核
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

sharpened = cv2.filter2D(img, -1, kernel)

cv2.imshow("Sharpened Image", sharpened)
cv2.imwrite("sharpen_output.jpg", sharpened)
cv2.waitKey(0)
cv2.destroyAllWindows()
