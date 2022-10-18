import numpy as np
import cv2

def getSymbol(value):
    index = int((value / 255) * (len(DENSITY) - 1))
    return DENSITY[index]

#29 symbols
DENSITY = 'Ñ@#W$9876543210?!abc;:+=-,._ '
WIDTH = 200
HEIGHT = 100
CHANNEL = 3

img = cv2.imread('support.jpg')
resized = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)

output = ""

for i in range(HEIGHT):
    output += "\n"
    for j in range(WIDTH):
        avg = sum(resized[i, j]) / len(resized[i, j])
        output += getSymbol(avg)

print(output)

with open('ascii.txt', 'w', encoding="utf-8") as f:
    f.write(output)

cv2.imshow("zdjecie", resized)
cv2.waitKey(0)