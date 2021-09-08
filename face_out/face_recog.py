import cv2
import os
import numpy as np
import face_recognition    # RGB이미지만 인식함

'''
STEP 1:
이미지를 꺼내서 RGB이미지로 변경하기
그리고 imshow로 출력해보기
'''


def input2(img_path):
    # 테스트할 IU이미지를 RGB형태로 변경, 단체사진
    print(img_path)
    #response = urllib.request.urlopen(img_path)
    imgTest = face_recognition.load_image_file(img_path)  # test이미지를 바꾸고싶으면 여기를 바꾸기
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)
    return imgTest


def input1(img_path2):
    # 학습할 IU이미지를 RGB형태로 변경
    imgIU = face_recognition.load_image_file(img_path2)
    imgIU = cv2.cvtColor(imgIU, cv2.COLOR_BGR2RGB)
    return imgIU



def process(imgTest, imgIU):

    '''
    STEP 2:
    face detection = 얼굴 위치 확인
    face encode = 그것을 숫자로 변경
    '''
    # 학습할 이미지
    # 하나의 이미지로 train을 해서 첫번째 요소만 필요(?)
    faceLoc = face_recognition.face_locations(imgIU)[0]  # return (top, right, bottom, left), print로 확인 가능
    encodeIU = face_recognition.face_encodings(imgIU)[0]  # return 128 measurement
    # 찾은 detection위치를 rectangle로 그리자
    cv2.rectangle(imgIU, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255),
                  2)  # cv2.rectangle(img, start, end, color, thickness)

    # 테스트할 이미지
    faceLocTest = face_recognition.face_locations(imgTest)  # [(92, 390, 199, 282), (136, 643, 226, 554)]
    encodeTest = face_recognition.face_encodings(imgTest)
    for face in faceLocTest:
        cv2.rectangle(imgTest, (face[3], face[0]), (face[1], face[2]), (255, 0, 255), 2)

    return imgTest

def show(imgTest, path, filename):
    # 이미지 화면에 띄우기
    # cv2.imshow('IU', imgIU)
    #cv2.imshow('IU Test', imgTest)
    cv2.imwrite(os.path.join(path, filename), imgTest)
    cv2.waitKey(0)

#    cv2.imwrite('result/res.jpg', imgTest)  # 이미지 저장
#    cv2.waitKey(5000)  # 1ms안에 코드 종료됨
