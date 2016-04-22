# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:27:05 2015

@author: DJM <op87960@gmail.com>
"""
from __future__ import division
from html2csv import *
import urllib2
import cookielib
import urllib
import string
#import Image
#import cStringIO 
#from pytesser import *
import csv
import re
import os
import getpass
import sys  
reload(sys)  
sys.setdefaultencoding('gb2312')

class gdutLogin:
    
    #初始化方法
    def __init__(self):
       
        logo='''           #########################################################################
       #     __  __                     __           ______    _____           #
       #    /\ \/\ \                   /\ \         /\__  _\  /\  _ `\         #
       #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \/\ \        #
       #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
       #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
       #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
       #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.0 #
       #                                                                By DJM #
       #                                                            from  GDUT #
       #                                             dengjiaming@greatzone.com #
       #########################################################################'''
        print logo        
        
        print u'程序正在初始化。。。'        
        #登陆页面
        self.loginpage = "http://jwgldx.gdut.edu.cn/default2.aspx"
        self.vrifycodeUrl = "http://jwgldx.gdut.edu.cn/CheckCode.aspx"
        #要post的url
        self.LoginUrl   = "http://jwgldx.gdut.edu.cn/default2.aspx"
        self.filename = 'cookie.txt'
        #下面这段是关键了，将为urlib2.urlopen绑定cookies
        #MozillaCookieJar(也可以是 LWPCookieJar ，这里模拟火狐，所以用这个了) 提供可读写操作的cookie文件,存储cookie对象
        self.cookiejar = cookielib.MozillaCookieJar(self.filename)
        # 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookieSupport= urllib2.HTTPCookieProcessor(self.cookiejar)
        #下面两行为了调试的
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        #创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的
        opener = urllib2.build_opener(cookieSupport, httpsHandler)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起，安装opener,此后调用urlopen()时都会使用安装过的opener对象，
        urllib2.install_opener(opener)
        #打开登陆页面, 以此来获取cookies   。  但是因为  ##打开验证码页面就可以获取全部cookies了，所以可以直接跳过这一步。算是可有可无的
        cook = urllib2.urlopen(self.loginpage)
         #学分list
        self.credit = []
        #成绩list
        self.grades = []
        #绩点list
        self.gpa = []
    
        
        #打印cookies
#        print   self.cookiejar    

        #昵称
        self.nickname = '';
        #用户名，密码
        self.username = raw_input('username : ')
        #self.password = getpass.getpass()raw_input(u"请输入密码 : ")
        self.password = getpass.getpass('password: ')
        
    #获取验证码函数   
    def getCode(self):
#        print u"验证码获取成功"
#        print u"请在浏览器中输入您看到的验证码"        
        file = urllib2.urlopen(self.vrifycodeUrl)
        pic= file.read()
        path = "code.jpg"
        #img = cStringIO.StringIO(file) # constructs a StringIO holding the image  AttributeError: addinfourl instance has no attribute 'seek'
        localpic = open(path,"wb")
        localpic.write(pic)
        localpic.close()
        text =raw_input('verifiedCode : ')
        return text
    
    #登录函数
    def login(self,text):   
        
        #设置cookie的值，因为post request head  需要 返回 cookie (不是cookies ，是将cookies的格式处理后的值)  
        cookies = ''
        #这里要从
        for index, cookie in enumerate(self.cookiejar):
            #print '[',index, ']';
            #print cookie.name;
            #print cookie.value;
            #print "###########################"
            cookies = cookies+cookie.name+"="+cookie.value+";";
#        print "###########################"
        cookie = cookies[:-1]
#        print "cookies:",cookie
        print u'cookies获取成功'

        #请求数据包
        postData = {   
         '__VIEWSTATE': 'dDwyODE2NTM0OTg7Oz7QqY3yg91iEh+CrEbxxVUHRHuTxg==',
         'txtUserName':self.username, 
         'TextBox2':self.password,    
         'txtSecretCode':text,
         'RadioButtonList1':'%D1%A7%C9%FA',
         'Button1':'',
         'lbLanguage':'',
         'hidPdrs':'',
         'hidsc':''
        } 
         
 
        #post请求头部
        headers = {
            
         'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            
            'Host':    'jwgldx.gdut.edu.cn',
            #'Cookie':cookies,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',  
            'Referer' : 'http://jwgldx.gdut.edu.cn/',
         #'Content-Type': 'application/x-www-form-urlencoded',
         #'Content-Length' :474,
            'Connection' : 'Keep-Alive'
         
        }
#        print headers        
        
        #合成post数据 
        data = urllib.urlencode(postData)    
#        print "data:###############"
#        print  data
        #创建request
        #构造request请求
        request = urllib2.Request(  self.LoginUrl,data,headers  )
        try:
         #访问页面
         response = urllib2.urlopen(request)
         #cur_url =  response.geturl()
         #print "cur_url:",cur_url
         status = response.getcode()
#         print status
        except  urllib2.HTTPError, e:
          print e.code
        #将响应的网页打印到文件中，方便自己排查错误
        #必须对网页进行解码处理
        f = response.read().decode("gb2312")
##        print f
        a = re.search(r"alert\('(.*?)'\)",f,re.S)
        if a:
            print a.group(1)    #输出错误信息
            return -1
        b = re.search(r'<span id="xhxm">(.*?)<',f,re.S)
        if b:
            print u"欢迎你"+b.group(1)
            self.nickname = b.group(1)
#        if a:
#            if re.search(u'验证码不正确',f):
#                print u'验证码不正确'
#            else:
#                print u'登录失败'
#            exit(0)
        #outfile =open("c:\\rel_ip.txt","wb")
        #print >> outfile , "%s"   % ( f)
#        print f
        
        self.cookiejar.save(ignore_discard=True, ignore_expires=True)
        #cookiejar.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        #响应的信息
        #info = response.info()
        #print info
        return cookies
    
    #获取成绩功能
    def getGrade(self,cookies,year):    
        year = year
        term = '1'
        
        postData = {   
         '__VIEWSTATE': 'dDw0MTg3MjExMDA7dDw7bDxpPDE+Oz47bDx0PDtsPGk8MT47aTwxNT47aTwxNz47aTwyMz47aTwyNT47aTwyNz47aTwyOT47aTwzMD47aTwzMj47aTwzND47aTwzNj47aTw0OD47aTw1Mj47PjtsPHQ8dDw7dDxpPDE2PjtAPFxlOzIwMDEtMjAwMjsyMDAyLTIwMDM7MjAwMy0yMDA0OzIwMDQtMjAwNTsyMDA1LTIwMDY7MjAwNi0yMDA3OzIwMDctMjAwODsyMDA4LTIwMDk7MjAwOS0yMDEwOzIwMTAtMjAxMTsyMDExLTIwMTI7MjAxMi0yMDEzOzIwMTMtMjAxNDsyMDE0LTIwMTU7MjAxNS0yMDE2Oz47QDxcZTsyMDAxLTIwMDI7MjAwMi0yMDAzOzIwMDMtMjAwNDsyMDA0LTIwMDU7MjAwNS0yMDA2OzIwMDYtMjAwNzsyMDA3LTIwMDg7MjAwOC0yMDA5OzIwMDktMjAxMDsyMDEwLTIwMTE7MjAxMS0yMDEyOzIwMTItMjAxMzsyMDEzLTIwMTQ7MjAxNC0yMDE1OzIwMTUtMjAxNjs+Pjs+Ozs+O3Q8cDw7cDxsPG9uY2xpY2s7PjtsPHByZXZpZXcoKVw7Oz4+Pjs7Pjt0PHA8O3A8bDxvbmNsaWNrOz47bDx3aW5kb3cuY2xvc2UoKVw7Oz4+Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWtpuWPt++8mjMxMTMwMDY0NTk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWnk+WQje+8mumCk+WYiemTrTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a2m6Zmi77ya6K6h566X5py65a2m6ZmiOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzkuJPkuJrvvJo7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOe9kee7nOW3peeoizs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86KGM5pS/54+t77ya572R57uc5bel56iLMTMoMik7Pj47Pjs7Pjt0PEAwPDtAMDw7OztAMDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs7Ozs+Ozs7Ozs7Ozs7Oz47Ozs7Ozs7Ozs+Ozs+O3Q8QDA8Ozs7Ozs7Ozs7Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxHREdZRFg7Pj47Pjs7Pjt0PEAwPDs7Ozs7Ozs7Ozs+Ozs+Oz4+Oz4+Oz4wRXi2T0BNvosaeOvzacaXoPZQkQ==',
         'ddlXN':year, 
         'ddlXQ':term,    
         'txtQSCJ':'0',
         'txtZZCJ':'100',
         'Button5':'%B0%B4%D1%A7%C4%EA%B2%E9%D1%AF'
        } 
         
         
        #post请求头部
        headers = {
            
         'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            
            'Host':    'jwgldx.gdut.edu.cn',
            'Cookie':cookies,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',  
            'Referer' : 'http://jwgldx.gdut.edu.cn/xscj.aspx?xh='+self.username+'&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121605',
         #'Content-Type': 'application/x-www-form-urlencoded',
         #'Content-Length' :474,
            'Connection' : 'Keep-Alive'
         
        }
        
        NewUrl = 'http://jwgldx.gdut.edu.cn/xscj.aspx?xh='+self.username+'&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121605'
        #NewUrl = 'http://jwgl.gdut.edu.cn/xskscx.aspx?xh=3113006459&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121604'
        data = urllib.urlencode(postData)
        request = urllib2.Request(  NewUrl,data,headers)
        try:
        # 访问页面
         response = urllib2.urlopen(request)
        # cur_url =  response.geturl()
        # print "cur_url:",cur_url
         status = response.getcode()
#         print status
        except urllib2.HTTPError, e:
         print e.code
        #将响应的网页打印到文件中，方便自己排查错误
        #必须对网页进行解码处理
        res= response.read().decode("gb2312")
        response.close()
        print u'1：计算绩点并输出成绩单\n2：计算绩点'
        choice = raw_input(u'请选择要使用的功能！')
        if choice=='1':
            self.getGradeInfo(res,year)
        else: 
            self.getGpa(res)
#        outfile =open("c:\\rel_ip.txt","w")
#        print >> outfile , "%s"   % ( res.encode('gb2312'))
#        print "%s"   % ( res.encode('gb2312'))
#        f = open('c:\\rel_ip.txt','r')
#        content= f.read()
#        print '%s' % (content.decode('gb2312'))
           
    def youxiu(self):
        return 4.5
                
    def lianghao(self):
        return 3.5
            
    def zhongdeng(self):
        return 2.5
            
    def jige(self):
        return 1.5
    
    #输出平均绩点
#    平均学分绩点（ GPA ）＝∑（课程学分 * 课程绩点）/∑ 课程学分
#    学习成绩与绩点数的折算方法为： 
#    90～100分折合为4.0～5.0绩点，优秀折合为4.5绩点；
#    80～89分折合为3.0～3.9绩点，良好折合为3.5绩点； 
#    70～79分折合为2.0～2.9绩点，中等折合为2.5绩点；
#    60～69分折合为1.0～1.9绩点，及格折合为1.5绩点； 
#    59分以下（不及格）折合为0绩点。
    def getGpa(self,res):
        operator = {u'优秀':self.youxiu,u'良好':self.lianghao,u'中等':self.zhongdeng,u'及格':self.jige} 
        a = re.search('<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="DataGrid1" width="100%">(.*?)</table>',res,re.S)
#        print a
        if a:
            m = re.findall('<tr.*?<td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td><td>.*?</td>.*?</tr>',a.group(),re.S)
            #m = re.findall('<TR>.*?<p.*?<p.*?<p.*?<p.*?<p.*?>(.*?)</p>.*?<p.*?<p.*?>(.*?)</p>.*?</TR>',content.decode('gb2312'),re.S)'
        for i in m:
#            print i[0]+'  '+i[1]
            self.credit.append(i[1])
            self.grades.append(i[0])
            
        #计算总绩点
        sum = 0.0
        weight = 0.0
        for i in range(len(self.credit)):
            if  i==0:
                self.gpa.append(u'绩点'.encode('gb2312'))
                continue
            if(self.grades[i].isdigit()):
                temp = string.atof(self.grades[i])-50.0 if string.atof(self.grades[i])>=60 else 0.0
                sum += string.atof(self.credit[i])*string.atof(temp/10.0)
            else: 
                temp = operator.get(self.grades[i])()
                sum+=  string.atof(self.credit[i])*temp
            self.gpa.append(temp)
#            print temp
            weight += string.atof(self.credit[i])
            
        print u'本学期平均绩点为:',sum/weight
        return sum/weight
    
    #输出成绩表单并写文件
    def getGradeInfo(self,res,year):
        temp = []        
        avg = self.getGpa(res)        
        a = re.search('<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="DataGrid1" width="100%">(.*?)</table>',res,re.S)
#        print a
        if a:
            m = re.findall('<tr.*?<td>.*?</td><td>(.*?)</td><td>.*?</td><td>(.*?)</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td><td>.*?</td>.*?</tr>',a.group().encode('gb2312'),re.S)
            print u'学生成绩：\n'
            with open(self.nickname+year+u'的成绩单.csv', 'wb') as csvfile:
                spamwriter = csv.writer(csvfile,dialect='excel')            
                for i in range(len(m)):
                    temp = []                    
                    for a in m[i]:
                        temp.append(a)
                        print a.decode('gb2312'),
                    temp.append(self.gpa[i])
                    spamwriter.writerow(temp)  
                    print '\n'
                spamwriter.writerow(['','',u'本学期平均绩点为'.encode('gb2312'),avg])       
            print u'成绩单已成功保存在./'+self.nickname+year+u'的成绩单.csv，请注意查看'
             
    #获取课表
    def getTimeTable(self,cookies,year,term):
        year = year
        term = term
        if year == '2014-2015' and term == '1':
            viewstate = 'dDwzOTI4ODU2MjU7dDw7bDxpPDE+Oz47bDx0PDtsPGk8MT47aTwyPjtpPDQ+O2k8Nz47aTw5PjtpPDExPjtpPDEzPjtpPDE1PjtpPDI0PjtpPDI2PjtpPDI4PjtpPDMwPjtpPDMyPjtpPDM0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcZTs+Pjs+Ozs+O3Q8dDxwPHA8bDxEYXRhVGV4dEZpZWxkO0RhdGFWYWx1ZUZpZWxkOz47bDx4bjt4bjs+Pjs+O3Q8aTwzPjtAPDIwMTUtMjAxNjsyMDE0LTIwMTU7MjAxMy0yMDE0Oz47QDwyMDE1LTIwMTY7MjAxNC0yMDE1OzIwMTMtMjAxNDs+PjtsPGk8MT47Pj47Oz47dDx0PDs7bDxpPDE+Oz4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a2m5Y+377yaMzExMzAwNjQ1OTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85aeT5ZCN77ya6YKT5ZiJ6ZOtOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzlrabpmaLvvJrorqHnrpfmnLrlrabpmaI7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOS4k+S4mu+8mue9kee7nOW3peeoizs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86KGM5pS/54+t77ya572R57uc5bel56iLMTMoMik7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MT47aTwxPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+O2w8aTwwPjs+O2w8dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0PjtpPDU+O2k8Nj47aTw3Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDwwMDAwNjgyNTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MDAwMDY4MjU7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOiwgzAwNzg7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCgyMDE0LTIwMTUtMiktMjQxMDA3MzUtMDAwMDY4MjUtMTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86K6h566X5py657uE5oiQ5Y6f55CGOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzlkagy56ysOOiKgui/nue7rTLoioJ756ysMi0y5ZGofS/mlZk1LTEwNy/lj7bmnpfplIs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWRqDPnrKwz6IqC6L+e57utMuiKgnvnrKwzLTPlkajljZXlkah9L+aVmTUtMTA3L+WPtuael+mUizs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MjAxNS0wMy0wNC0xNC00MTs+Pjs+Ozs+Oz4+Oz4+Oz4+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDE+O2k8MT47bDw+Oz4+Oz47Ozs7Ozs7Ozs7PjtsPGk8MD47PjtsPHQ8O2w8aTwxPjs+O2w8dDw7bDxpPDA+O2k8MT47aTwyPjtpPDM+O2k8ND47aTw1PjtpPDY+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPOaVsOaNrue7k+aehOivvueoi+iuvuiuoTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85p2o5Yqy5rabOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxLjA7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDE5LTE5Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47Pj47Pj47Pj47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MD47aTwwPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDM+O2k8Mz47bDw+Oz4+Oz47Ozs7Ozs7Ozs7PjtsPGk8MD47PjtsPHQ8O2w8aTwxPjtpPDI+O2k8Mz47PjtsPHQ8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDIwMTQtMjAxNTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Mjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85pWw5o2u57uT5p6E5a6e6aqMOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnajlirLmtps7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEuMDs+Pjs+Ozs+Oz4+O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDIwMTQtMjAxNTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Mjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86K6h566X5py657uE5oiQ5Y6f55CG5a6e6aqMOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzlj7bmnpfplIs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEuMDs+Pjs+Ozs+Oz4+O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDIwMTQtMjAxNTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Mjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85pWw5o2u57uT5p6E6K++56iL6K6+6K6hOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnajlirLmtps7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEuMDs+Pjs+Ozs+Oz4+Oz4+Oz4+Oz4+Oz4+Oz6xV55Kloo59ME/IcANdwVqo2p94A=='
        elif year == '2014-2015' and term == '2':
            viewstate = 'dDwzOTI4ODU2MjU7dDw7bDxpPDE+Oz47bDx0PDtsPGk8MT47aTwyPjtpPDQ+O2k8Nz47aTw5PjtpPDExPjtpPDEzPjtpPDE1PjtpPDI0PjtpPDI2PjtpPDI4PjtpPDMwPjtpPDMyPjtpPDM0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcZTs+Pjs+Ozs+O3Q8dDxwPHA8bDxEYXRhVGV4dEZpZWxkO0RhdGFWYWx1ZUZpZWxkOz47bDx4bjt4bjs+Pjs+O3Q8aTwzPjtAPDIwMTUtMjAxNjsyMDE0LTIwMTU7MjAxMy0yMDE0Oz47QDwyMDE1LTIwMTY7MjAxNC0yMDE1OzIwMTMtMjAxNDs+PjtsPGk8MT47Pj47Oz47dDx0PDs7bDxpPDA+Oz4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a2m5Y+377yaMzExMzAwNjQ1OTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85aeT5ZCN77ya6YKT5ZiJ6ZOtOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzlrabpmaLvvJrorqHnrpfmnLrlrabpmaI7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOS4k+S4mu+8mue9kee7nOW3peeoizs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86KGM5pS/54+t77ya572R57uc5bel56iLMTMoMik7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MD47aTwwPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDA+O2k8MD47bDw+Oz4+Oz47Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPHA8cDxsPFBhZ2VDb3VudDtfIUl0ZW1Db3VudDtfIURhdGFTb3VyY2VJdGVtQ291bnQ7RGF0YUtleXM7PjtsPGk8MT47aTwwPjtpPDA+O2w8Pjs+Pjs+Ozs7Ozs7Ozs7Oz47Oz47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MT47aTwxPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+O2w8aTwwPjs+O2w8dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDwyMDE0LTIwMTU7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOaVsOWtl+mAu+i+keWPiuezu+e7n+iuvuiuoeWunumqjDs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85byg6Z2ZOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxLjA7Pj47Pjs7Pjs+Pjs+Pjs+Pjs+Pjs+Pjs+xpwxIA7xD2huK8RwSK00S5JUaS4='
        else:
            viewstate = 'dDwzOTI4ODU2MjU7dDw7bDxpPDE+Oz47bDx0PDtsPGk8MT47aTwyPjtpPDQ+O2k8Nz47aTw5PjtpPDExPjtpPDEzPjtpPDE1PjtpPDI0PjtpPDI2PjtpPDI4PjtpPDMwPjtpPDMyPjtpPDM0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcZTs+Pjs+Ozs+O3Q8dDxwPHA8bDxEYXRhVGV4dEZpZWxkO0RhdGFWYWx1ZUZpZWxkOz47bDx4bjt4bjs+Pjs+O3Q8aTwzPjtAPDIwMTUtMjAxNjsyMDE0LTIwMTU7MjAxMy0yMDE0Oz47QDwyMDE1LTIwMTY7MjAxNC0yMDE1OzIwMTMtMjAxNDs+PjtsPGk8MT47Pj47Oz47dDx0PDs7bDxpPDA+Oz4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a2m5Y+377yaMzExMzAwNjQ1OTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85aeT5ZCN77ya6YKT5ZiJ6ZOtOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzlrabpmaLvvJrorqHnrpfmnLrlrabpmaI7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOS4k+S4mu+8mue9kee7nOW3peeoizs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w86KGM5pS/54+t77ya572R57uc5bel56iLMTMoMik7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtsPGk8MT47PjtsPHQ8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MD47aTwwPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDA+O2k8MD47bDw+Oz4+Oz47Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPHA8cDxsPFBhZ2VDb3VudDtfIUl0ZW1Db3VudDtfIURhdGFTb3VyY2VJdGVtQ291bnQ7RGF0YUtleXM7PjtsPGk8MT47aTwwPjtpPDA+O2w8Pjs+Pjs+Ozs7Ozs7Ozs7Oz47Oz47dDxAMDxwPHA8bDxQYWdlQ291bnQ7XyFJdGVtQ291bnQ7XyFEYXRhU291cmNlSXRlbUNvdW50O0RhdGFLZXlzOz47bDxpPDE+O2k8MT47aTwxPjtsPD47Pj47Pjs7Ozs7Ozs7Ozs+O2w8aTwwPjs+O2w8dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDwyMDE0LTIwMTU7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOaVsOWtl+mAu+i+keWPiuezu+e7n+iuvuiuoeWunumqjDs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85byg6Z2ZOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxLjA7Pj47Pjs7Pjs+Pjs+Pjs+Pjs+Pjs+Pjs+xpwxIA7xD2huK8RwSK00S5JUaS4='
        
        postData = {   
         '__EVENTARGUMENT': '',
         '__EVENTTARGET':'xqd', 
         '__VIEWSTATE':viewstate,    
         'xnd':year,
         'xqd':term
        } 
         
         
        #post请求头部
        headers = {
            
         'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            
            'Host':    'jwgldx.gdut.edu.cn',
            'Cookie':cookies,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',  
            'Referer' : 'http://jwgldx.gdut.edu.cn/xskbcx.aspx?xh='+self.username+'&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121603',
         #'Content-Type': 'application/x-www-form-urlencoded',
         #'Content-Length' :474,
            'Connection' : 'Keep-Alive'
         
        }
        
        NewUrl = 'http://jwgldx.gdut.edu.cn/xskbcx.aspx?xh='+self.username+'&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121603'
        #NewUrl = 'http://jwgl.gdut.edu.cn/xskscx.aspx?xh=3113006459&xm=%B5%CB%BC%CE%C3%FA&gnmkdm=N121604'
        data = urllib.urlencode(postData)
        request = urllib2.Request(  NewUrl,data,headers)
        try:
        # 访问页面
         response = urllib2.urlopen(request)
        # cur_url =  response.geturl()
        # print "cur_url:",cur_url
         status = response.getcode()
#         print status
        except urllib2.HTTPError, e:
         print e.code
        #将响应的网页打印到文件中，方便自己排查错误
        #必须对网页进行解码处理
        res= response.read().decode("gb2312")
        response.close()
#        print res
        a = re.search('<table id="Table1" class="blacktab" bordercolor="Black" border="0" width="100%">(.*?)</table>',res,re.S)
        if a:
            print a
            outfile = open(self.nickname+year+u'第'+term+u'学期的课表.html','w')
            print >> outfile , "%s"   % ( a.group().encode('utf-8'))
            parser = html2csv()
            parser.feed( a.group() )
            open(self.nickname+year+u'第'+term+u'学期的课表.csv','w+b').write( parser.getCSV() )
            print u'课表已成功保存在./'+self.nickname+year+u'第'+term+u'学期的课表.csv，请注意查看'
        
    
    #主函数
    def main(self):
        text = self.getCode()
        cookies = self.login(text)
        if cookies!= -1:
            flag = 1
            while (flag == 1):
                print u'登入成功\n1.查询个人成绩(学年)\t2.获取个人课表'
                print u'请输入你要使用的功能:  '
                choice = raw_input()
                pattern = re.compile(r'20\d\d-20\d\d')
                if choice =='1':
                    print u'请选择你要查询的学年:(格式为2013-2014)'
                    
                    year = raw_input()
                    res = pattern.match(year)
                    if res == None:
                        print u'输入错误，格式应为20xx－20xx。'
                        continue
                    flag = 0
                    self.getGrade(cookies,year)
                elif choice =='2':
                    print u'请选择你要查询的学年:(格式为2013-2014)'
                    year = raw_input()
                    res = pattern.match(year)
                    if res == None:
                        print u'输入错误，格式应为20xx－20xx。'
                        continue
    
                    print u'请选择你要查询的学期:  '
                    print u'1.第1学期\t2.第2学期'
                    if raw_input()=='1':
                        term = '1'
                    else:
                        term = '2'
                    self.getTimeTable(cookies,year,term)
                    flag = 0
                else:
                    print u'输入错误'
                
#        print text
    
    
login = gdutLogin()
login.main()
     
