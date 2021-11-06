from flask import Flask, session, render_template, redirect, request, url_for, flash, send_file
import math
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, QuestionContent, User, ImageInfo, Comment
from datetime import datetime
import face_recog_image
import face_recog_video
import face_recog_imageOnly
import face_recog_videoOnly
import os

engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask( __name__)
# User Web Page

@app.route('/question_delete', methods=['GET','POST'])
def question_delete():
    id = request.args.get('id', '아이디')
    q_delete = db_session.query(QuestionContent).filter_by(id=id).first()
    if q_delete:
        db_session.delete(q_delete)

        db_session.commit()
        flash('글이 삭제되었습니다.')
        return redirect('/mypage')

    else:
        return render_template('/user_templates/main.html')


@app.route('/myquestion_edit', methods=['GET', 'POST'])
def myquestion_edit():

    title = request.args.get('title', '제목')
    category = request.args.get('category', '카테고리')
    content = request.args.get('content', '내용')
    id = request.args.get('id', '아이디')
    date = request.args.get('date', '날짜')
    edit_question = db_session.query(QuestionContent).filter_by(id=id).first()

    comment_list = db_session.query(Comment).filter_by(question_id=id).all()

    if request.method == 'POST':
        #print(request.form['content'])
        if edit_question:
            edit_question.create_date=datetime.now()

            if request.form['now_title'] != edit_question.title:
                edit_question.title = request.form['now_title']
            if request.form['now_content'] != edit_question.content:
                edit_question.content = request.form['now_content']
            db_session.add(edit_question)
            db_session.commit()

        return render_template('/user_templates/question.html',
                               title=edit_question.title, date=edit_question.create_date, category=category, content=edit_question.content, comment_list=comment_list)
    else:
        return render_template('/user_templates/myquestion_edit.html', title=title, category=category,
                           content=content, id=id, date=date)


@app.route('/category_search', methods=['GET','POST'])
def category_search():

    #category = request.args.get('category', '카테고리')
    #print(category)
    # 이렇게 하면 category는 올바르게 나오거든 근데 request.method가 post가 아닌걸로 나와!

    #if request.method == 'POST':

        category = request.args.get('category', '카테고리')
        print(category)
        # 한 페이지당 최대 게시물
        limit = 5
        # 페이지 값
        page = int(request.args.get('page', type=int, default=1))

        question_list = db_session.query(QuestionContent).filter(QuestionContent.is_secret == 0, QuestionContent.category == category).all()
# 게시물 총 개수
        tot_cnt = len(question_list)

        # list를 각 페이지에 맞게 slice 시킴
        # question_list = question_list[((page-1)*limit) : ((page-1)*limit+limit)]
        if page == 1:
            question_list = question_list[-((page - 1) * limit + limit):]
        else:
            question_list = question_list[-((page - 1) * limit + limit):-((page - 1) * limit)]
        # print((page-1)*limit)
        # print((page-1)*limit+limit)

        # 마지막 페이지 수, 반드시 올림 해야 함.
        last_page_num = math.ceil(tot_cnt / limit)

        # 페이지 블럭 5개씩 표기
        block_size = 5
        # 현재 블럭의 위치 (첫번째 블럭이라면, block_num=0)
        block_num = int((page - 1) / block_size)

        # 현재 블럭의 맨 처음 페이지 넘버 (첫번째 블럭이라면 block_start = 1, 두번째 블럭이라면 block_start = 6)
        block_start = (block_size * block_num) + 1
        # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
        block_end = block_start + (block_size - 1)

        return render_template('/user_templates/q&a.html', question_list=question_list,
                               limit=limit, page=page, tot_cnt=tot_cnt,
                               block_size=block_size, block_num=block_num, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num,now_user=session['u_id'])
    #else:
     #   return render_template('/user_templates/q&a.html')

