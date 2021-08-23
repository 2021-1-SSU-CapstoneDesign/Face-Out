from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)  # 카테고리 번호
    name = Column(String(100), nullable=False)  # 카테고리 이름

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class QuestionContent(Base):
    __tablename__ = 'question_content'

    id = Column(Integer, primary_key=True)  # 질문 번호
    content = Column(Text, nullable=False)  # 질문 내용
    create_date = Column(DateTime(), nullable=False)  # 질문 등록날짜

    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(Question)  # 질문이랑 연결

    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'create_date': self.create_date,
        }


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


engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.create_all(engine)
