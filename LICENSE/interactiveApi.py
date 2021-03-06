#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from sqlalchemy import Column, String, create_engine, Integer,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import datetime
import os 
import random


app = Flask(__name__)

# 解决跨域请求问题
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

# 创建对象的基类:
Base = declarative_base()
# 定义v_type对象:
class v_type(Base):
    # 表的名字:
    __tablename__ = 'v_type'

    # 表的结构:
    Id = Column(Integer, primary_key=True)
    TypeName = Column(String(255))
    Remarks = Column(String(500))

class Lists(object):
    def __init__(self,code,msg,count,data):
        self.code = code
        self.msg = msg
        self.count = count
        self.data = data

class v_videos(Base):
    # 表的名字:
    __tablename__ = 'v_videos'

    # 表的结构:
    Id = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Cid = Column(Integer)
    CreateTime = Column(DateTime)
    ModifyTime = Column(DateTime)
    TypeId = Column(Integer)
    ImgUrl = Column(String(500))
    Remarks = Column(String(500))
    Type = Column(Integer)

class v_videoList(Base):
    # 表的名字:
    __tablename__ = 'v_videoList'

    # 表的结构:
    Id = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Cid = Column(Integer)
    CreateTime = Column(DateTime)
    ModifyTime = Column(DateTime)
    TypeId = Column(Integer)
    ImgUrl = Column(String(500))
    Remarks = Column(String(500))
    TypeName = Column(String(255))
    Title = Column(String(255))

class v_countries(Base):
    # 表的名字:
    __tablename__ = 'v_countries'

    # 表的结构:
    Id = Column(Integer, primary_key=True)
    Title = Column(String(255))
    Code = Column(String(255))

def v_typedict(std):
    return {
        'Id': std.Id,
        'TypeName': std.TypeName,
        'Remarks': std.Remarks
    }

def v_countriesdict(std):
    return {
        'Id': std.Id,
        'Title': std.Title,
        'Code': std.Code
    }

def v_videosdict(std):
    if not isinstance(std, v_videos):
        return std.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return {
            'id': std.Id,
            'name': std.Name,
            'Cid': std.Cid,
            # 'createTime': std.CreateTime,
            # 'ModifyTime': std.ModifyTime,
            'TypeId': std.TypeId,
            'ImgUrl': std.ImgUrl,
            'Remarks': std.Remarks
        }

def json_default(value):
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, Lists):
        return value.__dict__
    elif isinstance(value, v_videoList):
        return {
            'id': value.Id,
            'name': value.Name,
            'Cid': value.Cid,
            'createTime': value.CreateTime,
            'ModifyTime': value.ModifyTime,
            'TypeId': value.TypeId,
            'ImgUrl': value.ImgUrl,
            'remarks': value.Remarks,
            'typeName':value.TypeName,
            'title':value.Title
        }
    else:
        pass


def v_videoListdict(std):
    if isinstance(std, datetime.datetime):
        return std.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return {
            'id': std.Id,
            'name': std.Name,
            'cid': std.Cid,
            'createTime': std.CreateTime,
            'ModifyTime': std.ModifyTime,
            'typeId': std.TypeId,
            'imgUrl': std.ImgUrl,
            'remarks': std.Remarks,
            'typeName':std.TypeName,
            'title':std.Title
        }

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:cdUsr@2020.@116.196.75.200:3306/video')
# 创建DBSession类型:
# autocommit：是否自动提交，改为true可以防止发生(sqlalchemy.exc.InvalidRequestError) Can't reconnect until invalid transaction is rolled back错误，但会无法提交事务
DBSession = sessionmaker(bind=engine,autocommit=False) 

# 创建Session:
session = DBSession()



@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/getType', methods=['GET', 'POST'])
def signin_form():
    
    try:
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(v_type).filter().all()
        # 打印类型和对象的name属性:
        # print('type:', type(user))
        # print(user)
        types = json.dumps(user, default=v_typedict,ensure_ascii=False)
        # print(types)
        return types
    except Exception as e:
        session.rollback()
        pass
    

@app.route('/getList', methods=['GET', 'POST'])
def getList():

    try:
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(v_countries).filter().all()
        # 打印类型和对象的name属性:
        # print('type:', type(user))
        # print(user)
        types = json.dumps(user, default=v_countriesdict,ensure_ascii=False)
        # print(types)
        return types
    except Exception as e:
        session.rollback()
        pass