@app.route('/question_search', methods=['GET','POST'])
def question_search():
    if request.method == 'POST':
        search = request.form['search']
        #search_data = db_session.query(QuestionContent).filter_by(QuestionContent.is_secret==0, QuestionContent.content.in_(search)).all()
        #search_data = db_session.query(QuestionContent).filter(QuestionContent.is_secret == 0, QuestionContent.content.ilike(search)).all()

        # 한 페이지당 최대 게시물
        limit = 5
        # 페이지 값
        page = int(request.args.get('page', type=int, default=1))

        # .all() 이 붙은 순간 list가 됨.
        question_list = []
        content_list = db_session.query(QuestionContent).filter(QuestionContent.is_secret == 0).all()
        for i in content_list:
            if search in i.content:
                question_list.append(i)
        #question_list = db_session.query(QuestionContent).filter(QuestionContent.is_secret == 0, QuestionContent.content.ilike(search)).all()

        # 게시물 총 개수
        tot_cnt = len(question_list)

        # list를 각 페이지에 맞게 slice 시킴
        # question_list = question_list[((page-1)*limit) : ((page-1)*limit+limit)]
        if page == 1:
            question_list = question_list[-((page - 1) * limit + limit):]
        else:
            question_list = question_list[-((page - 1) * limit + limit):-((page - 1) * limit)]
        # print((page-1)*limit)
        # print((page-1)*limit+limit)

        # 마지막 페이지 수, 반드시 올림 해야 함.
        last_page_num = math.ceil(tot_cnt / limit)

        # 페이지 블럭 5개씩 표기
        block_size = 5
        # 현재 블럭의 위치 (첫번째 블럭이라면, block_num=0)
        block_num = int((page - 1) / block_size)

        # 현재 블럭의 맨 처음 페이지 넘버 (첫번째 블럭이라면 block_start = 1, 두번째 블럭이라면 block_start = 6)
        block_start = (block_size * block_num) + 1
        # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
        block_end = block_start + (block_size - 1)
        if session.get('u_id'):
            return render_template('/user_templates/q&a.html', question_list=question_list,
                               limit=limit, page=page, tot_cnt=tot_cnt,
                               block_size=block_size, block_num=block_num, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num, now_user=session['u_id'])
        else:
            return render_template('/user_templates/q&a.html', question_list=question_list,
                                   limit=limit, page=page, tot_cnt=tot_cnt,
                                   block_size=block_size, block_num=block_num, block_start=block_start,
                                   block_end=block_end, last_page_num=last_page_num)
    #return render_template('/user_templates/q&a.html', question_list=search_data)
    else:
        return render_template('/user_template/q&a.html')



@app.route('/question', methods=['GET', 'POST'])
def question():
    title = request.args.get('title', '제목')
    category = request.args.get('category', '카테고리')
    content = request.args.get('content', '내용')
    id = request.args.get('id', '아이디')
    date = request.args.get('date', '날짜')
    writer = request.args.get('writer', '글쓴이')

    comment_list = db_session.query(Comment).filter_by(question_id=id).all()

    if not session.get('u_id'):
        return render_template('/user_templates/question.html', title=title, date=date, category=category,
                               content=content, id=id,  writer=writer, comment_list=comment_list)
    else:
        # 댓글 추가
        if request.method == 'POST':
            comment_content = request.form['content']
            if len(comment_content) > 300:
                flash("댓글제한수를 넘겼습니다. 300자 이하로 다시 입력해주세요.")
                return render_template('/user_templates/question.html', title=title, date=date, category=category,
                                   content=content,
                                   id=id, now_user=session['u_id'], writer=writer, comment_list=comment_list)
            else:
                new_comment = Comment(comment_content=comment_content, commenter=session['u_id'], question_id=id)
                db_session.add(new_comment)
                db_session.commit()
                comment_list = db_session.query(Comment).filter_by(question_id=id).all()
                return render_template('/user_templates/question.html', title=title, date=date, category=category,
                           content=content, id=id, now_user=session['u_id'], writer=writer, comment_list=comment_list)
        else:
            return render_template('/user_templates/question.html', title=title, date=date, category=category, content=content,
                               id=id, now_user=session['u_id'], writer=writer, comment_list=comment_list)



