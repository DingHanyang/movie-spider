#-*- coding: utf-8 -*-
from email.parser import Parser
from email.header import decode_header
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import poplib
import smtplib

USERNAME='398556053@qq.com'
PASSWORD='xhzmraahbzldbjjb'


class ReceiveEmail():

    def __init__(self):
        # 连接到POP3服务器:
        self.server = poplib.POP3_SSL('pop.qq.com')
        #print(self.server.getwelcome()),'\n连接到POP服务器'
        # 可以打开或关闭调试信息:
        #self.server.set_debuglevel(1)

    def login(self):
        # 身份认证:
        self.server.user(USERNAME)
        self.server.pass_(PASSWORD)
        print ('连接到POP服务器,登陆账号成功')

    def __re_login(self):
        self.server.quit()
        self.server = poplib.POP3_SSL('pop.qq.com')
        try:
            self.server.user(USERNAME)
            self.server.pass_(PASSWORD)
        except:
            print("登陆邮箱超时，正在尝试重新登陆")
            self.__re_login()

    def get_emails(self,num):
        self.__re_login()
        mails_list=[]
        resp, mails, octets = self.server.list()
        index=len(mails)#当前邮件数量
        if num==1:return [self.get_one_email()]
        for i in range(index-num+1,index+1):
            resp, lines, octets = self.server.retr(i)
            msg_content = b'\r\n'.join(lines).decode("utf-8")
            msg = Parser().parsestr(msg_content)
            mails_list.append(self.__get_header(msg))

        return mails_list

    #获取所有邮件信息(设置为获取最近30天)
    def get_one_email(self):
        # stat()返回邮件数量和占用空间:
        #print('邮件数量: %s. 总大小(字节): %s' % self.server.stat())

        # list()返回所有邮件的编号:
        # resp服务器响应 mails消息列表 返回octets消息的大小
        resp, mails, octets = self.server.list()

        index=len(mails)
        #根据索引获取指定邮件所有列  索引从1到index index为最新的一封邮件
        resp, lines, octets = self.server.retr(index)
        #lines里面存储了邮件原始文本的每一行
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode("utf-8")
        #把邮件解析为message对象
        msg = Parser().parsestr(msg_content)
        return self.__get_header(msg)

    #解析邮件头部信息
    def __get_header(self,msg):
        info_list = []
        # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject','Date']:
            value = msg.get(header, '')
            if value:
                if header=='Date':
                    value = self.__decode_str(value)
                    info_list.append(value)
                elif header == 'Subject':
                    # 需要解码Subject字符串:
                    value = self.__decode_str(value)
                    info_list.append(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = self.__decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    info_list.append(addr)
                #info_list.append(value)
            else:
                info_list.append("NULL")
            #print('%s: %s' % (header, value))#输出信息
        return info_list

    def __decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def __guess_charset(self,msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def quit(self):
        self.server.quit()
        print ("已退出POP服务器")


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

class SendEmail():

    #初始化各参数
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.qq.com"  # 设置服务器
        self.mail_user =USERNAME  # 用户名
        self.mail_pass = PASSWORD  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
        self.sender = '398556053@qq.com'  # 发送方名称

    #登陆到SMTP服务器
    def login(self):
        try:
            self.smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)#创建一个SMTP对象
            self.smtpObj.login(self.mail_user, self.mail_pass)  # 登陆
            print ('连接到SMTP服务器,登陆账号成功')
        except (smtplib.SMTPException):
            print ('登陆失败\n')

    #创建一封新邮件
    def create(self,resDict):
        #邮件内容
        htmlP1 = "<html><body><h1>查询消息回复</h1>" \
                 "<p>共返回结果" + str(len(resDict)) + "条</p>"

        temp = ''
        for keys in resDict:
            temp += "<p>_____" + str(keys) + "_____</p>"
            temp += "<p>名称:" + str(resDict[keys][0]) + "</p>"
            temp += "<p>类型:" + str(resDict[keys][1]) + "</p>"
            temp += "<p>更新时间:" + str(resDict[keys][2])+ "</p>"
            temp += "<p>状态:" + str(resDict[keys][3])+ "</p>"
            temp += "<p>链接:" + str(resDict[keys][4]) + "</p>"
            temp += "<p>下载列表：</p>"
            for li in resDict[keys][5]:
                temp+="<p><b>"+str(li[0])+":</b>  "+str(li[1])+"</p>"
        htmlP2 = temp
        htmlP3 = "</body></html>"


        self.message=MIMEText(htmlP1+htmlP2+htmlP3 ,'html','utf-8')
        #发送方
        self.message['From'] = _format_addr('吃一口Python <%s>' % self.sender)
        #接收方
        self.message['To'] = 'you'

        #邮件标题
        subject = '查询信息回复'
        self.message['Subject'] = Header(subject, 'utf-8')


    #发送当前编辑的邮件
    def send(self,address):
        receivers=[]
        receivers.append(address)

        try:
            self.smtpObj.sendmail(self.sender, receivers, self.message.as_string())#发送邮件
            print ('发送成功')
        except smtplib.SMTPException:
            print ('发送失败\n')

    def quit(self):
        self.smtpObj.quit()
        print ('已退出SMTP服务器')


if __name__=="__main__":
    receive=ReceiveEmail()
    receive.login()
    print(receive.get_emails(3))
    receive.quit()


