# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import urllib
import os
import re
import traceback
import shutil
firurl = "http://127.0.0.1:5000/index.html"
weburl = r"http://127.0.0.1:5000"
learned = []
target = 'build'
pattern = r'(.*\/).*\.(css|js|html)'
def reqUrlRec(url):
    try:
        if not url.startswith(r'http://'):
        #拼接url
            tempurl = weburl+'/'+url
        else:
            tempurl = url
        if not tempurl.startswith(weburl):
            #非本站内容，不爬去
            return
        #获取目录
        print(tempurl)
        tempurl = os.path.realpath(urlparse(urllib.parse.unquote(tempurl)).path)
        if tempurl in learned:
            return
        dirs = re.match(pattern, tempurl).group(1)
        print(dirs)
        if not os.path.exists(target + dirs) and dirs.endswith('/'):
            os.makedirs(target + dirs)
        page = requests.get(weburl + tempurl).content
        fp = open(target + tempurl, 'wb')
        fp.write(page)
        fp.close()
        learned.append(tempurl)
        soup = BeautifulSoup(page, 'html.parser')
        for a in soup.find_all('a'):
            if a['href'] not in learned:
                reqUrlRec(a['href'])
    except Exception:
        print(traceback.print_exc())
        pass

try:
    os.makedirs('build')
except OSError:
    pass
reqUrlRec(firurl)
os.system('cp -rf cblog/static build/')

with open('build/404.html', 'wb') as fp:
    fp.write(requests.get(weburl+'/idex').content)
