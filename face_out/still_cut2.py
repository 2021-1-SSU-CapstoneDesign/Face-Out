import numpy as np
import cv2


def makeStillCutImage(path, onlyMainStillCut=False):
    videoObj = cv2.VideoCapture(path)

    seconds = 10
    fps = videoObj.get(cv2.CAP_PROP_FPS)  # Gets the frames per second
    multiplier = fps * seconds

    frameCount = 0
    ret = 1

    while ret:
        frameId = int(round(videoObj.get(1)))  # current frame number
        ret, frame = videoObj.read()

        if frameId % multiplier < 1:
            # cv2.resize(img, dsize, fx, fy, interpolation)
            resizeImage = cv2.resize(frame, (320, 320))
            cv2.imwrite("frame%d.jpg" % frameCount, resizeImage)
            frameCount += 1

        if onlyMainStillCut:
            break


if __name__ == '__main__':
    makeStillCutImage('test.mp4')