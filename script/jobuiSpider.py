'''
    Jobui Spider
    Author:  Ziqiang Wang,Ryan Shi
    For CMPS263 project
    Find all salary data of each job title in the JobUI
'''

import re
import urllib2
import random
from bs4 import BeautifulSoup
import csv
import sys

reload(sys)
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr

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
# Target address
joblisturl = 'http://www.jobui.com/salary/beijing/'
joburl = 'http://www.jobui.com'
if __name__ == "__main__":
    # Get job title and href
    try:
        req = urllib2.Request(joblisturl, headers=uas[random.randint(0, len(uas) - 1)])
        source = urllib2.urlopen(req, timeout=10).read()
        text = unicode(source)
        soup = BeautifulSoup(text, "html.parser")
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

    divs = soup.findAll('div', {'class': 'line-job-list j-line-job'})
    data = []
    for div in divs:
        areas = div.findAll('div', class_=['job-list-title', 'j-job-title'])
        jobs_ = div.findAll('div', class_=['job-select-wrapper'])
        i = 0
        while ((i < len(areas)) and (i < len(jobs_))):
            jobs__ = jobs_[i].findAll('a', {'class': 'job-name-title'})
            for job in jobs__:
                data.append({'title': job.text, 'area': areas[i].text, 'href': str(joburl + job.get('href'))})
            i += 1

    # Output all jobs and address
    header = ['title', 'href', 'area']
    with open('jobs.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
    # Get salary history and data for different level of employpee
    jobs = data
    data = []
    bad = []
    for job in jobs:
        try:
            print 'Capture', job['title']
            try:
                req = urllib2.Request(job['href'], headers=uas[random.randint(0, len(uas) - 1)])
                source = urllib2.urlopen(req, timeout=10).read()
                text = unicode(source)
                soup = BeautifulSoup(text, "html.parser")
            except (urllib2.HTTPError, urllib2.URLError), e:
                print e

            scripts = soup.findAll('script', {'type': 'text/javascript'})

            for script in scripts:
                pattern = re.compile(u'[\u9a8c]\\\',data: \[(.*?)\]')
                if (re.findall(pattern, script.text)):
                    list = re.findall(pattern, script.text)[0].split(',')
                    for i in range(len(list)):
                        job['exp_' + str(i)] = int(list[i])
                pattern = re.compile(u'[\u8d44]\\\',data: \[(.*?)\]')
                if (re.findall(pattern, script.text)):
                    list = re.findall(pattern, script.text)[0].split(',')
                    for i in range(len(list)):
                        job[str(2016 - len(list) + i + 1)] = int(list[i])
            data.append(job)
        except e:
            bad.append(job)

    # Output the the webpage that unable to captured to recaptured or pass if pages is 404 or corrupts
    header = ['title', 'href', 'area']
    with open('bad.csv', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect='excel')
        writer.writeheader()
        for i in bad:
            writer.writerow(i)

    # Output the salary history to the scv file
    # title: job title
    # area: job area
    # exp_i: salary of i*2 year of employment of employee
    # 2009-2016: salary history
    header = ['title', 'href', 'area', 'exp_0', 'exp_1', 'exp_2', 'exp_3', 'exp_4', 'exp_5', '2009', '2010', '2011',
              '2012', '2013', '2014', '2015', '2016']
    with open('wage.csv', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect='excel')
        writer.writeheader()
        for i in data:
            writer.writerow(i)
