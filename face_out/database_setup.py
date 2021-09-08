from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True) # 유저 번호
    u_name = Column(String(50), nullable=False)   # 유저 이름
    u_phone = Column(String(50), nullable=False)   # 유저 핸드폰 번호
    u_id = Column(String(100), nullable=False)       # 유저 id
    u_pw = Column(String(100), nullable=False)       # 유저 pw

    @property
    def serialize(self):
        return {
            'id': self.id,
            'u_name': self.u_nameame,
            'u_phone': self.u_phone,
            'u_id': self.u_id,
            'u_pw': self.u_pw,
        }


class QuestionContent(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)  # 질문 번호
    title = Column(Text, nullable=False) # 질문 제목
    content = Column(Text, nullable=False)  # 질문 내용
    create_date = Column(String(50), nullable=False)  # 질문 등록날짜
    is_secret = Column(Boolean, nullable=False)  # 비밀글 설정 여부
    category = Column(String(50), nullable=False) # 카테고리 번호
    writer = Column(String(100), nullable=False)    # 작성자 아이디

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'create_date': self.create_date,
            'is_secret': self.is_secret,
            'writer' : self.writer,
        }


class Comment(Base):
    __tablename__ = 'comment_info'

    id = Column(Integer, primary_key=True)  # 댓글 번호
    comment_content = Column(Text, nullable=False)  # 댓글 내용
    #create_date = Column(String(50), nullable=False)  # 댓글 등록날짜
    commenter = Column(String(100), nullable=False)   # 작성자 아이디
    question_id = Column(Integer, nullable=False) # 질문 번호

    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'writer': self.writer,
            'question_id': self.question_id,
        }


class ImageInfo(Base):
    __tablename__ = 'image_info'

    id = Column(Integer, primary_key=True)  # 이미지 번호
    url = Column(Text, nullable=False) # 이미지 링크
    user = Column(String(100), nullable=False)  # 사용자 id
    date = Column(String(50), nullable=False) # ㄷㅡㅇㄹㅗㄱㄴㅏㄹㅉㅏ
    name = Column(Text, nullable=False) # image ㅇㅣㄹㅡㅁ

    @property
    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'user': self.user,
            'date': self.date,
            'name': self.name,
        }

engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.create_all(engine)