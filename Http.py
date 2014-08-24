#coding: UTF-8
import socket
import thread
import urlparse
import select
import re
import httplib2
import urllib
#import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

BUFLEN=8192000 #缓冲区

#重写BaseHTTPRequestHandler类
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
 
    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


#接收一个HTTP请求报文，返回其响应报文
def http(request):
    headers={}
    destnation=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    header=''
    while True:
        header+=request
        index=header.find('\n')
        if index >0:
            break
    #firstLine,self.request=header.split('\r\n',1)
    firstLine=header[:index]
    request=header[index+1:]
    headers['method'],headers['path'],headers['protocol']=firstLine.split()
    url=urlparse.urlparse(headers['path'])
    hostname=url[1]
    port="80"
    if hostname.find(':') >0:
        addr,port=hostname.split(':')
    else:
        addr=hostname
    port=int(port)
    ip=socket.gethostbyname(addr)
    #print "IP\PORT:\n",ip,port                          #已获取目标远端服务器IP及端口
    destnation.connect((ip,port))       #套接字连接远端服务器
    data="%s %s %s\r\n" %(headers['method'],headers['path'],headers['protocol'])
    p = re.compile(r'Accept-Encoding[^\n]*\n')
    #p = re.compile(r'Accept-Encoding.*')
    accept_encoding=""
    accept_encoding=accept_encoding.join(p.findall(request))
    request=request.replace(accept_encoding,'')
    destnation.send(data+request)         #向远端服务器发送请求报文
    #print "Request:\n"+data+request       #打印请求报文

    response=""       
    while True:
        data=''
        #rlist,wlist,elist)=select.select(readsocket,[],[],3)
        #if rlist:
        data=destnation.recv(BUFLEN)    #接收服务器返回的响应报文  
        #print "Respond:\n",data       #打印响应报文
        if len(data)>0:
            response+=data    #self.source套接字的目标是本地浏览器，向目标浏览器发送来自远端服务器的响应报文
        else:
            break
    return response



#接收一个HTTP请求头部的名称和一个请求报文，返回这个头部的内容
def get_head(head,request):
    requset=request.replace("Cookie:\r\n","Cookie:")
    head=head.replace("-","\-")
    re_str=head+":.*"
    #print re_str
    p = re.compile(re_str)
    Content_Type=""
    Content_Type=Content_Type.join(p.findall(request))
    #print Content_Type
    #print Content_Type
    re_str2=head+":"
    #print re_str2
    q= re.compile(re_str2)
    Content_Type2=""
    Content_Type2=Content_Type2.join(q.findall(Content_Type))
    Content_Type=Content_Type.replace(Content_Type2,"")
    #print Content_Type
##    r= re.compile(r';.*')
##    Content_Type3=""
##    Content_Type3=Content_Type3.join(r.findall(Content_Type))
##    Content_Type=Content_Type.replace(Content_Type3,"")
    #print Content_Type
    return Content_Type

#接收一个HTTP请求报文，返回该请求所使用的HTTP方法
def get_method(request):
    cn=request.find('\n')
    firstLine=request[:cn]
    #print firstLine[:len(firstLine)-9]
    line=firstLine.split()
    method=line[0]
    #targetHost=line[1]
    return method


#接收一个HTTP请求报文，返回该请求的target
def get_target(request):
    cn=request.find('\n')
    firstLine=request[:cn]
    #print firstLine[:len(firstLine)-9]
    line=firstLine.split()
    #method=line[0]
    target=line[1]
    return target

#以字典形式返回post的数据
def get_postdata(request):
    cn=request.find('\r\n\r\n')
    #print cn
    cn=cn+4
    postdata=request[cn:]
    #print postdata
    postdir=dict(re.findall(r'(?P<name>[^=&\r\n]*)=(?P<value>[^&\r\n]*)', postdata))
    #print postdir
    return postdir

#以字典形式返回所有的请求头
def get_headers(request):
    request2 = HTTPRequest(request)
    return dict(request2.headers)

#发送HTTP请求报文，取得响应主体
def get_response(request):
    resp=http(request)
    cn=resp.find('\r\n\r\n')
    #print cn
    cn=cn+4
    resp2=resp[cn:]
    return resp2

    
##    h = httplib2.Http()
##    headers=get_headers(request)
##    method=get_method(request)
##    #print method
##    url2=get_target(request)
##    host=get_head("Host",request)
##    url="http://"+host+url2
##    #url= 'http://202.115.47.141/loginAction.do'
##    if method=="GET":
##        resp, content = h.request(url, 'GET', headers=headers)
##    if method=="POST":
##        postdata=get_postdata(request)
##        data2=urllib.urlencode(postdata)
##        resp, content = h.request(url, 'POST',  headers=headers,body=data2)
##        return content
                      
    

if __name__=='__main__':
    #request='POST /loginAction.do HTTP/1.1\r\nHost: 202.115.47.141\r\nProxy-Connection: keep-alive\r\nContent-Length: 26\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nOrigin: http://202.115.47.141\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36\r\nContent-Type: application/x-www-form-urlencoded\r\nReferer: http://202.115.47.141/login.jsp\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nCookie: JSESSIONID=adbLCbvOdTi0gd1qF0REu\r\n\r\nzjh=1142053025&mm=30501591'
    request="""POST http://127.0.0.1/ch4/edit.php HTTP/1.1
Host: 127.0.0.1
Proxy-Connection: keep-alive
Content-Length: 1320
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://127.0.0.1/ch4/edit.php
Accept-Language: zh-CN,zh;q=0.8
Cookie: chuser=admin; chupwd=admin; PHPSESSID=19gqm3fe8d71cfetsir2pgh1d3

uname=%3Cchiruomorg%3E&ucountry=%3Cchiruomorg%3E&um=%3Cchiruomorg%3E&uemail=%3Cchiruomorg%3E&uaddress=%3Cchiruomorg%3E&submit=Save
"""
    #print request
#测试http函数
    print "start"
    response=http(request)
    print "end"
    #print response

#测试get_head函数 
##    print request
##    result=get_head("Cookie",request)
##    print result

#测试get_targethost函数
##    target=get_target(request)
##    print target


#测试get_response函数  
##    response=get_response(request)
##    print response

#测试get_headers函数  
##    response=get_headers(request)
##    print response

#测试get_headers函数  
##    response=get_headers(request)
##    print response
    
