

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#create engine (connection to db)
engine = create_engine('sqlite://restaurantmenu.db')
# Bind engine to Base class
Base.metadata.bind = engine
#bucket to store instructions to send to db
DBSession = sessionmaker(bind = engine)
# create instance of session
session = DBSession()
#create an instance of the restaurant class, this will create a row in the Restaurant table
myFirstRestaurant = Restaurant(name = "Pizza Palace")
#add command to session
session.add(myFirstRestaurant)
#send instructions in session to db
session.commit()
#query db to see if new row was created
session.query(Restaurant).all()
#Add row to MenuItem table
cheesepizza = MenuItem(name = "Cheese Pizza",
				description = "Made with all natural ingredients and fresh mozzarella",
				course = "Entree",
				price = "$8.99",
				restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
#query db to see if new menu item shows update
session.query(MenuItem).all()
#assign a variable to store a query for the first row of Restaurant
firstresult = session.query(Restaurant).first()
#Columns are now referenceable as methods
#firstresult.name will output 'Pizza Palance'

#When the db contains many items, you can query for
#specific data by creating a variable to hold results
items = session.query(MenuItem).all()
for item in items:
	print item.name

#...update item.......................................
#query for items
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
#print out results of query
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"
# get veggieBurger.id from correct entry (ex. id==8)
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 8).one()
#update price, add to session and commit
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

#...update many items..................................
for veggieBurger in veggieBurgers:
	if veggieBurger.price != '$2.99':
		veggieBurger.price = '$2.99'
		session.add(veggieBurger)
		session.commit()
		
#...delete an item......................................
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()


