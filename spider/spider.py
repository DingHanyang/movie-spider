#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS

from urllib.request import urlopen
import re


class spider:

    # 根据网站不同分类页面来爬取所有电影的详细页面地址，存放后再从详细页面获取信息。
    def spider_url(self):
        url_set=set()
        TYPEDICT = {"科幻电影":"Kehuandianying","动作电影":"Dongzuodianying","恐怖电影":"Kongbudianying",
                    "喜剧电影":"Xijudianying","爱情电影":"Aiqingdianying","剧情电影":"Juqingdianying",
                    "战争电影":"Zhanzhengdianying","动漫":"Anime","综艺":"Zuixinzongyi","电视剧":"Dianshiju",
                    "美剧":"Zuixinmeiju","韩剧":"Zuixinhanju","港剧":"Zuixingangju","偶像剧":"Ouxiangju",
                    "日剧":"Zuixinriju","泰剧":"Taiguodianshiju"}

        for keys in TYPEDICT:
            html = urlopen("http://www.loldytt.com/"+TYPEDICT[keys]+"/chart/1.html")
            bsObj = BS(html.read(), "html.parser",from_encoding="gb18030")
            pageNum=int(re.findall(r"\d+\.?\d*", bsObj.find("div",{"class":"pagebox"}).span.text)[1])

            for i in range(1,pageNum+1):
                html = urlopen("http://www.loldytt.com/" + TYPEDICT[keys] + "/chart/"+str(i)+".html")
                bsObj = BS(html.read(), "html.parser")
                print("正在爬取",bsObj.title)
                a = bsObj.find_all("a", {"href": re.compile("^http://www.loldytt.com/"+TYPEDICT[keys]+"/.[A-Z0-9].*/")})
                for li in a:
                    url=li.get("href")
                    print(url)
                    url_set.add(url+"\n")
        fp = open("URL.txt", "a")
        for line in url_set:
            try:
                fp.write(line)
            except:
                continue
        fp.close()

    # 从详细页面获取信息
    def spider_info(self):
        url_set=set()
        fp = open("URL.txt","r")
        for line in fp:
            url_set.add(line.replace("\n",""))
        fp.close()

        for d in url_set:
            try:
                html=urlopen(d)
                bsObj = BS(html.read(), "html.parser", from_encoding="gb18030")
            except:
                print("无法正确打开网页")
                continue

            name=bsObj.h1.a.text
            time=bsObj.h1.p.text
            type=str(bsObj.find("div",{"id":"fenlei"}).find("ul").get_text())
            type=type.split()
            type=type[0]
            print("名称：",name)
            print("时间：",time)
            print("类型：",type)


            thunderList=[]#下载连接
            try:
                uls=bsObj.find("ul",{"id":"ul1"}).find_all("li")
                for li in uls:
                    title=li.a.get("title")
                    href=li.a.get("href")
                    thunderList.append([str(title).replace(".","_"),str(href)])
                    print(title,href)
            except:
                try:
                    uls=bsObj.find("div",{"id":"bt"}).find_all("li")
                    for li in uls:
                        title = li.a.get("title")
                        href = li.a.get("href")
                        thunderList.append([str(title).replace(".", "_"), str(href)])
                        print(title, href)
                except:
                    continue



if __name__=="__main__":
    spider=spider()
    spider.spider_url()
    spider.spider_info()
