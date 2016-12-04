#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from server.mongo import MongoDao
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from urllib.error import HTTPError,URLError


class Search:
    # 初始化浏览器驱动
    def __init__(self,browser_path):
        self.browser = webdriver.PhantomJS(
            executable_path=browser_path)
        self.mongo=MongoDao()

        print('初始化搜索模块成功')

    # 搜索loldytt这个网站 返回一个列表 元素是字典
    def search_loldytt(self, keys):
        # loldytt的搜索页面 不从主页进入是为了绕开广告及弹窗
        self.browser.implicitly_wait(3)
        try:
            self.browser.get("http://so.loldytt.com/search.asp")
        except NoSuchElementException as e:
            print(e)
            self.browser.refreash()

        # 通过分析html代码模拟向搜索框发送数据
        search_box = self.browser.find_element_by_class_name("key")
        search_box.send_keys(keys)
        search_box.submit()

        # 跳转到结果页
        # 获取所有结果所在ol标签
        ol_list = self.browser.find_element_by_class_name("solb").find_elements_by_tag_name("ol")
        print("共搜索到", len(ol_list), "条结果")

        # 处理搜索到的结果
        self.res_list=[]
        # 通过遍历每个ol标签得到 各种数据信息
        for res in ol_list:
            name = res.find_element_by_tag_name("label").find_element_by_tag_name("a").text  # 影片名
            link = res.find_element_by_tag_name("label").find_element_by_tag_name("a").get_attribute("href")  # 链接
            type = res.find_element_by_tag_name("b").text  # 影片类型
            time = res.find_element_by_tag_name("strong").text  # 更新时间

            url_list = []
            print("名称:",name)
            print("类型:",type)
            print("更新时间:",time)

            try:
                html = urlopen(link)
                bsObj = BS(html.read(), "html.parser", from_encoding="gb18030")

            except HTTPError as e:
                print(e)
                print("无法正确打开网页")
                return

            try:
                uls = bsObj.find("ul", {"id": "ul1"}).find_all("li")
                for li in uls:
                    title = li.a.get("title")
                    href = li.a.get("href")
                    url_list.append([str(title).replace(".", "_"), str(href)])
            except:
                try:
                    uls = bsObj.find("div", {"id": "bt"}).find_all("li")
                    for li in uls:
                        title = li.a.get("title")
                        href = li.a.get("href")
                        url_list.append([str(title).replace(".", "_"), str(href)])
                except:
                    print("无下载地址")
                    return

            self.res_list.append({"名称":name,"类型":type,"更新时间":time,"下载连接":url_list})
        return self.res_list



    def quit(self):
        self.browser.quit()
        print('已关闭搜索模块')


if __name__ == "__main__":
    search = Search(r"D:\Program Files (x86)\phantomjs-2.1.1-windows\bin\Phantomjs.exe")
    search.search_loldytt('超脱')
    print(search.res_list)
    search.browser.quit()







