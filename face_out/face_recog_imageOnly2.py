import cvlib as cv
import cv2
import face_recognition


# 테스트할 IU이미지를 RGB형태로 변경
imgTest = face_recognition.load_image_file('img/iu.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)


# 얼굴 위치
# faceLocTest = face_recognition.face_locations(imgTest)

# 모자이크 함수
def mosaic(src, ratio=0.1):
    faces = cv.detect_face(src)[0]

    for face in faces:
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]

        face_img = src[startY:endY, startX:endX]

        M = face_img.shape[0]
        N = face_img.shape[1]

        face_img = cv2.resize(face_img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        face_img = cv2.resize(face_img, (N, M), interpolation=cv2.INTER_NEAREST)

        src[startY:endY, startX:endX] = face_img

    return src

# 모자이크 처리
mosaic(imgTest)

cv2.imshow('imgTest', imgTest)
cv2.waitKey(0)