@app.route('/comment_delete', methods=['GET','POST'])
def comment_delete():
    title = request.args.get('title', '제목')
    category = request.args.get('category', '카테고리')
    content = request.args.get('content', '내용')
    id = request.args.get('id', '아이디')
    date = request.args.get('date', '날짜')
    writer = request.args.get('writer', '글쓴이')

    c_delete = db_session.query(Comment).filter_by(id=id).first()
    if c_delete:
        db_session.delete(c_delete)
        db_session.commit()
        comment_list = db_session.query(Comment).all()
        #return redirect('/question')
        return render_template('/user_templates/question.html', title=title, date=date, category=category,
                               content=content, id=id, now_user=session['u_id'], writer=writer,
                               comment_list=comment_list)
    else:
        return render_template('/user_templates/main.html')



@app.route('/q_write', methods=['GET','POST'])
def q_write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        create_date = datetime.now()
        # category = request.form['category']
        category = request.form.get('category', False)


        if not title:
            flash('제목을 입력하세요')
            return redirect('/q_write')

        if not category:
            # 하나라도 작성하지 않으면 다시 회원가입 화면
            flash('카테고리를 체크해주세요.')
            return redirect('/q_write')

        if not content:
            flash('내용을 입력하세요')
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

    if not session.get('u_id'):
        return render_template('/user_templates/q&a.html', question_list=question_list, limit=limit, page=page,
                               tot_cnt=tot_cnt,
                               block_size=block_size, block_num=block_num, block_start=block_start, block_end=block_end,
                               last_page_num=last_page_num)
    else:
        return render_template('/user_templates/q&a.html', question_list=question_list, limit=limit, page=page, tot_cnt=tot_cnt,
                               block_size=block_size, block_num=block_num, block_start=block_start, block_end=block_end,
                               last_page_num=last_page_num, now_user=session['u_id'])


@app.route('/mypage')
def my_page():
    #print(request.method)
    if session.get('u_id'):
        info = db_session.query(User).filter_by(u_id=session['u_id']).first()
        question = db_session.query(QuestionContent).all()
        imageInfo = db_session.query(ImageInfo).all()

        # 한 페이지당 최대 게시물
        limit = 5
        # 페이지 값
        page = int(request.args.get('page', type=int, default=1))

        # .all() 이 붙은 순간 list가 됨.
        # question_list = db_session.query(QuestionContent).all()

        question_list = db_session.query(QuestionContent).filter_by(writer=session['u_id']).all()

        # 게시물 총 개수
        tot_cnt = len(question_list)

        # list를 각 페이지에 맞게 slice 시킴
        # question_list = question_list[((page-1)*limit) : ((page-1)*limit+limit)]
        if page == 1:
            question_list = question_list[-((page - 1) * limit + limit):]
        else:
            question_list = question_list[-((page - 1) * limit + limit):-((page - 1) * limit)]
        # print((page-1)*limit)
        # print((page-1)*limit+limit)

        # 마지막 페이지 수, 반드시 올림 해야 함.
        last_page_num = math.ceil(tot_cnt / limit)

        # 페이지 블럭 5개씩 표기
        block_size = 5
        # 현재 블럭의 위치 (첫번째 블럭이라면, block_num=0)
        block_num = int((page - 1) / block_size)

        # 현재 블럭의 맨 처음 페이지 넘버 (첫번째 블럭이라면 block_start = 1, 두번째 블럭이라면 block_start = 6)
        block_start = (block_size * block_num) + 1
        # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
        block_end = block_start + (block_size - 1)

        return render_template('/user_templates/mypage.html', now_uname=info.u_name, now_uphone=info.u_phone,
                               now_uid=info.u_id, now_upw=info.u_pw, writer=info.u_id, question=question,
                               question_list=question_list, limit=limit, page=page, tot_cnt=tot_cnt,
                               block_size=block_size,
                               block_num=block_num, block_start=block_start, block_end=block_end,
                               last_page_num=last_page_num, imageinfo=imageInfo)


    else:
        flash('로그인 후 이용가능합니다.')
        return redirect('/login')


