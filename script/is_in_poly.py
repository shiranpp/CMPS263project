
'''
    Job Salary analysis
    Author: Ziqiang Wang
    For CMPS263 project
    Analysis the Salary data to show total saving.
'''
import json
import matplotlib.path as mplPath
import numpy as np
import re
from dbbase import session,Dist,MDist,Cell,Record
import json
import os
def hashlist(l):
    return str(l[0])+str(l[1])

if __name__ == "__main__":
    json_data = open('beijing.json').read()
    data = json.loads(json_data)
    cells=session.query(Cell).filter(Cell.avg_price>1000).all()

    cood=[]
    for cell in cells:
        se=re.findall("[0-9.]+",cell.cood)
        if (se):
            cood.append([round(float(se[1]),3),round(float(se[0]),3)])
        else:
            cood.append([0,0])


    n=len(data['features'])


    polys=[]
    for i in range(0,n):
        poly=[]
        cdatas=data['features'][i]['geometry']['coordinates']
        if (data['features'][i]['properties']['childNum']<2):
            poly.append(mplPath.Path(np.array(cdatas[0])))
        else:
            for cdata in cdatas:
                poly.append(mplPath.Path(np.array(cdata[0])))
        polys.append(poly)


    dists=[[] for i in range(0,n)]
    dicts=[{} for i in range(0,n)]
    for i in range(0,len(cells)):
        loc=cood[i]
        for j in reversed(range(0,n)):
            for poly in polys[j]:
                if (poly.contains_point(loc)):
                    if(hashlist(loc) in dicts[j]):
                        dicts[j][hashlist(loc)]["name"].append(cells[i].name)
                        dicts[j][hashlist(loc)]["price"].append(cells[i].avg_price)
                    else:
                        dicts[j][hashlist(loc)]={"cood":loc}
                        dicts[j][hashlist(loc)]["name"]=[cells[i].name]
                        dicts[j][hashlist(loc)]["price"]=[cells[i].avg_price]
                    break

    for i in range(0,n):
        s=0
        num=0
        cell_=[]
        for key, value in dicts[i].iteritems():
            s+=sum(value["price"])
            num+=len(value["price"])
            cell_.append({'coordinates':value["cood"],'price':value["price"],'name':value["name"],'avg_price':sum(value["price"])/len(value["price"])})
        data['features'][i]['properties']['avg_price']=s/num
        data['features'][i]['properties']['cells']=cell_



    if(os.path.exists('beijingdata.js')):
        os.remove('beijingdata.js')



    x="var geodata = "+json.dumps(data)+";"
    with open('beijingdata.js', 'w') as outfile:
        outfile.write(x)





