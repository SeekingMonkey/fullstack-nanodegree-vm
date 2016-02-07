import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

#Classes........................
"""
syntax: __tablename__ = '[SOME TABLE]'
syntax: columnName = Column(attributes1,...,attributesN)
Attribute ex.
Sting(250)
Integer
relationship(Class)
nullable = False
primary_key = True
ForeignKey('some_table_id')
"""

class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	
class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)
	



#Ending Boiler plate.............
engine = create_engine('sqlite:///restaurantmenu.db')
#engine = create_engine('postgresql://ec2-user@10.0.0.199:5432/restaurantmenu.db')
Base.metadata.create_all(engine)