@app.route('/myinfo_edit', methods=['GET','POST'])
def myinfo_edit():
    edit = db_session.query(User).filter_by(u_id=session['u_id']).first()
    image_edit = db_session.query(ImageInfo).filter_by(user=session['u_id']).all()
    question_edit = db_session.query(QuestionContent).filter_by(writer=session['u_id']).all()
    comment_edit = db_session.query(Comment).filter_by(commenter=session['u_id']).all()

    if request.method == 'GET':
        return render_template('/user_templates/myinfo_edit.html',
                               now_uname=edit.u_name, now_uphone=edit.u_phone, now_uid=edit.u_id, now_upw=edit.u_pw)
    else:
        if request.form['u_name'] != edit.u_name:
            edit.u_name = request.form['u_name']
        if request.form['u_phone'] != edit.u_phone:
            edit.u_phone = request.form['u_phone']
        if request.form['u_id'] != edit.u_id:
            edit.u_id = request.form['u_id']
        if request.form['u_pw'] != edit.u_pw:
            edit.u_pw = request.form['u_pw']

        for u_image in image_edit:
            if request.form['u_id'] != u_image.user:
                u_image.user = request.form['u_id']
                db_session.add(u_image)

        for u_question in question_edit:
            if request.form['u_id'] != u_question.writer:
                u_question.writer = request.form['u_id']
                db_session.add(u_question)

        for u_comment in comment_edit:
            if request.form['u_id'] != u_comment.commenter:
                u_comment.commenter = request.form['u_id']
                db_session.add(u_comment)


        db_session.add(edit)
        db_session.commit()
        session['u_id'] = edit.u_id
        return redirect('/mypage')
    return render_template('/user_templates/main.html')


# 마이페이지/내 사진에서 삭제버튼 눌렀을 때 처리
@app.route('/delete_image', methods=['GET', 'POST'])
def delete_image():
    name = request.args.get('name', '파일이름')
    i_delete = db_session.query(ImageInfo).filter_by(name=name).first()
    if i_delete:
        db_session.delete(i_delete)
        db_session.commit()
        flash('글이 삭제되었습니다.')
        return redirect('/mypage')
    else:
        return render_template('/user_templates/main.html')



@app.route('/mosaic_process')
def video_process():
    return render_template('/user_templates/mosaic_process.html')


# 메인
@app.route('/', methods = ['GET', 'POST'])
def index():
        return render_template('/user_templates/main.html')



