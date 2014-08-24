#coding: UTF-8
import re
import anydbm
import thread 

##基于正则的字符串替换
def r_replace(re2,des,data):
    p = re.compile(re2)
    tem=""
    tem=tem.join(p.findall(data))
    data=data.replace(tem,des)
    return data


##i为请求，c为响应。把请求响应报文写入持久化字典
def write_dbm(i,c,path,arg):
    lock = thread.allocate_lock()      
    lock.acquire()
    Record=anydbm.open(path,arg)
    Record[i]=c
    Record.close()    
    lock.release()

##判断正在表达式word的语句是否在字符串data中
def In_Text(word,data):
    if not data:
        data=" "
    if not word:
        word=" "
##    word=word.replace('(',r'\(')
##    word=word.replace(')',r'\)')
##    word=word.replace('*',r'\*')
##    word=word.replace('.',r'\.')
##    word=word.replace('?',r'\?')
##    word=word.replace('+',r'\+')
##    word=word.replace('$',r'\$')
##    word=word.replace('^',r'\^')
##    #word=word.replace('\',r'\\')
##    word=word.replace('/',r'\/')
##    word=word.replace('[',r'\/')
##    word=word.replace(']',r'\/')
##    word=word.replace('{',r'\{')
##    word=word.replace('{',r'\}')
##    word=word.replace('|',r'\|')
##    data=data.replace('\n','')
##    data=data.replace('\r','')
    p2 = re.compile(r''+word+'')
    #print brequest
    record_result=p2.findall(data)
    #print "word is:",word
    #print "data is:",data
    #print record_result
    if record_result :
        return True
    else:
        return False


def In_Text2(word,data):
    if not data:
        data=" "
    if not word:
        word=" "
    word=word.replace('(',r'\(')
    word=word.replace(')',r'\)')
    word=word.replace('*',r'\*')
    word=word.replace('.',r'\.')
    word=word.replace('?',r'\?')
    word=word.replace('+',r'\+')
    word=word.replace('$',r'\$')
    word=word.replace('^',r'\^')
    #word=word.replace('\',r'\\')
    word=word.replace('/',r'\/')
    word=word.replace('[',r'\/')
    word=word.replace(']',r'\/')
    word=word.replace('{',r'\{')
    word=word.replace('{',r'\}')
    word=word.replace('|',r'\|')
    data=data.replace('\n','')
    data=data.replace('\r','')
    p2 = re.compile(r''+word+'')
    #print brequest
    record_result=p2.findall(data)
    #print "word is:",word
    #print "data is:",data
    #print record_result
    if record_result :
        return True
    else:
        return False


if __name__=='__main__':
    word="""<script>alert("XSS")</script>"""
    data="""fdsaf"ds
fefwf<script>alert("XSS")</script>dsfdsfs
gtgrbre"""
    print In_Text2(word,data)






    

