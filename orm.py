# -*- coding:utf-8 -*-
"""
File Name: orm
Version:
Description:
Author: liuxuewen
Date: 2018/1/4 10:49
"""
from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:mime@123@99.48.58.95:3306/spider?charset=utf8",echo=False)

DB_Session = sessionmaker(bind=engine)

Base = declarative_base()




class KuaiDiPhoneOrm(Base):
    __tablename__ = 'kuaidi100_phone'
    id = Column(Integer, primary_key=True,autoincrement=True)
    kuaidi_id=Column(String(32))
    phone_tag= Column(String(128))
    phone_num = Column(String(16))
    source = Column(String(64))
    create_time= Column(DateTime)

db_sess = DB_Session()
def save2mysql(data):
    
    db_sess.add(KuaiDiPhoneOrm(kuaidi_id=data['kuaidi_id'],
                               province=data['province'],
                               city=data['city'],
                               phone_tag=data['phone_tag'],
                               phone_num=data['phone_num'],
                               source=data['source'],
                               create_time=data['create_time']))
    db_sess.commit()