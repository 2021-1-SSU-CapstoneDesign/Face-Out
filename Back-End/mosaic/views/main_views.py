from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


# User Web Page

@bp.route('/signup')    # 회원가입
def sign_up():
    return render_template('/user_templates/signup.html')

@bp.route('/question')
def question():
    return render_template('/user_templates/question.html')

@bp.route('/save_video')
def save_video():
    return render_template('/user_templates/save_video.html')

@bp.route('/q_write')
def q_write():
    return render_template('/user_templates/q_write.html')

@bp.route('/mypage')
def my_page():
    return render_template('/user_templates/mypage.html')

@bp.route('/mosaic_process')
def video_process():
    return render_template('/user_templates/mosaic_process.html')

@bp.route('/login')
def login():
    return render_template('/user_templates/login.html')

@bp.route('/q&a')
def question_notice():
    return render_template('/user_templates/q&a.html')

@bp.route('/')
def index():
    return render_template('/user_templates/main.html')