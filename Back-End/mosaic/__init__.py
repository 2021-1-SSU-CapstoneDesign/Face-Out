from flask import Flask, session, render_template, redirect, request, url_for, flash, send_file
import math
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, QuestionContent, User
from datetime import datetime
import os

engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask( __name__)
# User Web Page

@app.route('/question_delete', methods=['GET','POST'])
def question_delete():
    if request.method == 'POST':

        title = request.args.get('title', '제목')
        category = request.args.get('category', '카테고리')
        content = request.args.get('content', '내용')
        id = request.args.get('id', '아이디')
        date = request.args.get('date', '날짜')
        # filter_by 안에 뭐가 들어가야할지 모르겠음.. 내가 누른 글의 번호를 어떻게 알아내지..?
        # 여기 id 쓰면 돼!!
        q_delete = db_session.query(QuestionContent).filter_by().one()
        db_session.delete(q_delete)
        db_session.commit()
        return redirect('/mypage')
    else:
        return render_template('/user_templates/main.html')

@app.route('/myquestion')
def myquestion():
    #print('들어왔어?')

    title = request.args.get('title', '제목')
    date = request.args.get('date', '날짜')
    category = request.args.get('category', '카테고리')
    content = request.args.get('content', '내용')
    id = request.args.get('id','아이디')
    #print(title)
    #print(id)
    #return redirect('/myquestion')
    return render_template('/user_templates/myquestion.html', title=title, date=date, category=category, content=content, id=id)


@app.route('/myquestion_edit', methods=['GET', 'POST'])
def myquestion_edit():
    edit_question = db_session.query(QuestionContent).filter_by(title=QuestionContent.title).first()
    #return render_template('/user_templates/myquestion_edit.html', title=edit_question.title, category=edit_question.category, content=edit_question.content)
    if request.method == 'post':
        edit_question.create_date=datetime.now()
        if request.form['title'] != edit_question.title:
            edit_question.title = request.form['title']
        if request.form['date'] != edit_question.date:
            edit_question.date = request.form['date']
        if request.form['category'] != edit_question.category:
            edit_question.category = request.form['category']
        if request.form['content'] != edit_question.content:
            edit_question.content = request.form['content']
        db_session.add(edit_question)
        db_session.commit()
        return render_template('/user_templates/main.html')

    title = request.args.get('title', '제목')
    category = request.args.get('category', '카테고리')
    content = request.args.get('content', '내용')
    id = request.args.get('id', '아이디')
    date = request.args.get('date', '날짜')
    #print("id 뭐임?")
    #print(id)
    return render_template('/user_templates/myquestion_edit.html', title=title, category=category,
                           content=content, id=id, date=date)




@app.route('/question_search', methods=['GET','POST'])
def question_search():
    if request.method == 'POST':
        search = request.form['search']
        #search_data = db_session.query(QuestionContent).filter_by(QuestionContent.is_secret==0, QuestionContent.content.in_(search)).all()
        search_data = db_session.query(QuestionContent).filter(QuestionContent.is_secret == 0, QuestionContent.content.ilike(search)).all()
        return redirect('/q&a')
        #return render_template('/user_templates/main.html')
    else:
        return render_template('/user_template/q&a.html')


@app.route('/q_write', methods=['GET','POST'])
def q_write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        create_date = datetime.now()
        # category = request.form['category']
        category = request.form.get('category', False)

        if not category:
            # 하나라도 작성하지 않으면 다시 회원가입 화면
            flash('카테고리를 체크해주세요.')
            return redirect('/q_write')
        newQ = QuestionContent()
        newQ.title = title
        newQ.content = content
        newQ.create_date = create_date
        newQ.category = category

        try:
            if request.form['is_secret']:
                newQ.is_secret = True
        except: newQ.is_secret = False
        info = db_session.query(User).filter_by(u_id=session['u_id']).first()
        newQ.writer = info.u_id

        db_session.add(newQ)
        db_session.commit()

        return redirect('/q&a')
    else:
        return render_template('/user_templates/q_write.html')


@app.route('/q&a', methods=['GET', 'POST'])
def question_notice():
    # 한 페이지당 최대 게시물
    limit = 5
    # 페이지 값
    page = int(request.args.get('page', type=int, default=1))

    # .all() 이 붙은 순간 list가 됨.
    question_list = db_session.query(QuestionContent).all()

    # 게시물 총 개수
    tot_cnt = len(question_list)

    # list를 각 페이지에 맞게 slice 시킴
    # question_list = question_list[((page-1)*limit) : ((page-1)*limit+limit)]
    if page == 1:
        question_list = question_list[-((page - 1) * limit + limit):]
    else:
        question_list = question_list[-((page - 1) * limit + limit):-((page - 1) * limit)]
    #print((page-1)*limit)
    #print((page-1)*limit+limit)

    # 마지막 페이지 수, 반드시 올림 해야 함.
    last_page_num = math.ceil(tot_cnt/limit)

    # 페이지 블럭 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫번째 블럭이라면, block_num=0)
    block_num = int((page-1)/block_size)

    # 현재 블럭의 맨 처음 페이지 넘버 (첫번째 블럭이라면 block_start = 1, 두번째 블럭이라면 block_start = 6)
    block_start = (block_size * block_num)+1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    return render_template('/user_templates/q&a.html', question_list=question_list,
                           limit=limit, page=page, tot_cnt=tot_cnt,
    block_size=block_size, block_num=block_num, block_start=block_start,
    block_end=block_end, last_page_num=last_page_num)