# main.html과 mosaic_process.html에서 버튼 클릭 시 파일 업로드 처리
@app.route('/save_file', methods = ['GET', 'POST'])
def upload_file():

    d_path = request.args.get('path','경로')
    image_extenstion = ['ai', 'bmp', 'jpeg', 'jpg', 'jpe', 'jfif', 'jp2', 'j2c', 'pcx', 'psd', 'tga', 'taga',
                        'png', 'tif', 'tiff']
    video_extenstion = ['mp4', 'm4v', 'avi', 'wmv', 'mwa', 'asf', 'mpg', 'mpeg', 'ts', 'mkv', 'mov', '3gp', '3g2','gif',
                        'webm']
    if request.method == 'POST':

        # 모자이크에서 제외할 이미지
        f_input = request.files['file1']
        # 모자이크 할 파일 (단체사진)
        f_output = request.files['file2']

        if f_input.filename == '':
            print("잘 들어감")
            # 모자이크에서 제외할 이미지가 없을 때 전체 인물 모자이크 처리코드
            downloads_path = './static/downloads'
            d_path = './downloads/'
            filename2 = f_output.filename

            file_extenstion = filename2.split(".")[-1]
            filename = filename2

            if file_extenstion in image_extenstion:  # 단체 사진이 이미지 파일인 경우,
                if session.get('u_id'):
                    info = db_session.query(User).filter_by(u_id=session['u_id']).first()
                    filename = info.u_id + '-' + filename2
                    downloads_path = './static/member_img_downloads'
                    d_path = './member_img_downloads/'

                f_output.save('./static/output_uploads/' + secure_filename(filename2))  # 모자이크 할 image file (단체사진)
                path2 = './static/output_uploads/' + filename2

                # 서윤이가 보낸 코드 실행 부분
                img=face_recog_imageOnly.input(path2)
                img=face_recog_imageOnly.process(img)
                face_recog_imageOnly.save(downloads_path, img, filename)
                d_path=d_path+filename
                print("썸네일")
                print(d_path)
                return render_template('/user_templates/save_file.html', filename=filename, path=d_path)

            elif file_extenstion in video_extenstion:   # 단체 사진이 비디오 파일인 경우,
                if session.get('u_id'):
                    info = db_session.query(User).filter_by(u_id=session['u_id']).first()
                    filename = info.u_id + '-' + filename2
                    downloads_path = './static/member_video_downloads'
                    #d_path = './member_video_downloads/'

                f_output.save('./static/output_uploads/' + secure_filename(filename2))  # 모자이크 할 video file (단체사진)
                path2 = './static/output_uploads/' + filename2
                filename=filename.split(".")[0] + '.mp4'
                #filename = filename
                print("check")
                print(filename)
                img = face_recog_videoOnly.input(path2)
                downloads_path = downloads_path + '/' + filename
                fn = filename.split(".")[0] + ".jpg"
                d_path = './thumnail/' + fn
                d_path2 = './static/thumnail/' + fn
                writer = face_recog_videoOnly.process(img, downloads_path, d_path2)
                face_recog_videoOnly.save(writer)



                # 썸네일 생성
                #img = still_cut.makeStillCutImage(downloads_path)

                #still_cut.save(img, d_path2)

                return render_template('/user_templates/save_file.html', filename=filename, path=d_path)


        elif f_input.filename != '' and f_output.filename != '':    # 전체 이미지가 잘 들어온 경우, f_input 제외한 모든 대상 모자이크 처리
            downloads_path = './static/downloads'
            d_path = './downloads/'

            filename1 = f_input.filename    # 모자이크에서 제외할 이미지
            filename2 = f_output.filename   # 모자이크 할 image file (단체사진)

            file_extenstion = filename2.split(".")[-1]
            filename = filename2

            if file_extenstion in image_extenstion:     # 단체 사진이 이미지 파일인 경우,

                if session.get('u_id'):
                    info = db_session.query(User).filter_by(u_id=session['u_id']).first()
                    filename = info.u_id + '-' + filename2
                    downloads_path = './static/member_img_downloads'
                    d_path = './member_img_downloads/'

                f_input.save('./static/input_uploads/' + secure_filename(filename1))  # 모자이크에서 제외할 이미지
                f_output.save('./static/output_uploads/' + secure_filename(filename2))  # 모자이크 할 image file (단체사진)
                path1 = './static/input_uploads/' + filename1
                path2 = './static/output_uploads/' + filename2

                # 서윤이가 보낸 코드 실행 부분
                imgTrain = face_recog_image.input1(path1)  # 모자이크에서 제외할 이미지
                imgTest = face_recog_image.input2(path2)  # 모자이크 할 image file (단체사진)
                imgTest = face_recog_image.process(imgTest, imgTrain)
                face_recog_image.save(imgTest, downloads_path, filename)
                d_path = d_path + filename
                print(d_path)
                return render_template('/user_templates/save_file.html', filename=filename, path=d_path)

            elif file_extenstion in video_extenstion:   # 단체 사진이 비디오 파일인 경우,

                if session.get('u_id'):
                    info = db_session.query(User).filter_by(u_id=session['u_id']).first()
                    filename = info.u_id + '-' + filename2
                    downloads_path = './static/member_video_downloads'
                    #d_path = './member_video_downloads/'

                f_input.save('./static/input_uploads/' + secure_filename(filename1))  # 모자이크에서 제외할 이미지
                f_output.save('./static/output_uploads/' + secure_filename(filename2))  # 모자이크 할 video file (단체사진)
                path1 = './static/input_uploads/' + filename1
                path2 = './static/output_uploads/' + filename2

                filename=filename.split(".")[0] + '.mp4'
                print("check")
                print(filename)
                # 서윤이가 보낸 코드 실행 부분
                img = face_recog_video.input1(path1)  # 모자이크에서 제외할 이미지
                cap = face_recog_video.input2(path2)  # 모자이크 할 video file (단체사진)
                #d_path = d_path + filename
                downloads_path = downloads_path + '/' + filename
                fn = filename.split(".")[0] + ".jpg"
                d_path = './thumnail/' + fn
                d_path2 = './static/thumnail/'+fn
                writer = face_recog_video.process(cap, img, downloads_path, d_path2)
                face_recog_video.save(writer)



                print(downloads_path)
                return render_template('/user_templates/save_file.html', filename=filename, path=d_path)

            else:   # 지원하지 않는 형식

                flash('지원하지 않는 확장자입니다.')
                return render_template('/user_templates/main.html')

        else :
            # 그 이외의 모든 경우
            flash('모자이크 할 파일을 업로드 해주세요')
            return render_template('/user_templates/main.html')


