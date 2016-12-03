#-*- coding: utf-8 -*-
from pymongo import MongoClient
import re


class MongoDao():

    def __init__(self):
        self.client = MongoClient()  # 创建默认连接 localhost 27017
        self.db=self.client.movie    # 选择数据库 如果不存在将在插入数据后建立

    #infos 字典类型
    def insert_Infos(self,infos):
        self.posts=self.db.movieInfos
        self.posts.insert_one(infos)

    def find_moive(self,name):
        self.posts=self.db.movieInfos
        self.res_list=[]
        regex=re.compile(name)
        for u in self.posts.find({"名称":name}):
            self.res_list.append(u)

        return self.res_list

if __name__=="__main__":
    mongo=MongoDao()
    mongo.find_moive("超脱")