#coding: UTF-8
import socket  
import thread  
import urlparse  
import select
import re
import r_text
import ContentType
import _Record
import sys
sys.stderr = None  
BUFLEN=4096
#scr为报文，x为要替换成为的，sign为要被替换掉的
def content_len(scr,x,sign_t):
    #print scr
    count2=scr.count(sign_t)
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
    cha=cha*count2
    #print "count2:",count2
    #print "s2:",s2
    #print "cha:",cha
    n_l=s2+cha
    #print n_l
    return n_l
#scr为报文，x为要替换成为的，sign为要被替换掉的
def update_cl(scr,x,sign_t):
    c_len=str(content_len(scr,x,sign_t))
    scr=r_text.r_replace(r'Content-Length:\s*\d*',"Content-Length: "+c_len,scr)
    return scr
 
  
class Proxy(object):  
    def __init__(self,conn,addr,text):  
        self.source=conn  
        self.request=""  
        self.headers={}  
        self.destnation=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.req=text
        self.run()
        self.req=""
  
    def get_headers(self):  
        header=''  
        while True:  
            #header+=self.source.recv(BUFLEN)
            header=header+self.req
            index=header.find('\r\n')  
            if index >0:  
                break  
        #firstLine,self.request=header.split('\r\n',1)
            if len(header)<10:
                thread.exit_thread()
        firstLine=header[:index]
        #print "head:",header
        #print firstLine
        self.request=header[index+2:]  
        self.headers['method'],self.headers['path'],self.headers['protocol']=firstLine.split()  
  
    def conn_destnation(self):  
        url=urlparse.urlparse(self.headers['path'])
        #print url[1]
        hostname=url[1]  
        port="80"  
        if hostname.find(':') >0:  
            addr,port=hostname.split(':')  
        else:  
            addr=hostname  
        port=int(port)  
        ip=socket.gethostbyname(addr)
        if ip=="0.0.0.0":
            thread.exit_thread()
        #print ip,port
        self.destnation.connect((ip,port))  
        data="%s %s %s\r\n" %(self.headers['method'],self.headers['path'],self.headers['protocol'])
        a_request=data+self.request
        p = re.compile(r'Accept-Encoding[^\n]*\n')
        #p = re.compile(r'Accept-Encoding.*')
        accept_encoding=""
        accept_encoding=accept_encoding.join(p.findall(a_request))
        a_request=a_request.replace(accept_encoding,'')
        if a_request.find('&lt;chiruomorg&gt;') >0:  
            a_request=update_cl(a_request,'<chiruomorg>','&lt;chiruomorg&gt;')
            a_request=a_request.replace('&lt;chiruomorg&gt;','<chiruomorg>')
        if a_request.find('%26lt%3Bchiruomorg%26gt%3B') >0:
            a_request=update_cl(a_request,'%3Cchiruomorg%3E','%26lt%3Bchiruomorg%26gt%3B')
            a_request=a_request.replace('%26lt%3Bchiruomorg%26gt%3B','%3Cchiruomorg%3E')
        self.destnation.send(a_request)  
        #print data+self.request
        self.req=a_request
        #print a_request
  
    def renderto(self,req):
        readsocket=[self.destnation]
        a_data=""
        while True:  
            data=''  
            (rlist,wlist,elist)=select.select(readsocket,[],[],3)  
            if rlist:  
                data=rlist[0].recv(BUFLEN)  
                if len(data)>0:  
                    self.source.send(data)
                    a_data=a_data+data
                else:  
                    break
        if ContentType.Content_Is_Text(ContentType.Get_Content_Type(a_data)):
            print "in 1"
            if r_text.In_Text(r'%3Cchiruomorg%3E',req) or r_text.In_Text(r'<chiruomorg>',req):
                print "in 2"
                r_text.write_dbm(req,a_data,"Screq","c")
            _Record.record_pro(req,a_data)
                    #print data
                    #print 'S'
        #self.destnation.close()
        #self.source.close()
        
    def run(self):  
        self.get_headers()  
        self.conn_destnation()  
        self.renderto(self.req)  
  
  
  
class Server(object):  
  
    def __init__(self,host,port,handler=Proxy):  
        self.host=host  
        self.port=port  
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.server.bind((host,port))  
        self.server.listen(30)  
        self.handler=handler  
  
    def start(self):
        while True:  
            try:
                conn,addr=self.server.accept()
                #print "New accept"
                thread.start_new_thread(Engine,(self,conn,addr))
            except:  
                pass


class Engine(object):
    def __init__(self,Server,conn,addr):
        len_req=int(0)    #content-length的值
        #len_data=int(0)  #实际内容长度
        s_data=""
        s_len_data=int(0)
        while True:
            data=""
            data=conn.recv(BUFLEN)
##            if data :
##                print data
            if data.startswith("GET"or"HEAD") and data:
                thread.start_new_thread(Server.handler,(conn,addr,data))
                #print "New Get thread"
                continue
            elif data :
                print "Ready to Post"
                len_data=len(data)
                if r_text.In_Text(r'Content-Length:',data):
                    print "First Post"
                    p1 = re.compile(r'Content-Length:\s*\d*')
                    l1=p1.findall(data)
                    s1=""
                    s1=s1.join(l1)
                    p2= re.compile(r'\d*')
                    l2=p2.findall(s1)
                    s2=""
                    s2=s2.join(l2)
                    len_req=int(s2)
                    print "len_req:",len_req
                    index=data.find('\r\n\r\n')
                    con=data[index+4:]
                    print "con:\n",con
                    #print len(con)
                    len_data=len(con)
                    s_len_data=len_data
                    print "len_data_t:",len_data
                    s_data=data
                else :
##                    print "Post After"
##                    print "len_data_before",len_data
##                    len_data=len_data+len(data)
##                    print "len_data:",len_data
                    s_len_data=s_len_data+len_data
                    s_data=s_data+data
                if s_len_data==len_req :
                    thread.start_new_thread(Server.handler,(conn,addr,s_data))
                    
                    print "New POST thread"
 
                

  
if __name__=='__main__':  
    s=Server('127.0.0.1',8083)  
    s.start()  
