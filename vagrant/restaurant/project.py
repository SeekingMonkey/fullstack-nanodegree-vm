from flask import Flask, render_template, request, redirect, url_for, flash
#create an instance of Flask with name of this application as the argument
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def displayRestaurants():
	restaurants = session.query(Restaurant).all()
	print "restaurant.all() queried..."
	for r in restaurants:
		print r.name
	return render_template('restaurants.html', restaurants=restaurants)
	
# include variables within urls by using the following formula...
# path/<type: variable_name>/path/
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	print "restaurant_id : %s" % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
	print "restaurant.name : %s" % restaurant.name
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	print "MenuItem  query complete..."
	output = ''
	output += "<h2>%s</h2>" % restaurant.name
	return render_template('menu.html', restaurant=restaurant,items=items)
	
# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		print "...entering if block: if request.method == 'POST'"
		newItem = MenuItem(name = request.form['name'], price = request.form['price'], description = request.form['description'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New menu item created!!')
		print "...redirecting to : %s" % url_for('restaurantMenu', restaurant_id=restaurant_id)
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template(
			'newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	print "edited item successdully queried..."
	if request.method == 'POST':
		editedItem.name = request.form['name']
		editedItem.description = request.form['description']
		editedItem.price = request.form['price']
		session.add(editedItem)
		session.commit()
		flash('Item has been edited!!')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		print "...rendering template with values : %s, %s, %s" % (restaurant_id, menu_id, editedItem.name)
		return render_template(
			'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	try:
		itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	except:
			return "Something went wrong with your query.  :("
			
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('Item has been deleted!!')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))	
	else:
		return render_template(
			'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemToDelete)
	
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True	
	app.run(host = '0.0.0.0', port = 5000)