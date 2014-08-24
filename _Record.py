#coding: UTF-8
import ContentType
import re
import r_text
from bs4 import BeautifulSoup
import Http


#接收Http请求报文，响应报文，以及标记字符串作为参数；标记字符串被写死
#检查该报文是否包含数据输出点，并根据输出点的位置进行分类
#.\_Record\html  输出点直接在html中
#.\_Record\in_html  输出点直接在html的某种标签中
#.\_Record\html_js  输出点在html的非js标签的js中
#.\_Record\js  输出点直接在js中
#.\_Record\json  输出点直接在json中


    

def record_pro(request,response):
    #html="Hello"
    #print request
    html=Http.get_response(request)  #取得响应主体，同时进行报文重放测试
    #print "Hello:\n"+html
    Is_Json=ContentType.Content_Is_Json(ContentType.Get_Content_Type(response))
    Is_Html=ContentType.Content_Is_Html(ContentType.Get_Content_Type(response))
    Is_js=ContentType.Content_Is_js(ContentType.Get_Content_Type(response))
    Is_css=ContentType.Content_Is_css(ContentType.Get_Content_Type(response))
##返回报文为json
    if Is_Json:  
        re=r'<chiruomorg>'
        if r_text.In_Text(re,response):
            r_text.write_dbm(request," ",r'.\_Record\json',"c")
##返回报文为html
    elif Is_Html:
        #print "in is_html"
        soup=BeautifulSoup(html)
        js=soup.find_all('script') #以列表的方式返回所有js标签
        #print js
    ##输出点在html的js标签中        
        sign2=r'chiruomorg'  #
        for i in js:
            #print i+"\n"
            i2=i.string
            if r_text.In_Text(r'chiruomorg',i2):
                r_text.write_dbm(request," ",r'.\_Record\js',"c")
                #print "in js1"
                break
        #html2=soup.script.decompose()
    ##输出点在html的非js标签的js中（各种on的情况等）            
        sign3=r'on[^=]*=[^>]*chiruomorg[^>]*'    
        sign4=r'var[^=]*=[^;]*chiruomorg[^;]*;'
        if r_text.In_Text(sign3,html) or r_text.In_Text(sign4,html):
            #print "in html_js"
            r_text.write_dbm(request," ",r'.\_Record\html_js',"c")
    ##输出点在html标签<>之外
        sign5=r'<chiruomorg>'
        if r_text.In_Text(sign5,html):
            r_text.write_dbm(request," ",r'.\_Record\html',"c")
            #print "in html1"
    ##输出点在html标签<>之中,某属性
        sign6=r'<[^>]*=\s*[^>]*chiruomorg[^>]*>'  
        if r_text.In_Text(sign6,html):
                    r_text.write_dbm(request," ",r'.\_Record\html_in',"c")
                    #print "in html4"
##返回报文为纯JS
    elif Is_js:
        #soup=BeautifulSoup(html)
        sign2=r'chiruomorg'
        #js=soup.find_all('script') #以列表的方式返回所有js标签
        #for i in js:
        #i2=i.string
        if r_text.In_Text(sign2,html):
            r_text.write_dbm(request," ",r'.\_Record\js',"c")
            #print "in js2"
##返回报文为纯css
    elif Is_css:
        pass
        sign2=r'chiruomorg'
        if r_text.In_Text(sign2,html):
            r_text.write_dbm(request," ",r'.\_Record\css',"c")
            #print "in js2"
##其他情况
    else:
        re=r'<chiruomorg>'
        if r_text.In_Text(re,response):
            r_text.write_dbm(request," ",r'.\_Record\html',"c")
            #print "in html2"
                    
                   
                
        
                
        
