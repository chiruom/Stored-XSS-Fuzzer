#coding: UTF-8
import re


#接收http响应报文作参数，返回其contenttpye字段冒号后的字符串
def Get_Content_Type(data):
    p = re.compile(r'Content\-.ype:.*')
    Content_Type=""
    Content_Type=Content_Type.join(p.findall(data))
    #print Content_Type
    q= re.compile(r'Content\-.ype:')
    Content_Type2=""
    Content_Type2=Content_Type2.join(q.findall(Content_Type))
    Content_Type=Content_Type.replace(Content_Type2,"")
    #print Content_Type
    r= re.compile(r';.*')
    Content_Type3=""
    Content_Type3=Content_Type3.join(r.findall(Content_Type))
    Content_Type=Content_Type.replace(Content_Type3,"")
    #print Content_Type
    return Content_Type

#接收contenttpye字段冒号后的字符串，判断该响应报文类型是否为文本型
def Content_Is_Text(Content_Type):
    ty=Content_Type.split('/')
    text=["text","javascript","html","css","x-javascript","application","json","multipart","form-data"]
    for i in ty:
        if i in text:
            return True
    return False

#接收contenttpye字段冒号后的字符串，判断该响应报文类型是否为Json型
def Content_Is_Json(Content_Type):
    ty=Content_Type.split('/')
    text=["json"]
    for i in ty:
        if i in text:
            return True
    return False

def Content_Is_Html(Content_Type):
    ty=Content_Type.split('/')
    text=["html","text"]
    for i in ty:
        if i in text:
            return True
    return False

def Content_Is_js(Content_Type):
    ty=Content_Type.split('/')
    text=["x-javascript","javascript","application"]
    for i in ty:
        if i in text:
            return True
    return False
    

def Content_Is_css(Content_Type):
    ty=Content_Type.split('/')
    text=["css","CSS"]
    for i in ty:
        if i in text:
            return True
    return False
    


if __name__=='__main__':
    example1="fwfwefwefwefwfwfwe\r\nfgadfadsfasf\r\nContent-Type:image/png\r\n"
    example2="fwfwefwefwefwfwfwe\r\nfgadfadsfasf\r\nContent-Type:text/css;charset=xx\r\n"
    r1=Get_Content_Type(example1)
    print r1
    r2=Get_Content_Type(example2)
    print r2
    rr1=Content_Is_Text(r1)
    print rr1
    rr2=Content_Is_Text(r2)
    print rr2   

