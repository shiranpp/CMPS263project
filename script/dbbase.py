
# coding: utf-8



from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
Base = declarative_base()
Base_ = declarative_base()
engine=create_engine("sqlite:///aptpricedb.db")
engine_=create_engine("sqlite:///data.db")


#table for each District
class Dist(Base):
    __tablename__ = 'dist'

    id = Column(String(32), primary_key=True)
    name = Column(String(64))
    
    def __repr__(self):
        return "<Dist(%r, %r)>" % (
                self.id, self.name
            )
#table for each area in District
class MDist(Base):
    __tablename__ = 'mdist'

    id = Column(String(32), primary_key=True)
    name = Column(String(64))
    dist_id = Column(String(32),ForeignKey('dist.id'))
    cood=Column(String(64))
    dist=relationship('Dist')
    def __repr__(self):
        return "<MiniDist(%r, %r, %r, %r)>" % (
                self.id, self.name, self.cood, self.dist.name
            )
#table for each negiboor
class Cell(Base):
    __tablename__ = 'cell'

    id = Column(String(32), primary_key=True)
    name = Column(String(64))
    cood=Column(String(64))
    avg_price=Column(Integer)
    onsale_num=Column(Integer)
    traffic=Column(String(64))
    mdist_id = Column(String(32),ForeignKey('mdist.id'))
    mdist=relationship('MDist')
    
    def __repr__(self):
        return "<Cell(%r, %r, %r, %r, %r, %r, %r, %r)>" % (
                self.id, self.name, self.cood, self.avg_price, self.onsale_num, self.traffic, self.mdist.name, self.mdist.dist.name
            )
#table for each pruches record
class Record(Base):
    __tablename__ = 'record'

    href = Column(String, primary_key=True)
    sign_time =Column(DateTime)
    area =Column(Integer)
    unit_price = Column(Integer)
    total_price = Column(Integer)
    style = Column(String)
    cell_id = Column(String,ForeignKey('cell.id'))
    cell=relationship('Cell')
    
    def __repr__(self):
        return "<MiniDist(%r, %r, %r, %r, %r, %r, %r)>" % (
                self.nre, self.sign_time, self.area, self.unit_price, self.total_price, self.style, self.cell.name
            )


class CJ(Base_):
    __tablename__ = 'chengjiao'

    href = Column(String, primary_key=True)
    name = Column(String)
    style = Column(String)
    area = Column(String)
    orientation = Column(String)
    floor = Column(String)
    year = Column(String)
    sign_time = Column(String)
    unit_price = Column(String)
    total_price = Column(String)
    fangchan_class = Column(String)
    school = Column(String)
    subway = Column(String)

    def __repr__(self):
        return "<Dist(%r, %r, %r, %r, %r, %r, %r)>" % (
            self.href, self.name, self.style, self.area, self.sign_time, self.unit_price, self.total_price
        )

Base.metadata.create_all(engine)
Base_.metadata.create_all(engine_)
Session = sessionmaker(bind=engine)
Session_ = sessionmaker(bind=engine_)
session = Session()
session_ = Session_()



