import numpy as np
import cv2
import os


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

        try:
            a = frameId % multiplier
            if a< 1:
                # cv2.resize(img, dsize, fx, fy, interpolation)
                resizeImage = cv2.resize(frame, (320, 320))
                #cv2.imwrite("frame%d.jpg" % frameCount, resizeImage)
                return resizeImage
                frameCount += 1
        except:
            print("error")

        if onlyMainStillCut:
            break

def save(img, path, filename):
    #cv2.imwrite(os.path.join(path, filename), img)    # 이미지 저장
    #cv2.imwrite('./static/thumnail/dayoung.jpg', img)  # 이미지 저장
    cv2.imwrite(os.path.join(path, filename), img)
    cv2.imwrite(path, img)
    cv2.waitKey(0)

#if __name__ == '__main__':
#    img = makeStillCutImage('./static/member_video_downloads/dayoung-iu_goo.mp4')
    #save(img, './static/thumnail', 'dayoung-iu_goo.mp4')
#    path = './static/thumnail/dayoung.jpg'
#    save(img, path)
