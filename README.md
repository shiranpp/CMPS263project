# CMPS263project
jobuiSpider.py----Find all salary history and data of job in the JobUI
LianjiaSpider_0_1.py--Find the District and mini-District information in lianjia
LianjiaSpider_0_2.py--Find all cell information in lianjia
coodCap.py--Capture the coodinate for all cell and minidistirct 

input:
Lianjia(inofmration to buy a apartment )
http://www.jobui.com/salary/beijing/
JOBUI(salary data in beijing)
http://bj.lianjia.com/xiaoqu
data.db--pruches history capture before lianjia implement ip blocker which i get from the a bloger

output:
wage.csv--salary data in beijing
aptpricedb.db--all inofmration to buy a apartment 

requirement:BeautifulSoup,geopy,sqlalchemy(installed by pip)

Instruction:

JOBUI:
1.Run the jobuiSpider.py

input:
JOBUI(salary data in beijing)
http://bj.lianjia.com/xiaoqu
output:
wage.csv--salary data in beijing

LianjiaSpider:
1.Put file LianjiaSpider_0_1.py, LianjiaSpider_0_2.py and dbbase.py in same
folder.
2.Run LianjiaSpider_0_1.py it will capture the District name and id with
beautifulsoup and urlib2. And capture the miniDistrict name and id in each District
page. The data will be store into the aptpricedb.db
3.Run LianjiaSpider_0_1.py. The script can capture the Cell in each
miniDistrict pages. LianJia.com web site will return 404 if an ip address request
too many data stream. My solution is to acquire the data part by part. Once the
output shows ¡®please change poxy and input any value to continue:¡¯. Use the
openVpn or change openVpn¡¯s connection sever to get a new ip address and input
any value in python console to continue.
The cell data will be store into the aptpricedb.db
input:
Lianjia(inofmration to buy a apartment )
http://www.jobui.com/salary/beijing/
Output:
aptpricedb.db--all inofmration to buy a apartment 

Coodinate for each cell:
1.Put coodCap.py,dbbase.py and aptpricedb.db from last section, Run the coodCap.py.
Input:
googlegeoAPI
Output:
aptpricedb.db-- Coordinate for cell



Match the data.db's pruches history to our data format:
1.PCMathcing.py, dbbase.py, aptpricedb.db and data.db in same dir
2.run PCMathcing.py
Input:
data.db--pruches history capture before lianjia implement ip blocker which i get from the a bloger
aptpricedb.db--pruches history for each cell
