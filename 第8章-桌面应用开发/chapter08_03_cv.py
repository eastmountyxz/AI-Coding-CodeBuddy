import cv2
import numpy as np

img = cv2.imread("baby.png")
rows, cols = img.shape[:2]

# 定义平移矩阵 (右移50，下移30)
M = np.float32([[1, 0, 50], [0, 1, 30]])
shifted = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow("Shifted Image", shifted)
cv2.imwrite("shifted_output.png", shifted)
cv2.waitKey(0)
cv2.destroyAllWindows()
