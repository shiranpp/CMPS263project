

'''
    Pruchers Record Matching
    Author:Ryan Shi
    For CMPS263 project
    Match the data.db's pruches history to our data format
'''
import re
import time
from datetime import datetime, date, time
import random
import threading
import json
import dbbase
#Data base structure
from dbbase import session,session_,Dist,MDist,Cell,Record,CJ
import sys
import time
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr

pattern = re.compile(u'([0-9]+)')

cells=session.query(Cell).all()

i=0
n=len(cells)

for cell in cells:
    i+=1
    print i,'/',n
    prs=session_.query(CJ).filter(CJ.name==cell.name).all()
    prs_=[]
    for pr in prs:
        if (len(pr.sign_time)>7):
            time=datetime.strptime(pr.sign_time, '%Y.%m.%d')
        else:
            time=datetime.strptime(pr.sign_time, '%Y.%m')
        if((re.findall(pattern,pr.total_price))and(re.findall(pattern,pr.unit_price))):
            prs_.append({'href':pr.href,'sign_time':time                        ,'area':int(re.findall(pattern,pr.area)[0]),'unit_price':int(re.findall(pattern,pr.unit_price)[0])                       ,'total_price':int(re.findall(pattern,pr.total_price)[0])*10000,'style':pr.style,'cell_id':cell.id})
    session.execute(Record.__table__.insert().prefix_with(' OR IGNORE'),prs_)
    session.commit()






