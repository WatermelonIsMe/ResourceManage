#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 设置数据库连接地址
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@127.0.0.1/aaa?charset=utf8"
# 是否追踪数据库修改  很消耗性能, 不建议使用
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 设置在控制台显示底层执行的SQL语句
app.config["SQLALCHEMY_ECHO"] = False

# 创建数据库连接
db = SQLAlchemy(app)


# resource_types表与resource_details表为一对多的关系
# 建立resource_types表  一
class Resource_type(db.Model):
    __tablename__ = 'resource_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # resource_types和resource_details表的关系由下面语句连接
    resource_details = db.relationship('Resource_detail')

    # def __init__(self, name):
    #     self.name = name


# 建立resource_details表 多
class Resource_detail(db.Model):
    __tablename__ = 'resource_details'
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(20))
    ipaddress = db.Column(db.String(20))
    # typeId为resource_type.id的外键
    type_Id = db.Column(db.Integer, db.ForeignKey('resource_types.id'))
    # resource_types和resource_details表的关系由下面语句连接。有一点不明白，在Rsource_type类下面定义了，在这里还要再定义，是否双向？
    resource_types = db.relationship('Resource_type')

    # resource_details表和applicants表的多对多的关系通过下面语句确定,
    details_applicants = db.relationship('Details_applicants', backref='resource_details')

    # def __init__(self, application, ipaddress, typeId):
    #     self.application = application
    #     self.ipaddress = ipaddress
    #     self.type_Id = typeId


# resource_details表与applicants表为多对多的关系
# 建立applicant表 多
class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    ip_users = db.Column(db.String(20))
    satffnumber = db.Column(db.String(20))
    department = db.Column(db.String(20))
    applyreason = db.Column(db.String(20))
    applytime = db.Column(db.String(20))
    effectivetime = db.Column(db.String(20))
    permission = db.Column(db.String(20))
    database_name = db.Column(db.String(20))
    database_tablename = db.Column(db.String(20))

    # resource_details表和applicants表的一对多的关系通过下面语句确定,
    applicants_details = db.relationship('Details_applicants', backref='applicants')


# 创建关系表  多对多关系必须创建单独的表来记录关联数据
class Details_applicants(db.Model):
    __tablename__ = 'details_applicants'  # 这就是所谓的一张视图表？没有实际存在数据，但是凭借关系型数据库的特点可以体现出一些数据关系

    applicants_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), primary_key=True)
    resource_details_id = db.Column(db.Integer, db.ForeignKey('resource_details.id'), primary_key=True)

    # 这张第三表中有两个主键，表示不能有applicants_id和resource_details_id都相同的两项

    def __init__(self, applicants_id=None, resource_details_id=None):
        self.applicants_id = applicants_id
        self.resource_details_id = resource_details_id


db.create_all()
