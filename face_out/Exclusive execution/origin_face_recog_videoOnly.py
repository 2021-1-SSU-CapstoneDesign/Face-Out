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


def main(
        output_path="videos/results.avi",
        model_name="VGG-Face",  # 이미지 비교에 사용 (우리는 FaceNet사용)
        detector_backend="opencv",  # 네모박스 찾는 detection에 사용 (우리는 ssd사용)
        distance_metric="cosine",  # 거리 비교 metric
        source=0,  # video file을 불러옴
):
    # ------------------------

    face_detector = FaceDetector.build_model(detector_backend)  # 우리는 ssd사용
    print("Detector backend is ", detector_backend)

    # ------------------------
    filename = output_path
    fc = 20  # 초당 저장할 frame

    input_shape = (224, 224)
    input_shape_x = input_shape[0]
    input_shape_y = input_shape[1]

    text_color = (255, 255, 255)

    model = DeepFace.build_model(model_name)  # 우리는 FaceNet사용
    print(model_name, " is built")

    # ------------------------

    input_shape = functions.find_input_shape(model)
    input_shape_x = input_shape[0]
    input_shape_y = input_shape[1]

    # -----------------------

    pivot_img_size = 112  # face recognition result image

    # -----------------------
    face_detected = False
    tic = time.time()

    cap = cv2.VideoCapture(source)  # webcam
    codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")  # 디지털 미디어 포맷 코드를 생성(인코딩 방식을 설정)
    out = cv2.VideoWriter(filename, codec, fc, (int(cap.get(3)), int(cap.get(4))))  # cap.get(3),(4)은 frame 사이즈 가로,세로

    frame_num = 0
    # 모자이크 시도
    while True:
        ret, img = cap.read()  # 제대로 읽었다면 ret=True, img=읽은 프레임
        frame_num += 1

        if img is None:
            break

        raw_img = img.copy()

        # faces stores list of detected_face and region pair    # detection한 얼굴과 그 위치를 저장
        faces = FaceDetector.detect_faces(
            face_detector, detector_backend, img, align=False
        )

        if len(faces) == 0:
            # face가 없을때
            out.write(raw_img)  # 읽어온 프레임 그대로 출력하기
            continue

        base_img = raw_img.copy()  # 지금의 프레임

        for face, (x, y, w, h) in faces:
            current_face = base_img[y: y + h, x: x + w]
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
        if frame_num == 1:  # 첫번째 프레임이면 썸네일에 쓸 이미지 저장
            cv2.imwrite("./first_frame_only.png", base_img)

        out.write(base_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # press q to quit
            break
    toc = time.time()
    print("Convert Video", toc - tic, " seconds")

    # kill open cv things
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # analysis(db_path=db_path, source=source)
    # VGG-Face: 3seconds video -> 8 seconds / 7seconds video -> 125 seconds
    # analysis(db_path=db_path, source=source, output_path='videos/test_vgg_7seconds.mp4', model_name='VGG-Face')
    # FaceNet: 3seconds video ->  seconds / 7 seconds video ->  84 seconds
    # +ssd: 7 seconds video ->  55 seconds

    parser = argparse.ArgumentParser(description='Need Target Face Image & Video')
    # parser.add_argument('--target', help='Need Target Face(No Bluring Face Image)')
    parser.add_argument('--video', help='Video for Converting')
    parser.add_argument('--output', help='output Path')

    args = parser.parse_args()
    # target = args.target
    video = args.video
    output = args.output
    main(source=video, output_path=output, model_name='Facenet', detector_backend='ssd')