from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Question, QuestionContent

engine = create_engine('mysql+pymysql://root:root@localhost/mosaic')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

question_upload = Question(name='동영상 업로드')
question_download = Question(name='동영상 다운로드')
question_save = Question(name='동영상 저장')
question_notice = Question(name='공지사항')

session.add(question_upload)
session.add(question_download)
session.add(question_save)
session.add(question_notice)
session.commit()

# 데이터 잘 들어가는지 확인용
question_content1 = QuestionContent(content='됐나?', create_date='2021-8-10', question=question_upload)

session.add(question_content1)
session.commit()

