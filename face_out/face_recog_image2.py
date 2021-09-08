import cvlib as cv
import cv2
import numpy as np
import face_recognition    # RGB이미지만 인식함

'''
STEP 1:
이미지를 꺼내서 RGB이미지로 변경하기
그리고 imshow로 출력해보기
'''
# 학습할 IU이미지를 RGB형태로 변경
imgIU = face_recognition.load_image_file('ImageBasic/IU_1.jpg')
imgIU = cv2.cvtColor(imgIU, cv2.COLOR_BGR2RGB)

# 테스트할 IU이미지를 RGB형태로 변경
imgTest = face_recognition.load_image_file('ImageBasic/아이유_유인나.jpg')    # test이미지를 바꾸고싶으면 여기를 바꾸기
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

'''
STEP 2:
face detection = 얼굴 위치 확인
face encode = 그것을 숫자로 변경
'''
# 학습할 이미지
# 하나의 이미지로 train을 해서 첫번째 요소만 필요(?)
faceLoc = face_recognition.face_locations(imgIU)[0]    # return (top, right, bottom, left), print로 확인 가능
encodeIU = face_recognition.face_encodings(imgIU)[0]    # return 128 measurement
# 찾은 detection위치를 rectangle로 그리자
# cv2.rectangle(img, start, end, color, thickness)
cv2.rectangle(imgIU, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

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
    # result = face_recognition.compare_faces([encodeIU], encode_test)
    dic = face_recognition.face_distance([encodeIU], encode_test)
    if dic < 0.45:
        result = True
    else:
        result = False

    results.append(result)
    faceDis.append(dic)

'''
최서윤이 만든 STEP 4:
false인 부분 모자이크 처리
'''
def mosaic(src, face, ratio=0.1):    
    (startX, startY) = face[3], face[0]    # left, top
    (endX, endY) = face[1], face[2]    # right, bottom

    face_img = src[startY:endY, startX:endX]    # [top:bottom, left:right]

    M = face_img.shape[0]
    N = face_img.shape[1]

    face_img = cv2.resize(face_img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    face_img = cv2.resize(face_img, (N, M), interpolation=cv2.INTER_NEAREST)

    src[startY:endY, startX:endX] = face_img

    return src


faceLocTest = face_recognition.face_locations(imgTest)
for index, result in enumerate(results):
    face = faceLocTest[index]
    if result == False:    # 만약 result로 동인인물이 아니라고(False라고) 나오면
        
        imgTest = mosaic(imgTest, face)

cv2.imwrite('./ImageAttendance/seoyun.jpg', imgTest) 
cv2.waitKey(1)    # 키보드가 눌리기전까지 프로그램이 무기한 기다린다