import cvlib as cv
import cv2
import face_recognition    # RGB이미지만 인식함
import os

'''
STEP 1:
이미지를 꺼내서 RGB이미지로 변경하기
그리고 imshow로 출력해보기
'''

def input1(img_path):
    # 학습할 이미지를 RGB형태로 변경
    imgTrain = face_recognition.load_image_file(img_path)
    imgTrain = cv2.cvtColor(imgTrain, cv2.COLOR_BGR2RGB)
    return imgTrain


def input2(img_path):
    # 테스트할 이미지를 RGB형태로 변경
    imgTest = face_recognition.load_image_file(img_path)    # test이미지를 바꾸고싶으면 여기를 바꾸기
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)
    return imgTest


def process(imgTest, imgTrain):
    '''
    STEP 2:
    face detection = 얼굴 위치 확인
    face encode = 그것을 숫자로 변경
    '''
    # 학습할 이미지
    # 하나의 이미지로 train을 해서 첫번째 요소만 필요(?)
    faceLoc = face_recognition.face_locations(imgTrain)[0]    # return (top, right, bottom, left), print로 확인 가능
    encodeIU = face_recognition.face_encodings(imgTrain)[0]    # return 128 measurement
    # 찾은 detection위치를 rectangle로 그리자
    # cv2.rectangle(img, start, end, color, thickness)
    cv2.rectangle(imgTrain, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    # 테스트할 이미지
    faceLocTest = face_recognition.face_locations(imgTest)    # [(92, 390, 199, 282), (136, 643, 226, 554)]
    encodeTest = face_recognition.face_encodings(imgTest)

    '''
    STEP 3:
    두 얼굴(의 인코딩 값)을 비교하고
    두 얼굴(의 인코딩 값) 사이의 거리(얼마나 닮았나)를 비교
    
    비교 모델: linear SVM
    '''
    results = []
    faceDis = []
    croppedFace = []
    for encode_test in encodeTest:
        dic = face_recognition.face_distance([encodeIU], encode_test)
        print(dic)
        if dic < 0.4:
            result = True
        else:
            result = False
        results.append(result)
        faceDis.append(dic)

    faceLocTest = face_recognition.face_locations(imgTest)
    for index, result in enumerate(results):
        face = faceLocTest[index]
        if result == False:  # 만약 result로 동인인물이 아니라고(False라고) 나오면
            imgTest = mosaic(imgTest, face)
    return imgTest



'''
STEP 4:
false인 부분 모자이크 처리
'''
def mosaic(src, face, ratio=0.05):
    (startX, startY) = face[3], face[0]    # left, top
    (endX, endY) = face[1], face[2]    # right, bottom

    face_img = src[startY:endY, startX:endX]    # [top:bottom, left:right]

    M = face_img.shape[0]
    N = face_img.shape[1]

    face_img = cv2.resize(face_img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    face_img = cv2.resize(face_img, (N, M), interpolation=cv2.INTER_NEAREST)

    src[startY:endY, startX:endX] = face_img

    return src

def save(imgTest, path, filename):
    cv2.imwrite(os.path.join(path, filename), imgTest)    # 이미지 저장
    cv2.waitKey(0)