# 获取视频信息列表
@app.route('/GetVideo/',methods=['GET', 'POST'])
def GetVideo():# page,limit,Name='',CId='',TypeId=''
    # form_data = request.form

    page = request.args.get("page")
    limit = request.args.get('limit')
    Name = request.args.get('Name')
    CId = request.args.get('CId')
    TypeId = request.args.get('TypeId')

    try:
        session.rollback()
        video = session.query(v_videoList)
        if Name:
            video = video.filter(v_videoList.Name.like("%{0}%".format(Name)))
        if CId:
            video = video.filter(v_videoList.Cid==CId)
        if TypeId:
            video = video.filter(v_videoList.TypeId==TypeId)
        video = video.limit(limit).offset((int(page)-1)*int(limit)).all()
        # print('type:', type(video))
        # for n in video:
        #     print(type(n))
        # types = json.dumps(video, default=v_videoListdict,ensure_ascii=False)
        count = session.query(v_videoList).count()
        lists = Lists('0','',count,video)
        types = json.dumps(lists, default=json_default,ensure_ascii=False)
        # print(types)
        return types
    except Exception as e:
        session.rollback()
        pass

    

# 新增视频信息
@app.route('/AddVideo',methods=['GET', 'POST'])
def AddVideo():
    Name = request.form['Name']
    Cid = request.form['Cid']
    TypeId = request.form['TypeId']
    ImgUrl = request.form['ImgUrl']
    Remarks = request.form['Remarks']
    try:
        # 保存一条数据
        new_video = v_videos(
            Name = Name,
            Cid = Cid,
            CreateTime = datetime.datetime.now(),
            TypeId = TypeId,
            ImgUrl = ImgUrl,
            Remarks = Remarks,
            Type = 1
            )
        session.add(new_video)
        session.commit()
        res = {
            'code': 0,
            'msg': '上传成功'
        }
    except Exception as e:
        res = {
            'code': 200,
            'msg': '上传失败'
        }
    return json.dumps(res)

# 查询视频信息
@app.route('/SelectVideo',methods=['GET', 'POST'])
def SelectVideo():
    Vid = request.args.get("Vid")
    try:
        session.rollback()
        video = session.query(v_videoList).filter(v_videoList.Id==Vid).one()
        types = json.dumps(video, default=v_videoListdict,ensure_ascii=False)
        # print(types)
        return types
    except Exception as e:
        session.rollback()
        pass

# 编辑保存
@app.route('/EditVideo',methods=['GET', 'POST'])
def EditVideo():
    Vid = request.form['Vid']
    Name = request.form['Name']
    Cid = request.form['Cid']
    TypeId = request.form['TypeId']
    ImgUrl = request.form['ImgUrl']
    Remarks = request.form['Remarks']
    try:
        session.rollback()
        video = session.query(v_videos).filter(v_videos.Id==Vid).one()
        video.Name = Name
        video.Cid = Cid
        video.ModifyTime = datetime.datetime.now()
        video.TypeId = TypeId
        video.ImgUrl = ImgUrl
        video.Remarks = Remarks
        session.commit()
        res = {
            'code': 0,
            'msg': '修改成功'
        }
        
    except Exception as e:
        res = {
            'code': 200,
            'msg': '修改失败'
        }
    return json.dumps(res)


# 删除视频
@app.route('/DeleteVideo',methods=['GET', 'POST'])
def DeleteVideo():
    Vid = request.args.get("Vid")
    try:
        session.rollback()
        video = session.query(v_videos).filter(v_videos.Id==Vid).one()
        # session.delete(video)
        video.Type = 0
        session.commit()
        res = {
            'code': 0,
            'msg': '删除成功'
        }
        
    except Exception as e:
        res = {
            'code': 200,
            'msg': '删除失败'
        }
    return json.dumps(res)


# 实现图片上传
@app.route('/AddImage',methods=['GET', 'POST'])
def AddImage():
    img = request.files.get('file')
     #转bytes类型
    pic = img.read()
    sufix = os.path.splitext(img.filename)[1]
 
    # 生成 随机文件名字
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = "%06d" % random.randint(0, 999999)
    name = now_time + random_str
 
    fname = "{}".format(name)+sufix
    dir = os.path.join(os.path.abspath('.'), 'goods_image')
    try:
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        with open(os.path.join(os.path.abspath('.'), 'goods_image', fname), 'wb') as f:
            f.write(pic)
 
        pic_path = os.path.join('..', 'goods_image', fname) # os.path.abspath('.') + '\goods_image\' + fname
 
    except Exception as e:
        res = {
            'code': 200,
            'msg': '保存图片失败'
        }
 
    res = {
        'image': pic_path,
        'code': 0,
        'msg': '上传图片成功'
    }
    # print(type(res))
    return json.dumps(res)


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

# 关闭Session:
session.close()

if __name__ == '__main__':
    app.run(port=9999)










