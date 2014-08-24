#coding: UTF-8
import Http
import os

def escape(text):

    text=text.replace('&','&#38;')
    text=text.replace(' ','&#160;')
    text=text.replace('<','&#60;')
    text=text.replace('>','&#62;')
    text=text.replace('"','&#34;')
    text=text.replace('\'','&#39;')
    return text


#x为XSS向量，a为请求报文，req为响应报文,info为漏洞类型说明
def report_pro(x,a,req,info):
    print "Discover XSS,Now write in report"
    if os.path.exists(r'.\Report.html'):  
        report=open(r'.\Report.html','a')
    else:
        report=open(r'.\Report.html','a') 
        report.write("<meta charset=\"UTF-8\"/>")
    report.write("<hr>")
    report.write("发现疑似XSS,输出点所在区域类型为"+info+",详情如下:<br>")
    report.write("输出点位置:")
    report.write(Http.get_target(a))
    report.write("<br>有效的XSS攻击向量为：")
    x=escape(x)
    report.write(x+"<br>")
    report.close()
