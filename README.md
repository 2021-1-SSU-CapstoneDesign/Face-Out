# Face Out : 얼굴 인식을 통한 사람 얼굴 모자이크 처리 웹


<br>

## 🚩 목차
#### 1.&nbsp; &nbsp;[참여자 역할](#1-참여자-역할-1)
#### 2.&nbsp; &nbsp;[프로젝트 설명](#2-프로젝트-설명-1)
#### 3.&nbsp; &nbsp;[수행 내용](#3-수행-내용-1)
#### 4.&nbsp; &nbsp;[기대 효과](#4-기대효과)
#### 5.&nbsp; &nbsp;[Dir & File 설명](#5-dir--file-설명-1)


<br><br>

## 1. 참여자 역할
최서윤|길다영|송선영
--|--|--
Web FrontEnd 구상 & Face Recognition Model|Web Front-End & Back-End & Face Recognition Model Request|Web Front-End & Back-End & DataBase


<br><br>

## 2. 프로젝트 설명
- Face Recognition을 통해 지정된 사람을 제외한 다른 사람들의 얼굴을 모자이크 처리하는 시스템.
- 사용자들이 모자이크 처리 시스템을 이용할 수 있도록 웹 서비스 제작
 
- 촬영된 영상에서 특정 인물 이외의 인물들을 모자이크 가능
- 유튜버와 같은 크리에이터들이 많이 생겨나면서 미처 모자이크 처리되지 못한 사람들의 초상권 보호



<br><br>

## 3. 수행 내용
### 🚥 웹페이지 구현도
웹페이지 구현도 | 실제 구현된 웹페이지
--|--
<img src="https://user-images.githubusercontent.com/53934639/132503608-99861563-1776-4216-b693-5744413de5dc.png" style="width:700px">|<img width="717" src="https://user-images.githubusercontent.com/53934639/132512594-1ea32147-9a2c-4336-a97f-7370798cddc6.png" algin="right">


<br>

### 🚥 전체 구성도
- 서버는 Flask, DB는 MySQL로 제작.

- Flask에서 MySQL을 사용하기 위해 Flask-sqlalchemy을 사용.

<p align="center">
<img src="https://user-images.githubusercontent.com/53934639/132503660-42668add-d651-49aa-b9a3-608eeb51bdfb.png" style="width:600px"></p>

<br>

### 🚥 모자이크 처리
<p align="center">

모자이크에서 제외할 인물 사진 | 모자이크 처리할 사진 | 모자이크 결과
--|--|--
<img src="https://user-images.githubusercontent.com/53934639/132504867-205ba54b-6d2e-45c1-a0a8-bf76fba9c7de.jpg" style="width:200px">|<img src="https://user-images.githubusercontent.com/53934639/132505221-d3d7633b-991d-4e84-8c42-5cc0f1f16e33.gif" style="width:300px">|<img src="https://user-images.githubusercontent.com/53934639/132505377-85f82766-1ce4-4064-ac22-a483a9c42347.gif" style="width:300px">
<img src="https://user-images.githubusercontent.com/53934639/132506099-815d0e77-ad03-4e3b-b114-05c71b4c857c.jpg" style="width:200px">|<img src="https://user-images.githubusercontent.com/53934639/132506126-7ec4b8b4-04a8-4ded-8bf0-8c30db99c9c6.jpg" style="width:200px">|<img src="https://user-images.githubusercontent.com/53934639/132506143-63ca4833-cbd9-4bdd-9c22-8c90ae4df701.jpg" style="width:200px">

<br><br>

## 4. 기대효과
- 모자이크 처리 제외 사진 1장만 넣어도 자동으로 모자이크 처리가 된다.
  
- 어플을 따로 다운받지 않아도 웹에서 서비스를 이용할 수 있다.
- 홈페이지에 모자이크한 사진 또는 영상을 보관 가능하다.
- 사람 얼굴이라는 특정부분만을 모자이크 처리할 수 있다.
- 모자이크를 하고자 하는 사람이 다수일 경우, 한번의 클릭으로 빠르게 사람 얼굴을 모자이크할 수 있다.


<br><br>

## 5. Dir & File 설명
<img src="https://user-images.githubusercontent.com/53934639/141782126-523d5b73-8303-40d0-af5a-bb3a5fc5f8c9.png" style="width:350px">|<p align="left">- init.py : DB와 연동하여 웹 사이트의 기능들을 정의한 함수와 얼굴인식 모델을 처리하는 함수를 정의<br> - database_setup.py : DB Table 설정 <br> - face_recog.py : 얼굴 인식 코드 <br> - face_recog_image.py : 모자이크에서 제외할 얼굴사진과 단체 사진 인식 후 모자이크 처리 코드 <br> - face_recog_imgaeOnly.py : 단체 사진 인식 후 인식된 전체 얼굴 모자이크 처리 코드 <br> - face_recog_video.py : 모자이크에서 제외할 얼굴사진과 단체 영상 인식 후 모자이크 처리 코드 <br> - face_recog_videoOnly.py : 단체 영상 인식 후 인식된 전체 얼굴 모자이크 처리 코드 <br> - new_face_recog_video.py & new_face_recog_videoOnly.py : 기존 영상 처리속도보다 속도를 개선한 코드</p>
--|--
![image](https://user-images.githubusercontent.com/53934639/132510584-79471bc3-14cb-42ab-9adb-ab2194768c50.png)|<p align="left">**- input_uploads : 웹에서 input으로 주어지는 모자이크에서 제외할 얼굴 사진을 저장. <br> - output_uploads : 웹에서 input으로 주어지는 모자이크 할 단체 사진 또는 영상을 저장. <br> - downloads : 비회원인 경우, 모자이크 처리 결과를 저장. <br> - member_img_downloads : 회원인 경우, 모자이크 처리 결과 중 사진을 저장. <br> - member_video_downloads : 회원인 경우, 모자이크 처리 결과 중 영상을 저장. <br> - thumnail : a모자이크 처리가 된 영상에서 썸네일을 저장 <br> (이미지와 영상을 모자이크 처리하는 코드가 다르고, 영상의 경우 썸네일을 만들어주어야 하기에 따로 dir을 만들어 저장하였음.)**</p>
![image](https://user-images.githubusercontent.com/53934639/132510683-0848a224-257a-43cb-aa5f-a8df9a0b9d9d.png)|<p align="left">**- login.html : 로그인 페이지 <br> - main.html : 메인 페이지, input으로 받은 파일들을 업로드, 모자이크 처리 방법 설명. <br> - mosaic_process.html : 모자이크 처리 페이지, 메인 페이지와 같은 기능. <br> - myinfo_edit.html : 회원인 경우, '내 정보'를 수정하는 페이지 <br> - mypage.html : 회원인 경우, '내 정보', 모자이크 처리된 결과 저장, '내 q&a' 볼 수 있음. <br> - myquestion_edit.html : '내 q&a' 수정하는 페이지 <br> - q&a.html : q&a 페이지 <br> - q_write.html : q&a에서 새 글 작성하는 페이지 <br> - question.html : q&a에서 글 클릭 시 나타나는 자세한 내용 페이지, 회원인 경우 댓글 작성 가능 <br> - save_file.html : 모자이크 처리된 결과를 기기에 다운로드 받거나 마이페이지에 저장하는 페이지 <br> - signup.html : 회원가입 페이지**</p>
![image](https://user-images.githubusercontent.com/53934639/141784010-b1a23068-eb11-499c-99cb-e4b0ad749f11.png)|<p align="left">**- 단독으로 실행되는 모자이크 처리 코드**</p>

<br><br>























