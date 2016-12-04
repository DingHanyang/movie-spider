#-*- coding: utf-8 -*-
from server.email_server import ReceiveEmail,SendEmail
from spider.search import Search
from server.mongo import MongoDao

from queue import Queue
import datetime
import threading
import time

class RunServer():
    BROWSER_PATH=r"D:\Program Files (x86)\phantomjs-2.1.1-windows\bin\Phantomjs.exe"
    wait_queue=Queue()#等待队列

    def __init__(self):
        #登陆pop3和smtp服务器
        self.receiver=ReceiveEmail()
        self.receiver.login()
        self.sender=SendEmail()
        self.sender.login()
        #启动搜索模块
        self.searcher=Search(self.BROWSER_PATH)
        #mongo数据库模块
        self.mongo=MongoDao()

    def quit(self):
        #关闭所有模块
        self.sender.quit()
        self.receiver.quit()
        self.searcher.quit()

    #格式化邮件时间
    def __format_time(self,time):
        return datetime.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %z')

    def get_request(self):
        # 启动时先获取最新一封邮件的时间
        flag_time = self.__format_time(self.receiver.get_one_email()[3])
        # 不停地监测是否有收到新邮件(flag_time之后的邮件，并把最新一封邮件的时间定义为flag_time)
        while True:
            time.sleep(5)
            print(self.wait_queue.qsize())
            flag = 0#判断是否有未收取邮件
            temp_list = self.receiver.get_emails(5)  # 获取最新的邮件

            for li in temp_list:
                if li[2]=='查询信息回复':
                    continue
                if self.__format_time(li[3]) > flag_time:
                    flag = 1
                    flag_time = self.__format_time(temp_list[-1:][0][3])
                    temp_list = temp_list[temp_list.index(li):]
                    break

            if flag == 1:
                for li in temp_list:
                    self.wait_queue.put(li)

    #['From', 'To', 'Subject','Date']
    #根据队列中的信息进行搜索
    def search_server(self):
        while True:
            do = self.wait_queue.get(block=True)# 如果队列中有对象则取出,否则调用线程暂停等待
            print(do)
            self.res_list = self.mongo.find_moive(do[2])
            if len(self.res_list)==0:#数据库中不存在则启动在线搜索
                self.res_list = self.searcher.search_loldytt(do[2])

            self.sender.create(self.res_list)
            self.sender.send(do[0])


FUNCS=[RunServer.get_request,RunServer.search_server]
nFUNCS=range(len(FUNCS))

def main():
    run=RunServer()
    threads=[]
    for i in nFUNCS:
        t = threading.Thread(target=FUNCS[i],args=(run,))
        threads.append(t)

    for i in nFUNCS:
        threads[i].start()

    for i in nFUNCS:
        threads[i].join()


if __name__ == '__main__':
    main()
