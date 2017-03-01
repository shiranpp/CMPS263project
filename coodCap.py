
'''
    Coordinate Capturer
    Author:Ryan Shi
    For CMPS263 project
    Capture the coodinate for all cell and minidistirct 
'''

import random
import threading
import json
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
import geopy
from geopy.geocoders import GoogleV3


google_api_key=''#input your google api key here

geolocator = GoogleV3(api_key=google_api_key, domain='maps.googleapis.com', scheme='https', client_id=None, secret_key=None, timeout=10, proxies=None)


#Use the google api to capture the coodinate for all minidistirst
mdlist=session.query(MDist).all()
for md in mdlist:
    if (md.cood==''):
        location = geolocator.geocode(md.dist.name+'  '+md.name+u' 北京')
        if location is None:
            location = geolocator.geocode(md.name+u' 北京')
        if location is not None:
            md.cood='['+str(location.latitude)+','+ str(location.longitude)+']'
            print 'captured coodinate at'+md.name+':'+location.address
        else:
            print 'no coodinate for'+md.name

session.commit()
#Use the google api to capture the coodinate for all cell
cells=session.query(Cell).filter(Cell.cood==None).all()
n=len(cells)
i=0
for cell in cells:
    i+=1;
    if (cell.cood=='' or cell.cood==None ):
        location = geolocator.geocode(cell.name+'  '+cell.mdist.dist.name+u' 北京')
        if location is None:
            location = geolocator.geocode(cell.name+u' 北京')
        if location is not None:
            cell.cood='['+str(location.latitude)+','+ str(location.longitude)+']'
            print i,'/',n,'captured coodinate at'+cell.name+':'+location.address
        else:
            cell.cood='g'
            print i,'/',n,'no coodinate for'+cell.name
session.commit()



