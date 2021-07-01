# Face Out - Web PART
<br>

- 2021.5 - 2021.9
- **'동영상에서 지정된 사람을 제외한 나머지 사람들을 모자이크 처리해주는 웹 사이트'** 프로젝트 중 **웹 부분** 구현.
- [점프 투 플라스크](https://wikidocs.net/81085)를 참고하여 프로젝트를 진행함.


<br>

## 역할
- Flask Web : 길다영
- MySQL : 송선영

<br>

## 목차
- [1. Flask 개발 환경 설정](#1-flask-개발-환경-설정)
- [2. Flask 실행 방법](#2-flask-실행-방법)
- [3. Front-End](#3-front-end)
  - [03-1. User Templates](#3-1-user-templates)
  - [03-2. Manager Templates](#3-2-manager-templates)
- [4. 프로젝트 구조](#4-프로젝트-구조)

<br>

----

<br>

## 1. Flask 개발 환경 설정
1) python과 pycharm 설치

2) Flask 개발 환경 만들기

순서|코드
--|--
가상 환경 디렉터리 생성 | <img src="https://user-images.githubusercontent.com/53934639/124146671-f4c81600-dac8-11eb-9419-39037d214259.png">
가상 환경 만들기 | ```C:\venvs> python -m venv mosaic_web_project```
가상 환경 진입 | ```C:\venvs> cd C:\venvs\mosaic_web_project\Scripts```<br>```C:\venvs\mosaic_web_project\Scripts> activate ```<br> ```(mosaic_web_project) C:\venvs\mosaic_web_project\Scripts>```
가상 환경에서 플라스크 설치 | ```(mosaic_web_project) C:\venvs\mosaic_web_project\Scripts> pip install Flask```
pip 최신 버전 설치 | ```(mosaic_web_project) C:\venvs\mosaic_web_project\Scripts> python -m pip install --upgrade pip```
프로젝트 루트 디렉터리 생성 | ```C:\> mkdir mosaic_web```<br>```C:\> cd mosaic_web```
플라스크 프로젝트를 담을 디렉터리 생성 후 이동 |  ```C:\venvs\mosaic_web_project\Scripts> activate ``` <br>  ```(mosaic_web_project) C:\mosaic_web> mkdir mosaic_web_project ```
배치 파일 생성 | [링크](https://wikidocs.net/81042) 참고하여 배치 파일 생성 후 실행하여 가상 환경 진입까지 진행.<br> projects -> mosaic_web, myproject -> mosaic_web_project 로 바꾸어 진행.

3) mosaic_web_project 디렉터리에 ./Back-End/mosaic 폴더를 삽입.

<br><br>

## 2. Flask 실행 방법
```
flask run
```
<br>
다음과 같은 에러 발생 시, 아래 코드 실행.

![image](https://user-images.githubusercontent.com/53934639/124149887-fb0bc180-dacb-11eb-83ee-35e85aef3753.png)

```
FLASK_APP=mosaic
```
```
FLASK_ENV=development
```

<br><br>

## 3. Front-End
- 웹에 나타나는 페이지들.
- 크게 사용자 템플릿과 관리자 템플릿으로 나뉨.

### 3-1. User Templates
- [main.html](./Back-End/mosaic/templates/user_templates/main.html) : 메인 페이지
- [mosaic_process.html](./Back-End/mosaic/templates/user_templates/mosaic_process.html) : 모자이크 처리 페이지
- [save_video.html](./Back-End/mosaic/templates/user_templates/save_video.html) : 모자이크 처리된 동영상 저장 또는 다운로드 하는 페이지
- [login.html](./Back-End/mosaic/templates/user_templates/login.html) : 로그인 페이지
- [signup.html](./Back-End/mosaic/templates/user_templates/signup.html) : 회원가입 페이지
- [mypage.html](./Back-End/mosaic/templates/user_templates/mypage.html) : 마이페이지
- [q&a.html](./Back-End/mosaic/templates/user_templates/q&a.html) : Q&A 페이지
- [q_write.html](./Back-End/mosaic/templates/user_templates/q_write.html) : Question 작성하는 페이지
- [question.html](./Back-End/mosaic/templates/user_templates/question.html) : 작성된 Question 보여주는 페이지

### 3-2. Manager Templates



<br><br>

## 4. 프로젝트 구조

- **static** : css, js 파일 <br><img src="https://user-images.githubusercontent.com/53934639/124150658-b6345a80-dacc-11eb-9ce4-f4c0fe5eb78a.png" align="right"> 
- **templates** : html 파일 <br>
- **views** : 화면 구성 <br>
  - **main_views.py** : 유지보수를 좋게 하기 위해 render_templates() 함수를 이용하여 html 렌더링함. <img src="https://user-images.githubusercontent.com/53934639/124151464-8a65a480-dacd-11eb-94fe-fea6372ab6e6.png" width = "500px" align="left">
























