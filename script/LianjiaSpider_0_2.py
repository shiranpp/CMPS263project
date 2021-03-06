'''
    LianjiaSpier-Neighborhood Capturer
    Author:Ryan Shi
    For CMPS263 project
    Find the All Neighborhood in Lianjia
'''

import urllib2
import random
import json
from bs4 import BeautifulSoup
# Data base structure
from dbbase import session, Dist, MDist, Cell, Record
import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr

# Build-in value

# UserAgent
uas = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
       {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'}, {
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
       {
           'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
       {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}, {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
       {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
       {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'},
       {
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)" '}
       ]
agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
# District
regions = ['haidian']
# URL to get cell
curl = "http://bj.lianjia.com/xiaoqu"
# URL to get purchase history
phurl = "http://bj.lianjia.com/chengjiao/c"

if __name__ == "__main__":
    # Seprate minidistrict to several part which i can rerun rest of part after i change my ip address
    mdlist = session.query(MDist).all()
    start = 0
    # aquire the data for each cell in minidistrict whicn include price traffic numer of apts on sale
    while (start < len(mdlist)):
        try:
            for dnum in range(start, len(mdlist)):
                # get cell information for each minidistrict
                # get total pages number
                mdlistitem = mdlist[dnum]
                start = dnum
                try:
                    req = urllib2.Request(curl + '/' + mdlistitem.id + '/',
                                          headers=uas[random.randint(0, len(uas) - 1)])
                    source = urllib2.urlopen(req, timeout=10).read()
                    text = unicode(source)
                    soup = BeautifulSoup(text, "html.parser")
                except (urllib2.HTTPError, urllib2.URLError), e:
                    print e
                pages = int(
                    json.loads(str(soup.find("div", {"class": "page-box house-lst-page-box"}).get('page-data')))[
                        u'totalPage'])

                # get cell information
                for i in range(1, pages + 1):
                    print 'capture cell ', mdlistitem.name, 'at page ', i, ':', dnum
                    # time.sleep(random.randint(0,2))
                    try:
                        req = urllib2.Request(curl + '/' + mdlistitem.id + '/pg' + str(i) + '/',
                                              headers=uas[random.randint(0, len(uas) - 1)])
                        source = urllib2.urlopen(req, timeout=10).read()
                        text = unicode(source)
                        soup = BeautifulSoup(text, "html.parser")
                    except (urllib2.HTTPError, urllib2.URLError), e:
                        print e
                    nebs = soup.find_all("li", {"class": "clear xiaoquListItem"})
                    cell = []
                    for neb in nebs:
                        uid = neb.find("div", {"class": "title"}).find("a").get('href').split('/')[4]
                        name = neb.find("div", {"class": "title"}).find("a").text
                        try:
                            price = int(neb.find("div", {"class": "totalPrice"}).find("span").text)
                        except:
                            price = 0
                        try:
                            num = int(neb.find("a", {"class": "totalSellCount"}).find("span").text)
                        except:
                            num = 0
                        try:
                            traffic = nebs[0].find("div", {"class": "tagList"}).find('span').text
                        except:
                            traffic = ''
                        cell.append({'id': uid, 'name': name, 'avg_price': price, 'onsale_num': num, 'traffic': traffic,
                                     'mdist_id': mdlistitem.id})
                        session.execute(Cell.__table__.insert().prefix_with(' OR IGNORE'), cell)
                        # write back to data base
                    session.commit()
        except:
            con = input('please change poxy and input any value to continue: ')
