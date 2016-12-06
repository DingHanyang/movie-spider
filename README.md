# movie-spider
定向爬取网站www.loldytt.com的所有资源，并提供邮件推送功能。

## 基本功能

- 通过爬虫将此网站的数据全部倒入Mongo数据库中，并提供搜索功能
- 对于网站更新的电影，如果搜索数据库时不存在，则爬取指定电影并存入本地数据库
- 邮件服务
  - 间隔指定时间段监测指定邮箱是否有收到用户发出的搜索需求邮件
  - 响应搜索需求，并返回结果邮件到用户邮箱



## 安装说明

python版本：`3.5`

系统平台：`windows10`

需要的python安装的第三方库: `pymongo,selenium,BeautifulSoup ` 

均可通过`pip install `安装

需要安装的软件：`PhantomJS	一个无头浏览器`

​			       `mongoDB3.2   	非关系型数据库	`   	

PhantomJS

只需下载并安装到任意路径即可

mongoDB

安装可参考我博客园笔记:  [MongoDB笔记](http://www.cnblogs.com/eatPython/p/6091524.html)



## 配置文件

[db]
host = 127.0.0.1#默认
port = 27017#默认

[email]
username =     #邮箱名
password =     #邮箱口令（非密码需获取）
popserver = pop.qq.com#此处使用腾讯的邮箱服务
smtpserver = smtp.qq.com#同上
sendername = 398556053@qq.com#发送者邮箱地址                                                                                            from = eatPython#发送者                                                                                                                                                           to = user#接受者

[browser]
path = D:\Program Files (x86)\phantomjs-2.1.1-windows\bin\Phantomjs.exe#phantomjs#浏览器路径



![email](http://ww4.sinaimg.cn/large/69cc9f84gw1fahdcuytc9j208l03egmu.jpg)



收到回复邮件时，两个框的信息分别为from和to处的信息，可自行修改。



## 说明

### 1.spider.py

![imag](http://ww3.sinaimg.cn/large/69cc9f84gw1fagv8vv4w6j21yz0lcq76.jpg)

首先人工获取各类资源子页面（大概十几种吧）

* 线程1用于访问这些页面并记录下这些页面中的URL，根据此网站的规律，通过正则取出影视资源详细页面并去重，放入队列中。
* 线程2从队列中取出一个URL（如为空，线程等待）访问URL并从中获取此页面影视的各类详细信息。

### 2.search.py

不同于spider,search采用selenium模拟浏览器的行为，对搜索框进行输入，并跳转到搜索结果页面后才采用urllib的方式进行采集。



# 未完






