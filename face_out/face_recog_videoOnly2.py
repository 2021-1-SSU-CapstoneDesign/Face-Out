import numpy as np
import cvlib as cv
import cv2
import face_recognition

# 테스트할 IU동영상을 불러옴
test_video = './img/girl3.gif'    # 테스트 비디오를 바꾸고싶다면 여기를 바꾸기
cap=cv2.VideoCapture(test_video)

# 프레임을 다시 모아 동영상으로 만들어야함
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # frame width
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # frame height
fps = cap.get(cv2.CAP_PROP_FPS)    # frame fps

fourcc = cv2.VideoWriter_fourcc(*'mp4v')    # 확장자가 mp4인 경우 MP4S 또는 MP4V를 사용  
writer = cv2.VideoWriter('./face_mosaic.mp4', fourcc, fps, (w, h))

# 모자이크 함수
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

frame_num = 0
# 동영상 모자이크 코드
while(True):
    frame_num += 1
    print("현재 프레임:", frame_num)

    # frame 추출
    ret, frame = cap.read()    # ret: 잘 읽으면 True, 못읽으면 False # frame: 하나의 프레임  
    if np.shape(frame)==():    # 만약 더이상 frame이 읽히지 않으면 while문 빠져나오기
        break
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 얼굴 위치 추출
    faceLocTest = face_recognition.face_locations(frame)
    for face in faceLocTest:
        mosaic(frame, face)

    # cv2.imshow("frame", frame)
    writer.write(frame)

    if cv2.waitKey(0) == 27:    # 만약 esc가 눌리면 while문을 벗어남
        break

writer.release()    # 동영상 저장
cv2.waitKey(0)    # 아무튼 뭔가 눌려야 실행종료(안누르면 안꺼짐)