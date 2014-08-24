#coding: UTF-8
import os





#删除_Record目录下的文件
if os.path.exists(r'.\_Record\html'):
    os.remove(r'.\_Record\html')
if os.path.exists(r'.\_Record\html_js'):
    os.remove(r'.\_Record\html_js')
if os.path.exists(r'.\_Record\js'):
    os.remove(r'.\_Record\js')
if os.path.exists(r'.\_Record\json'):
    os.remove(r'.\_Record\json')
if os.path.exists(r'.\_Record\in_html'):
    os.remove(r'.\_Record\in_html')


if os.path.exists(r'.\_Record\html.txt'):
    os.remove(r'.\_Record\html.txt')
if os.path.exists(r'.\_Record\js.txt'):
    os.remove(r'.\_Record\js.txt')


if os.path.exists(r'.\Screq'):
    os.remove(r'.\Screq')
if os.path.exists(r'.\Screq.txt'):
    os.remove(r'.\Screq.txt')


if os.path.exists(r'.\Record.txt'):
    os.remove(r'.\Record.txt')

if os.path.exists(r'.\Report.html'):
    os.remove(r'.\Report.html')



