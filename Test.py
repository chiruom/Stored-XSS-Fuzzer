#coding: UTF-8
import Http
import anydbm
#import XSScheck
import r_text
import report   #报告漏洞
import urllib
import os
import socket
import thread
import urlparse
import select
import httplib2
import re

BUFLEN=8192000 #缓冲区
sign="%3Cchiruomorg%3E"
sign2="<chiruomorg>"
#数据的输入点
f_screq=anydbm.open('Screq', 'r')
#脏数据报文记录
if os.path.exists(r'.\_Record\html'):
    f_record_html=anydbm.open(r'.\_Record\html', 'r')
if os.path.exists(r'.\_Record\html_js'):
    f_record_html_js=anydbm.open(r'.\_Record\html_js', 'r')
if os.path.exists(r'.\_Record\js'):
    f_record_js=anydbm.open(r'.\_Record\js', 'r')
if os.path.exists(r'.\_Record\json'):
    f_record_json=anydbm.open(r'.\_Record\json', 'r')
if os.path.exists(r'.\_Record\in_html'):
    f_record_in_html=anydbm.open(r'.\_Record\in_html', 'r')
#攻击向量
f_xss_html=open(r'.\_XSS\xss_html.txt','r')  
f_xss_html_js=open(r'.\_XSS\xss_html_js.txt','r')
f_xss_js=open(r'.\_XSS\xss_js.txt','r')
f_xss_json=open(r'.\_XSS\xss_json.txt','r')
f_xss_in_html=open(r'.\_XSS\xss_in_html.txt','r')
f_xss_css=open(r'.\_XSS\xss_css.txt','r')
d_xss_html=f_xss_html.readlines()
d_xss_html_js=f_xss_html_js.readlines()
d_xss_js=f_xss_js.readlines()
d_xss_json=f_xss_json.readlines()
d_xss_css=f_xss_css.readlines()
##d_xss_in_html=f_xss_in_html.readlines()
##
##
####并非通用的函数
##def check(xssfile,recordfile,keyword):
##    for x in xssfile:
##        print "check"+keyword
##        x2=urllib.quote(x)
##        for scr in f_screq:
##            print "Now in for"
##            scr=scr.replace(sign,x2)
##            print "start"
##            Http.get_response(scr)
##            print "end"
##            for a in recordfile:
##                print "start"
##                req=Http.get_response(a)
##                print "end"
##                if r_text.In_Text(x,req):
##                    report.report_pro(x,a,req,keyword)
##



def content_len(scr,x,sign_t,count):
    s_l=len(sign_t)
    x_l=len(x)
    cha=x_l-s_l
    #print "cha:",cha
    p1 = re.compile(r'Content-Length:\s*\d*')
    l1=p1.findall(scr)
    s1=""
    s1=s1.join(l1)
    p2= re.compile(r'\d*')
    l2=p2.findall(s1)
    s2=""
    s2=s2.join(l2)
    s2=int(s2)
    cha=cha*count
    #print count
    n_l=s2+cha
    return n_l
    
    

if __name__=='__main__':
    print "Now Start Check"
    if os.path.exists(r'.\_Record\html'):
    ##输出点在html标签<>之外
        for x in d_xss_html:  
            x2=urllib.quote(x)
            #print x2
            print "check _xss_html..."
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                #print scr
                #print "start"
                resp=Http.http(scr)
                #print "end"
                #print resp
                for a in f_record_html:
                    req=Http.http(a)
                    #print req
                    if r_text.In_Text2(x,req):
                        report.report_pro(x,a,req,"html")


    if os.path.exists(r'.\_Record\in_html'):                
    ##输出点在html标签<>之中,html属性当中
        for x in d_xss_in_html:
            x2=urllib.quote(x)
            # print x
            print "check _xss_in_html..."
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                resp=http_send(scr)
                #print resp
                for a in f_record_in_html:
                    req=Http.get_response(a)
                    x3=r'<[^>]*=\s*".*'+x+'.*"' 
                    if r_text.In_Text3(x3,req):
                        report.report_pro(x,a,req,"html")


    if os.path.exists(r'.\_Record\html_js'):       
    ##输出点在html的非js标签的js中   （各种on的情况等）  
        for x in d_xss_html_js:
            print "check _xss_html_js..."
            x2=urllib.quote(x)
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                Http.get_response(scr)
                for a in f_record_html_js:
                    req=Http.get_response(a)
                    if r_text.In_Text2(x,req):
                        report.report_pro(x,a,req,"xss_html_js")


    if os.path.exists(r'.\_Record\js'):    
    ##输出点在html的js标签中或js文件中
        for x in d_xss_js:
            print "check _xss_js..."
            x2=urllib.quote(x)
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                Http.get_response(scr)
                for a in f_record_js:
                    req=Http.get_response(a)
                    if r_text.In_Text2(x,req):
                        report.report_pro(x,a,req,"js")


                        
    if os.path.exists(r'.\_Record\json'):            
    ##输出点在json中
        for x in d_xss_json:
            print "check _xss_json..."
            x2=urllib.quote(x)
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                Http.get_response(scr)
                for a in f_record_json:
                    req=Http.get_response(a)
                    if r_text.In_Text2(x,req):
                        report.report_pro(x,a,req,"json")


    if os.path.exists(r'.\_Record\css'):            
    ##输出点在css中
        for x in d_xss_css:
            print "check _xss_css..."
            x2=urllib.quote(x)
            for scr in f_screq:
                cou=scr.count(sign)
                cou2=scr.count(sign2)
                scr=scr.replace(sign,x2)
                scr=scr.replace(sign2,x)
                c_len=str(content_len(scr,x2,sign,cou))
                c_len=str(content_len(scr,x,sign2,cou2))
                scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
                Http.get_response(scr)
                for a in f_record_json:
                    req=Http.get_response(a)
                    if r_text.In_Text2(x,req):
                        report.report_pro(x,a,req,"css")
                    



        
        
            
    print "Check Over"
    raw_input("Press Enter to continue: ")

