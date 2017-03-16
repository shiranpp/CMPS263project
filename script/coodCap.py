
# coding: utf-8

'''
    Coordinate Capturer
    Author:Ryan Shi
    For CMPS263 project
    Capture the coodinate for all cell
'''

import threading
#Data base structure
from dbbase import session,Dist,MDist,Cell,Record,engine
import sys
import time
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8")
sys.stdout = default_stdout
sys.stderr = default_stderr
import geopy
from geopy.geocoders import GoogleV3,Baidu

#google api key here need at least 6
google_api_key=[""]
baidu_api_key=""#baidu API Key
bgeolocator=[Baidu(baidu_api_key)]
geolocators=[]
for key in google_api_key:
    geolocators.append(GoogleV3(api_key=key, domain='maps.googleapis.com', scheme='https', client_id=None, secret_key=None, timeout=10, proxies=None))

# Thread to capture the coordinate with bgeolocator and sqlalchemy
class capThread (threading.Thread):
    def __init__(self, session, cells,geolocators):
        threading.Thread.__init__(self)
        self.session = session
        self.cells = cells
        self.geolocators = geolocators
        self.n=len(self.cells)
    def run(self):
        self.n=len(self.cells)
        self.i=0
        for geo in geolocators:
                while (self.i < self.n):
                    cell=cells[i]
                    self.i+=1;
                    location = geo.geocode(cell.name+'  '+cell.mdist.dist.name+u' 北京')
                    if location is None:
                        location = geo.geocode(cell.name+u' 北京')
                    if location is not None:
                        cell.cood='['+str(location.latitude)+','+ str(location.longitude)+']'
                        print self.i,'/',self.n,'captured coodinate at'+cell.name+':'+location.address
                    else:
                        cell.cood='g'
                        print self.i,'/',self.n,'no coodinate for'+cell.name

if __name__ == "__main__":
    #Use the google api to capture the coodinate for all cell
    cells=session.query(Cell).filter(Cell.cood==None).all()
    print "capture coodinate in google"
    data=[]
    n=len(cells)/2
    for i in range(0,2):
        data.append(cells[i*n:min(i*n+n,len(cells))])
    thread1 = capThread(session, data[0], geolocators[0:3])
    thread1.start()
    thread2 = capThread(session, data[1], geolocators[3:6])
    thread2.start()
    while((thread1.isAlive()) or (thread2.isAlive())):
        time.sleep(60)
    session.commit()
    print "capture coodinate in baidu"
    #Use the baidu api to capture the coodinate for all cell
    cells=session.query(Cell).filter(Cell.cood=='g').all()
    thread1 = capThread(session, cells, bgeolocator)
    thread1.start()
    while((thread1.isAlive())):
        time.sleep(60)
    session.commit()

