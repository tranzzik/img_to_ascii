# import the opencv library
import cv2
import numpy as np
from numba import jit
  
WIDTH = 192
HEIGHT = 144
DENSITY = 'Ñ@#W$9876543210?!abc;:+=-,._                '
HIGH_DENSITY_ORIGINAL = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
HIGH_DENSITY = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.                                                "


# def getSymbol(value):
#     index = int((value / 255) * (len(DENSITY) - 1))
#     return DENSITY[index]

def generate_ascii_letters():
    images = []
    #letters = "# $%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    letters = " \\ '(),-./:;[]_`{|}~"
    for letter in letters:
        img = np.zeros((12, 16), np.uint8)
        img = cv2.putText(img, letter, (0, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        images.append(img)
    return np.stack(images)

@jit(nopython=True)
def to_ascii_art(frame, images, box_height=12, box_width=16):
    height, width = frame.shape
    for i in range(0, height, box_height):
        for j in range(0, width, box_width):
            roi = frame[i:i + box_height, j:j + box_width]
            best_match = np.inf
            best_match_index = 0
            for k in range(1, images.shape[0]):
                total_sum = np.sum(np.absolute(np.subtract(roi, images[k])))
                if total_sum < best_match:
                    best_match = total_sum
                    best_match_index = k
            roi[:,:] = images[best_match_index]
    return frame

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
images = generate_ascii_letters()
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    gb = cv2.GaussianBlur(frame, (5, 5), 0)
    can = cv2.Canny(gb, 127, 31)
    ascii_art = to_ascii_art(can, images)

    #resized = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)

    #output = ""

    # for i in range(HEIGHT):
    #     output += "\n"
    #     for j in range(WIDTH):
    #         avg = sum(resized[i, j]) / len(resized[i, j])
    #         output += getSymbol(avg)
  
    # # Display the resulting frame
    cv2.imshow('frame', ascii_art)
    # with open('ascii.txt', 'w', encoding="utf-8") as f:
    #     f.write(output)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()