# save_file.html에서 마이페이지에 저장 버튼 눌렀을 때 처리
@app.route('/mypage_image', methods=['GET', 'POST'])
def mypage_image():
    image_extenstion = ['ai', 'bmp', 'jpeg', 'jpg', 'jpe', 'jfif', 'jp2', 'j2c', 'pcx', 'psd', 'tga', 'taga',
                        'png', 'tif', 'tiff']
    video_extenstion = ['mp4', 'm4v', 'avi', 'wmv', 'mwa', 'asf', 'mpg', 'mpeg', 'ts', 'mkv', 'mov', '3gp', '3g2','gif',
                        'webm']

    filename = request.args.get('filename', '파일이름')
    file_extenstion = filename.split(".")[-1]

    if file_extenstion in image_extenstion:  # 단체 사진이 이미지 파일인 경우,
        path = './member_img_downloads/' + filename # 이미지는 썸네일을 여기서 가져다 쓰고
    elif file_extenstion in video_extenstion:  # 단체 사진이 비디오 파일인 경우,
        fn = filename.split(".")[0] + ".jpg"
        #d_path = './thumnail/' + fn
        path = './thumnail/' + fn       # 비디오는 썸네일을 여기서 가져다 쓰거든..!
    else:
        flash('예기치 못한 오류가 발생했습니다.')
        return render_template('/user_templates/save_file.html')

    print(filename)
    if session.get('u_id'):
        #image = ImageInfo(url=downloads_path, user=session['u_id'], date=datetime.now(), name=filename)
        image = ImageInfo()
        image.url = path
        image.user = session['u_id']
        image.date = datetime.now()
        image.name = filename

        db_session.add(image)
        db_session.commit()
        return redirect('/mypage')
    else:
        flash('로그인 후 이용가능합니다')
        return render_template('/user_templates/main.html')



# save_file.html에서 파일 다운로드 버튼 눌렀을 때 처리
@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    image_extenstion = ['ai', 'bmp', 'jpeg', 'jpg', 'jpe', 'jfif', 'jp2', 'j2c', 'pcx', 'psd', 'tga', 'taga',
                        'png', 'tif', 'tiff']
    video_extenstion = ['mp4', 'm4v', 'avi', 'wmv', 'mwa', 'asf', 'mpg', 'mpeg', 'ts', 'mkv', 'mov', '3gp', '3g2','gif',
                        'webm']

    # 파일 이름 받아옴
    filename = request.args.get('filename', '파일이름')
    file_extenstion = filename.split(".")[-1]
    #filename2 = filename + '.mp4'

    # print(filename)
    downloads_path = './static/downloads/'

    if file_extenstion in image_extenstion:  # 단체 사진이 이미지 파일인 경우,
        if session.get('u_id'):
            info = db_session.query(User).filter_by(u_id=session['u_id']).first()
            downloads_path = './static/member_img_downloads/'

    elif file_extenstion in video_extenstion:  # 단체 사진이 비디오 파일인 경우,
        if session.get('u_id'):
            info = db_session.query(User).filter_by(u_id=session['u_id']).first()
            downloads_path = './static/member_video_downloads/'
    else:
        flash('예기치 못한 오류가 발생했습니다.')
        return render_template('/user_templates/save_file.html')

    print(filename)
    return send_file(downloads_path + filename, attachment_filename=filename, as_attachment=True)



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
        elif len(u_id) > 7:
            flash('아이디를 7자 이하로 입력해주세요.')
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


# 탈퇴 구현
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    delete_user = db_session.query(User).filter_by(u_id=session['u_id']).first()
    delete_question_user = db_session.query(QuestionContent).filter_by(writer=session['u_id']).all()
    delete_image_user = db_session.query(ImageInfo).filter_by(user=session['u_id']).all()


    db_session.delete(delete_user)
    for question_user in delete_question_user:
        db_session.delete(question_user)
    for image_user in delete_image_user:
        db_session.delete(image_user)
    db_session.commit()
    session.clear()

    return render_template('/user_templates/main.html',logged_in=False)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='127.0.0.1', port=5000)