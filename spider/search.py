#-*- coding: utf-8 -*-
from selenium import webdriver


class search:
    # 初始化浏览器驱动
    def __init__(self,browser_path):
        self.browser = webdriver.PhantomJS(
            executable_path=browser_path)
        print('初始化搜索模块成功')

    # 搜索loldytt这个网站
    def search_loldytt(self, keys):
        # loldytt的搜索页面 不从主页进入是为了绕开广告及弹窗
        self.browser.get("http://so.loldytt.com/search.asp")

        # 通过分析html代码模拟向搜索框发送数据
        search_box = self.browser.find_element_by_class_name("key")
        search_box.send_keys(keys)
        search_box.submit()

        # 跳转到结果页
        # 获取所有结果所在ol标签
        res_list = self.browser.find_element_by_class_name("solb").find_elements_by_tag_name("ol")
        print("共搜索到", len(res_list), "条结果")

        # 处理搜索到的结果
        i = 1
        self.res_dict = {}  # 结果集字典
        # 通过遍历每个ol标签得到 各种数据信息
        for res in res_list:
            name = res.find_element_by_tag_name("label").find_element_by_tag_name("a").text  # 影片名
            try:
                flag = res.find_element_by_tag_name("span").text  # 资源状态
            except:
                flag = "剧情介绍"
            link = res.find_element_by_tag_name("label").find_element_by_tag_name("a").get_attribute("href")  # 链接
            type = res.find_element_by_tag_name("b").text  # 影片类型
            time = res.find_element_by_tag_name("strong").text  # 更新时间
            self.res_dict[i] = [name, type, time, flag, link, []]  # 添加进字典中
            i += 1

        # 遍历字典搜索下载连接
        for keys in self.res_dict:
            print("_____", keys, "_____")
            print("名称:", self.res_dict[keys][0])
            print("类型:", self.res_dict[keys][1])
            print("更新时间:", self.res_dict[keys][2])
            print("状态:", self.res_dict[keys][3])
            print("链接:", self.res_dict[keys][4])
            self.browser.get(self.res_dict[keys][4])
            try:
                list_div = self.browser.find_element_by_id("liebiao").find_element_by_id("jishu")
                url_list = list_div.find_elements_by_tag_name("li")  # 资源集列表
                for li in url_list:
                    info = li.find_element_by_tag_name("span").find_element_by_tag_name("a")
                    self.res_dict[keys][5].append([info.text, info.get_attribute("href")])
                    print(info.text, info.get_attribute("href"))
            except:
                print("无资源")


    def quit(self):
        self.browser.quit()
        print('已关闭搜索模块')


if __name__ == "__main__":
    search = search(r"D:\Program Files (x86)\phantomjs-2.1.1-windows\bin\Phantomjs.exe")
    search.search_loldytt('超脱')
    search.browser.quit()







