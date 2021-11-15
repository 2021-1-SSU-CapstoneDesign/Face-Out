import numpy as np
import cvlib as cv
import cv2
import face_recognition    # RGB이미지만 인식함

'''
STEP 1:
이미지를 꺼내서 RGB이미지로 변경하기
동영상을 꺼내기
그리고 imshow로 출력해보기
'''
# 학습할 IU이미지를 RGB형태로 변경
imgIU = face_recognition.load_image_file('img/iu.jpg')
imgIU = cv2.cvtColor(imgIU, cv2.COLOR_BGR2RGB)

# 테스트할 IU동영상을 불러옴
downloads_path = './img/iu_goo.mp4'
test_video = downloads_path    # 테스트 비디오를 바꾸고싶다면 여기를 바꾸기
cap=cv2.VideoCapture(test_video)

'''
STEP 2:
face detection = 얼굴 위치 확인
face encode = 그것을 숫자로 변경
'''
# 학습할 이미지
faceLoc = face_recognition.face_locations(imgIU)[0]    # return (top, right, bottom, left), print로 확인 가능
encodeIU = face_recognition.face_encodings(imgIU)[0]    # return 128 measurement
cv2.rectangle(imgIU, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

'''
STEP3:
동영상 frame별 모자이크
'''
# 프레임을 다시 모아 동영상으로 만들어야함
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # frame width
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # frame height
fps = cap.get(cv2.CAP_PROP_FPS)    # frame fps

fourcc = cv2.VideoWriter_fourcc(*'mp4v')    # 확장자가 mp4인 경우 MP4S 또는 MP4V를 사용  
writer = cv2.VideoWriter('face_mosaic.mp4', fourcc, fps, (w, h))
downloads_path = './static/member_video_downloads/iu_goo.mp4'
writer = cv2.VideoWriter(downloads_path, fourcc, fps, (w, h))

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
    faces = face_recognition.face_encodings(rgbframe)    # frame에서 각 얼굴의 distance를 가져옴

    # 얼굴 거리비교
    results = []
    faceDis = []
    for face in faces:
        dic = face_recognition.face_distance([encodeIU], face)
        if dic < 0.4:
            results.append(True)
        else:
            results.append(False)
        faceDis.append(dic)

    # frame에서 얼굴이 True이면 네모치기, False이면 모자이크
    faceLocTest = face_recognition.face_locations(frame)
    for index, result in enumerate(results):
        index_face_location = faceLocTest[index]
        if result == False:
            mosaic(frame, index_face_location)

    # cv2.imshow("frame", frame)
    writer.write(frame)
    if frame_num == 1:
        cv2.imwrite('./frame.jpg', frame)

    if cv2.waitKey(0) == 27:    # 만약 esc가 눌리면 while문을 벗어남
        break
print(writer)
writer.release()    # 동영상 저장
cv2.waitKey(0)    # 아무튼 뭔가 눌려야 실행종료(안누르면 안꺼짐)