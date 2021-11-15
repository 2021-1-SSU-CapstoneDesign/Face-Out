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
    db_path,    # target으로 들어온 jpg이미지 넣는 곳
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
    if os.path.isfile(db_path) == True:
        employee = db_path
    else:
        print(
            "WARNING: There is no image in this path ( ",
            db_path,
            ") . Face recognition will not be performed.",
        )
        exit()

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

    # 모자이크 시도
    while True:
        ret, img = cap.read()    # 제대로 읽었다면 ret=True, img=읽은 프레임

        if img is None:
            break

        raw_img = img.copy()
        resolution = img.shape    # 읽은 프레임의 shape
        resolution_x = img.shape[1]
        resolution_y = img.shape[0]

        # faces stores list of detected_face and region pair    # detection한 얼굴과 그 위치를 저장
        faces = FaceDetector.detect_faces(
            face_detector, detector_backend, img, align=False
        )

        if len(faces) == 0:
            # face가 없을때
            out.write(raw_img)    # 읽어온 프레임 그대로 출력하기
            continue

        detected_faces = []
        face_index = 0
        
        # Detected Faces Check & Calculate Distance from Target face    # dection한 faces을 [target과의 거리, 그 위치]를 모두 저장
        for face, (x, y, w, h) in faces:
            if w > 130:  # discard small detected faces

                face_detected = True

                detected_face = img[y : y + h, x : x + w]  # crop detected face

                # -------------------------------------
                detected_face = functions.preprocess_face(    # 그 프레임에서 찾은 사람의 얼굴과 그 위치 담음
                    img=detected_face,    # cropped한 얼굴 넣음
                    target_size=(input_shape_y, input_shape_x),
                    enforce_detection=False,
                    detector_backend="opencv",
                )
                if detected_face.shape[1:3] == input_shape:  # 
                    img1_representation = model.predict(detected_face)[0, :]
                    
                    distance = findDistance(distance_metric, img1_rep=img1_representation, img2_rep=embedding[1])

                    detected_faces.append([distance, (x, y, w, h)])
                    face_index = face_index + 1    # 얼굴 하나 찾았다고 더해줌

                # -------------------------------------
        base_img = raw_img.copy()    # 지금의 프레임
        if (
            face_detected == True    # 그 프레임에 얼굴이 있으면 (즉, 아까의 for문을 거쳤다면)
        ):
            target_found = False
            detected_faces_final = detected_faces.copy()
            detected_faces_final.sort()
            for dist, detected_face in detected_faces_final:
                x = detected_face[0]
                y = detected_face[1]
                w = detected_face[2]
                h = detected_face[3]
                current_face = base_img[y : y + h, x : x + w]
                # cv2.rectangle(
                #     base_img, (x, y), (x + w, y + h), (67, 67, 67), 1
                # )  # draw rectangle to main image
                
                if dist <= threshold and not target_found:    # 닮은 사람을 찾으면
                    display_img = cv2.imread(embedding[0])    # target얼굴 가져옴
                    display_img = cv2.resize(    # target얼굴을 resize
                        display_img, (pivot_img_size, pivot_img_size)
                    )

                    label = embedding[0].split("/")[-1].replace(
                        ".jpg", ""
                    )
                    label = re.sub("[0-9]", "", label)
                    try:    # 원래 코드가 인물 찾으면 target얼굴을 옆에 붙여줌  # 찾은 얼굴 위치에따라 어디다가 target얼굴을 붙일지 정하는 코드
                        if (
                            y - pivot_img_size > 0
                            and x + w + pivot_img_size < resolution_x
                        ):
                            # top right
                            # base_img[
                            #     y - pivot_img_size : y,
                            #     x + w : x + w + pivot_img_size,
                            # ] = display_img

                            overlay = base_img.copy()
                            opacity = 0.4
                            # cv2.rectangle(
                            #     base_img,
                            #     (x + w, y),
                            #     (x + w + pivot_img_size, y + 20),
                            #     (46, 200, 255),
                            #     cv2.FILLED,
                            # )
                            # cv2.addWeighted(
                            #     overlay,
                            #     opacity,
                            #     base_img,
                            #     1 - opacity,
                            #     0,
                            #     base_img,
                            # )

                            # cv2.putText(
                            #     base_img,
                            #     label,
                            #     (x + w, y + 10),
                            #     cv2.FONT_HERSHEY_SIMPLEX,
                            #     0.5,
                            #     text_color,
                            #     1,
                            # )

                            # connect face and text  # 
                            # cv2.line(
                            #     base_img,
                            #     (x + int(w / 2), y),
                            #     (
                            #         x + 3 * int(w / 4),
                            #         y - int(pivot_img_size / 2),
                            #     ),
                            #     (67, 67, 67),
                            #     1,
                            # )
                            # cv2.line(
                            #     base_img,
                            #     (
                            #         x + 3 * int(w / 4),
                            #         y - int(pivot_img_size / 2),
                            #     ),
                            #     (x + w, y - int(pivot_img_size / 2)),
                            #     (67, 67, 67),
                            #     1,
                            # )

                        elif (
                            y + h + pivot_img_size < resolution_y
                            and x - pivot_img_size > 0
                        ):
                            # bottom left
                            # base_img[
                            #     y + h : y + h + pivot_img_size,
                            #     x - pivot_img_size : x,
                            # ] = display_img

                            overlay = base_img.copy()
                            opacity = 0.4
                            # cv2.rectangle(
                            #     base_img,
                            #     (x - pivot_img_size, y + h - 20),
                            #     (x, y + h),
                            #     (46, 200, 255),
                            #     cv2.FILLED,
                            # )
                            # cv2.addWeighted(
                            #     overlay,
                            #     opacity,
                            #     base_img,
                            #     1 - opacity,
                            #     0,
                            #     base_img,
                            # )

                            # cv2.putText(
                            #     base_img,
                            #     label,
                            #     (x - pivot_img_size, y + h - 10),
                            #     cv2.FONT_HERSHEY_SIMPLEX,
                            #     0.5,
                            #     text_color,
                            #     1,
                            # )

                            # connect face and text
                            # cv2.line(
                            #     base_img,
                            #     (x + int(w / 2), y + h),
                            #     (
                            #         x + int(w / 2) - int(w / 4),
                            #         y + h + int(pivot_img_size / 2),
                            #     ),
                            #     (67, 67, 67),
                            #     1,
                            # )
                            # cv2.line(
                            #     base_img,
                            #     (
                            #         x + int(w / 2) - int(w / 4),
                            #         y + h + int(pivot_img_size / 2),
                            #     ),
                            #     (x, y + h + int(pivot_img_size / 2)),
                            #     (67, 67, 67),
                            #     1,
                            # )

                        elif (
                            y - pivot_img_size > 0
                            and x - pivot_img_size > 0
                        ):
                            # top left
                            # base_img[
                            #     y - pivot_img_size : y,
                            #     x - pivot_img_size : x,
                            # ] = display_img

                            overlay = base_img.copy()
                            opacity = 0.4
                            # cv2.rectangle(
                            #     base_img,
                            #     (x - pivot_img_size, y),
                            #     (x, y + 20),
                            #     (46, 200, 255),
                            #     cv2.FILLED,
                            # )
                            # cv2.addWeighted(
                            #     overlay,
                            #     opacity,
                            #     base_img,
                            #     1 - opacity,
                            #     0,
                            #     base_img,
                            # )

                            # cv2.putText(
                            #     base_img,
                            #     label,
                            #     (x - pivot_img_size, y + 10),
                            #     cv2.FONT_HERSHEY_SIMPLEX,
                            #     0.5,
                            #     text_color,
                            #     1,
                            # )

                            # connect face and text
                            # cv2.line(
                            #     base_img,
                            #     (x + int(w / 2), y),
                            #     (
                            #         x + int(w / 2) - int(w / 4),
                            #         y - int(pivot_img_size / 2),
                            #     ),
                            #     (67, 67, 67),
                            #     1,
                            # )
                            # cv2.line(
                            #     base_img,
                            #     (
                            #         x + int(w / 2) - int(w / 4),
                            #         y - int(pivot_img_size / 2),
                            #     ),
                            #     (x, y - int(pivot_img_size / 2)),
                            #     (67, 67, 67),
                            #     1,
                            # )

                        elif (
                            x + w + pivot_img_size < resolution_x
                            and y + h + pivot_img_size < resolution_y
                        ):
                            # bottom righ
                            # base_img[
                            #     y + h : y + h + pivot_img_size,
                            #     x + w : x + w + pivot_img_size,
                            # ] = display_img

                            overlay = base_img.copy()
                            opacity = 0.4
                            # cv2.rectangle(
                            #     base_img,
                            #     (x + w, y + h - 20),
                            #     (x + w + pivot_img_size, y + h),
                            #     (46, 200, 255),
                            #     cv2.FILLED,
                            # )
                            # cv2.addWeighted(
                            #     overlay,
                            #     opacity,
                            #     base_img,
                            #     1 - opacity,
                            #     0,
                            #     base_img,
                            # )

                            # cv2.putText(
                            #     base_img,
                            #     label,
                            #     (x + w, y + h - 10),
                            #     cv2.FONT_HERSHEY_SIMPLEX,
                            #     0.5,
                            #     text_color,
                            #     1,
                            # )

                            # connect face and text
                            # cv2.line(
                            #     base_img,
                            #     (x + int(w / 2), y + h),
                            #     (
                            #         x + int(w / 2) + int(w / 4),
                            #         y + h + int(pivot_img_size / 2),
                            #     ),
                            #     (67, 67, 67),
                            #     1,
                            # )
                            # cv2.line(
                            #     base_img,
                            #     (
                            #         x + int(w / 2) + int(w / 4),
                            #         y + h + int(pivot_img_size / 2),
                            #     ),
                            #     (
                            #         x + w,
                            #         y + h + int(pivot_img_size / 2),
                            #     ),
                            #     (67, 67, 67),
                            #     1,
                            # )
                    except Exception as err:
                        print(str(err))
                else:    # 닮은 사람이 아니면(딴사람이면)
                    # here blur  # 모자이크 두껍게
                    rate = 30
                    roi = current_face.copy()
                    roi = cv2.resize(
                        roi, (w // rate, h // rate)
                    )  # 1/rate 비율로 축소
                    # 원래 크기로 확대
                    roi = cv2.resize(
                        roi, (w, h), interpolation=cv2.INTER_AREA
                    )
                    base_img[y : y + h, x : x + w] = roi  # 원본 이미지에 적용
                # -------------------------------
        out.write(base_img)
        print(out)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):  # press q to quit
            break
    toc = time.time()
    print("Convert Video", toc - tic, " seconds")
    

    # kill open cv things
    cap.release()
    cv2.destroyAllWindows()

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

if __name__ == "__main__":
    # analysis(db_path=db_path, source=source)
    # VGG-Face: 3seconds video -> 8 seconds / 7seconds video -> 125 seconds
    # analysis(db_path=db_path, source=source, output_path='videos/test_vgg_7seconds.mp4', model_name='VGG-Face')
    # FaceNet: 3seconds video ->  seconds / 7 seconds video ->  84 seconds
    # +ssd: 7 seconds video ->  55 seconds
    
    parser = argparse.ArgumentParser(description='Need Target Face Image & Video')
    parser.add_argument('--target', help='Need Target Face(No Bluring Face Image)')
    parser.add_argument('--video', help='Video for Converting')
    parser.add_argument('--output', help='output Path')

    args = parser.parse_args()
    target = args.target
    video = args.video
    output = args.output
    main(db_path=target, source=video, output_path=output, model_name='Facenet', detector_backend='ssd')