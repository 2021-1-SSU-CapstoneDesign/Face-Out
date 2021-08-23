from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Question, QuestionContent, User

engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask( __name__)
# User Web Page



@app.route('/question')
def question():
    return render_template('/user_templates/question.html')

#@app.route('/save_video')
#def save_video():
#    return render_template('/user_templates/save_video.html')

@app.route('/q_write')
def q_write():
    return render_template('/user_templates/q_write.html')

@app.route('/mypage')
def my_page():
    return render_template('/user_templates/mypage.html')

@app.route('/mosaic_process')
def video_process():
    return render_template('/user_templates/mosaic_process.html')


@app.route('/q&a')
def question_notice():
    return render_template('/user_templates/q&a.html')

# 파일 업로드
@app.route('/')
def index():
    return render_template('/user_templates/main.html')

# 파일 업로드 처리
@app.route('/save_video', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save(secure_filename(f.filename))
        return render_template('/user_templates/save_video.html')


# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('/user_templates/signup.html')
    else:
        u_name = request.form.get('u_name', False)
        u_phone = request.form.get('u_phone', False)
        u_id = request.form.get('u_id', False)
        u_pw = request.form.get('u_pw', False)

        if not (u_name and u_phone and u_id and u_pw):
            # 하나라도 작성하지 않으면 다시 회원가입 화면
            return render_template('/user_templates/signup.html')
        elif session.query(User).filter_by(u_id=u_id).first() is not None:  # ID 조회해서 존재하는 아이디인지 확인
            return '사용할 수 없는 아이디입니다.'
        else:
            userinfo = User()
            userinfo.u_name = u_name
            userinfo.u_phone = u_phone
            userinfo.u_id = u_id
            userinfo.u_pw = u_pw
            session.add(userinfo)
            session.commit()

            # 모두 작성하면 login 화면
            return render_template('/user_templates/login.html')
        return redirect('/')



# 로그인 구현
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/user_templates/login.html')
    else:
        u_id = request.form['u_id']
        u_pw = request.form['u_pw']
        try:
            data = session.query(User).filter_by(u_id=u_id, u_pw=u_pw).first()  # ID/PW 조회Query 실행
            if data is not None:  # 쿼리 데이터가 존재하면
                #session['u_id'] = u_id  # id를 session에 저장한다.
                #return "로그인 성공"
                return render_template('/user_templates/main.html')   # 쿼리 데이터가 있으면 main으로
            else:
                # 쿼리 데이터가 없으면 다시 login
                #return "로그인 실패"
                return render_template('/user_templates/login.html')
        except: # 예외 상황 발생시
            #print('u_id:', u_id, ' u_pw:', u_pw)
            #return "예외상황.."
            return render_template('/user_templates/login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)