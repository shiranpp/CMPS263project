
'''
    LianjiaSpier
    Author:Ryan Shi
    For CMPS263 project
    Find the District and mini-District in lianjia
'''

import re
import urllib2  
import random
import threading
import json
from bs4 import BeautifulSoup
import dbbase
#Data base structure
from dbbase import session,Dist,MDist,Cell,Record
import sys
import time
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr


# Build-in value

#UserAgent
uas=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)" '}
    ]
agent={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
#District
regions=['haidian']
#URL to get cell
curl="http://bj.lianjia.com/xiaoqu"
#URL to get purchase history
phurl="http://bj.lianjia.com/chengjiao/c"


# In[20]:
print 'capture district'
#get District name and id in lianjia
try:
    req = urllib2.Request(curl,headers=uas[random.randint(0,len(uas)-1)])
    source = urllib2.urlopen(req,timeout=10).read()
    text=unicode(source)
    soup = BeautifulSoup(text, "html.parser")
except (urllib2.HTTPError, urllib2.URLError), e:
    print e

dist_list=soup.findAll('div',{'data-role':'ershoufang'})[0].contents[1].find_all('a')
dist=[]
for distitem in dist_list:
    dist.append({'name':distitem.text,'id':str(distitem.get('href').split('/')[2])})
#save District to database
session.execute(Dist.__table__.insert().prefix_with(' OR IGNORE'),dist)
session.commit()

###########

#get minidistrict name and id for each district in lianjia
dist=session.query(Dist).all()
for distitem in dist:
    print 'capture minidistrict in district',distitem.name
    try:
        req = urllib2.Request(curl+'/'+distitem.id+'/',headers=uas[random.randint(0,len(uas)-1)])
        source = urllib2.urlopen(req,timeout=10).read()
        text=unicode(source)
        soup = BeautifulSoup(text, "html.parser")
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
    mdist_list=soup.findAll('div',{'data-role':'ershoufang'})[0].contents[3].find_all('a')
    mdist=[]
    for mdistitem in mdist_list:
        mdist.append({'id':str(mdistitem.get('href').split('/')[2]), 'name':mdistitem.text, 'dist_id':distitem.id,'cood':''})
    session.execute(MDist.__table__.insert().prefix_with(' OR IGNORE'),mdist)
#save minidistrict to database
session.commit()





