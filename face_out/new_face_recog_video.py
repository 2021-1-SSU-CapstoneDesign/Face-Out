import os
import cv2
import time
import re
import argparse

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from deepface import DeepFace
from deepface.commons import functions, distance as dst
from deepface.detectors import FaceDetector

def input1(video_path):
    # 모자이크에서 제외할 이미지 경로
    return video_path

def input2(video_path):
    # 모자이크 처리할 비디오 경로
    return video_path

def process(
    db_path ,    # target으로 들어온 jpg이미지 넣는 곳
    thumnail,
    output_path="videos/results.avi",
    model_name="VGG-Face",    # 이미지 비교에 사용 (우리는 FaceNet사용)
    detector_backend="opencv", # 네모박스 찾는 detection에 사용 (우리는 ssd사용)
    distance_metric="cosine",    # 거리 비교 metric
    source=0,    # video file을 불러옴

):

    # ------------------------

    face_detector = FaceDetector.build_model(detector_backend)    # 우리는 ssd사용
    print("Detector backend is ", detector_backend)

    # ------------------------
    filename = output_path
    fc = 20    # 초당 저장할 frame

    input_shape = (224, 224)
    input_shape_x = input_shape[0]
    input_shape_y = input_shape[1]

    text_color = (255, 255, 255)

    # target(e.g.아이유 인물 사진)이 있는지 확인

    employee = db_path


    model = DeepFace.build_model(model_name)    # 우리는 FaceNet사용
    print(model_name, " is built")

    # ------------------------

    input_shape = functions.find_input_shape(model)
    input_shape_x = input_shape[0]
    input_shape_y = input_shape[1]

    # tuned thresholds for model and metric pair
    threshold = dst.findThreshold(model_name, distance_metric)

    # ------------------------

    # find embeddings for employee list

    tic = time.time()

    # for employee in employees:
    embedding = []

    # preprocess_face returns single face. this is expected for source images in db.
    img = functions.preprocess_face(
        img=employee,
        target_size=(input_shape_y, input_shape_x),
        enforce_detection=False,
        detector_backend=detector_backend,
    )
    img_representation = model.predict(img)[0, :]

    embedding.append(employee)
    embedding.append(img_representation)

    toc = time.time()

    print("Embeddings found for given data set in ", toc - tic, " seconds")    # 사람얼굴 detection에 걸린 시간

    # -----------------------

    pivot_img_size = 112  # face recognition result image

    # -----------------------
    face_detected = False
    tic = time.time()

    cap = cv2.VideoCapture(source)  # webcam 
    codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")    # 디지털 미디어 포맷 코드를 생성(인코딩 방식을 설정)
    out = cv2.VideoWriter(filename, codec, fc, ( int(cap.get(3)), int(cap.get(4)) ) )  # cap.get(3),(4)은 frame 사이즈 가로,세로

    frame_num = 0
    # 모자이크 시도
    while True:
        ret, img = cap.read()  # 제대로 읽었다면 ret=True, img=읽은 프레임
        frame_num += 1

        if img is None:
            break

        raw_img = img.copy()
        resolution = img.shape  # 읽은 프레임의 shape
        resolution_x = img.shape[1]
        resolution_y = img.shape[0]

        # faces stores list of detected_face and region pair    # detection한 얼굴과 그 위치를 저장
        faces = FaceDetector.detect_faces(
            face_detector, detector_backend, img, align=False
        )

        if len(faces) == 0:
            # face가 없을때
            out.write(raw_img)  # 읽어온 프레임 그대로 출력하기
            continue

        detected_faces = []
        face_index = 0

        # Detected Faces Check & Calculate Distance from Target face    # dection한 faces을 [target과의 거리, 그 위치]를 모두 저장
        for face, (x, y, w, h) in faces:
            if w > 130:  # discard small detected faces
                face_detected = True

                detected_face = img[y: y + h, x: x + w]  # crop detected face

                # -------------------------------------
                detected_face = functions.preprocess_face(  # 그 프레임에서 찾은 사람의 얼굴과 그 위치 담음
                    img=detected_face,  # cropped한 얼굴 넣음
                    target_size=(input_shape_y, input_shape_x),
                    enforce_detection=False,
                    detector_backend="opencv",
                )
                if detected_face.shape[1:3] == input_shape:  #
                    img1_representation = model.predict(detected_face)[0, :]

                    distance = findDistance(distance_metric, img1_rep=img1_representation, img2_rep=embedding[1])

                    detected_faces.append([distance, (x, y, w, h)])
                    face_index = face_index + 1  # 얼굴 하나 찾았다고 더해줌

                # -------------------------------------
        base_img = raw_img.copy()  # 지금의 프레임
        if (
                face_detected == True  # 그 프레임에 얼굴이 있으면 (즉, 아까의 for문을 거쳤다면)
        ):
            target_found = False
            detected_faces_final = detected_faces.copy()
            detected_faces_final.sort()
            for dist, detected_face in detected_faces_final:
                x = detected_face[0]
                y = detected_face[1]
                w = detected_face[2]
                h = detected_face[3]
                current_face = base_img[y: y + h, x: x + w]
                if dist > threshold:  # 닮은 사람이 아니면(딴사람이면)
                    rate = 30  # here blur  # 모자이크 두껍게
                    roi = current_face.copy()
                    roi = cv2.resize(
                        roi, (w // rate, h // rate)
                    )  # 1/rate 비율로 축소
                    # 원래 크기로 확대
                    roi = cv2.resize(
                        roi, (w, h), interpolation=cv2.INTER_AREA
                    )
                    base_img[y: y + h, x: x + w] = roi  # 원본 이미지에 적용
                # -------------------------------
        if frame_num == 1:
            cv2.imwrite(thumnail, base_img)
        out.write(base_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # press q to quit
            break
    toc = time.time()
    print("Convert Video", toc - tic, " seconds")


    # kill open cv things
    cap.release()

    return out


def findDistance(metric, img1_rep, img2_rep):
    distance = 1000  # initialize very large value
    if metric == "cosine":
        distance = dst.findCosineDistance(
            img1_rep, img2_rep
        )
    elif metric == "euclidean":
        distance = dst.findEuclideanDistance(
            img1_rep, img2_rep
        )
    elif metric == "euclidean_l2":
        distance = dst.findEuclideanDistance(
            dst.l2_normalize(img1_rep),
            dst.l2_normalize(img2_rep),
        )

    return distance

def save(writer):
    writer.release()    # 동영상 저장
    cv2.waitKey(0)    # 아무튼 뭔가 눌려야 실행종료(안누르면 안꺼짐)