@app.route('/mypage')
def my_page():
    if session.get('u_id'):
        info = db_session.query(User).filter_by(u_id=session['u_id']).first()
        question = db_session.query(QuestionContent).all()
        #writer = info.u_id
        #for i in range(0, len(question)):
            #print(question[i].writer)
        #    if(question[i].writer == info.u_id):
                #print(question[i].writer)
        #        writer=question[i].writer
        #print(writer)


        return render_template('/user_templates/mypage.html', now_uname=info.u_name, now_uphone=info.u_phone,
                               now_uid=info.u_id, now_upw=info.u_pw, writer=info.u_id, question=question)
    else:
        flash('로그인 후 이용가능합니다.')
        return redirect('/login')


@app.route('/myinfo_edit', methods=['GET','POST'])
def myinfo_edit():
    edit = db_session.query(User).filter_by(u_id=session['u_id']).first()
    if request.method == 'GET':
        return render_template('/user_templates/myinfo_edit.html', now_uname=edit.u_name, now_uphone=edit.u_phone, now_uid=edit.u_id, now_upw=edit.u_pw)
    else:
        if request.form['u_name'] != edit.u_name:
            edit.u_name = request.form['u_name']
        if request.form['u_phone'] != edit.u_phone:
            edit.u_phone = request.form['u_phone']
        if request.form['u_id'] != edit.u_id:
            edit.u_id = request.form['u_id']
        if request.form['u_pw'] != edit.u_pw:
            edit.u_pw = request.form['u_pw']
        db_session.add(edit)
        db_session.commit()
        session['u_id'] = edit.u_id
        return redirect('/mypage')
    return render_template('/user_templates/main.html')

@app.route('/mosaic_process')
def video_process():
    return render_template('/user_templates/mosaic_process.html')


# 메인
@app.route('/')
def index():
    return render_template('/user_templates/main.html')


# main.html과 mosaic_process.html에서 버튼 클릭 시 파일 업로드 처리
@app.route('/save_file', methods = ['GET', 'POST'])
def upload_file():
    #print("체크")
    #print(request.method)
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save('./uploads/' + secure_filename(f.filename))
        return render_template('/user_templates/save_file.html')
    else:
        flash('파일을 업로드 해주세요')
        return render_template('/user_templates/main.html')


# save_file.html에서 파일 다운로드 버튼 눌렀을 때 처리
@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    #if request.method == 'GET':
     #   return render_template('/user_templates/save_file.html', files=files)

    if request.method == 'POST':
        print("들어왔나?")
        files = os.listdir("./uploads/")
        sw=0
        for x in files:
            if(x == request.form['file']):
                sw = 1
        print(sw)
        if(sw == 1):
            path = "./uploads/"
            return send_file(path+request.form['file'], attachment_filename=request.form['file'], as_attachment=True)
        else:
            flash('파일 이름을 다시 확인해주세요.')
            return render_template('/user_templates/save_file.html')






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
            flash('입력 양식을 전부 작성해주세요.')
            return render_template('/user_templates/signup.html')
        elif db_session.query(User).filter_by(u_id=u_id).first() is not None:  # ID 조회해서 존재하는 아이디인지 확인
            flash('사용할 수 없는 아이디입니다.')
            return redirect('/signup')
        else:
            userinfo = User()
            userinfo.u_name = u_name
            userinfo.u_phone = u_phone
            userinfo.u_id = u_id
            userinfo.u_pw = u_pw
            db_session.add(userinfo)
            db_session.commit()

            session['u_id'] = u_id
            session['logged_in'] = True

            # 모두 작성하면 login 화면
            return render_template('/user_templates/main.html', logged_in=True)
        return redirect('/')


# 로그인 구현
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/user_templates/login.html')
    else:
        u_id = request.form['u_id']
        u_pw = request.form['u_pw']
        data = db_session.query(User).filter_by(u_id=u_id, u_pw=u_pw).first()  # ID/PW 조회Query 실행
        if data is not None:  # 쿼리 데이터가 존재하면
            session['u_id'] = u_id
            session['logged_in'] = True
            # return "로그인 성공"
            # return render_template('/user_templates/main.html')   # 쿼리 데이터가 있으면 main으로
            return render_template('/user_templates/main.html', logged_in=True)  # 쿼리 데이터가 있으면 main으로
        else:
            # 쿼리 데이터가 없으면 다시 login
            # return "로그인 실패"
            flash('잘못 입력하셨습니다. 다시 로그인해주세요.')
            return redirect('/login')


# 로그아웃 구현
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return render_template('/user_templates/main.html',logged_in=False)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='127.0.0.1', port=5000)