#-*- coding: utf-8 -*-
from pymongo import MongoClient
import re

from server.Rconfig import Cf

cf = Cf()
PORT=cf.config.getint("db","port")
HOST=cf.config.get("db","host")


class MongoDao():

    def __init__(self):
        self.client = MongoClient(port=PORT,host=HOST)  # 创建默认连接 localhost 27017
        self.db=self.client.movie    # 选择数据库 如果不存在将在插入数据后建立
        print("与数据库成功建立连接")

    #infos 字典类型
    def insert_Infos(self,infos):
        self.posts=self.db.movieInfos
        self.posts.insert_one(infos)

    def find_moive(self,name):
        self.posts=self.db.movieInfos
        self.res_list=[]
        regex=re.compile(name)
        for u in self.posts.find({"名称":regex}).limit(10):
            self.res_list.append(u)

        return self.res_list

if __name__=="__main__":
    mongo=MongoDao()
    print(len(mongo.find_moive("求婚大作战")))