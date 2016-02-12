from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		#create engine (connection to db)
		engine = create_engine('sqlite:///restaurantmenu.db')
		# Bind engine to Base class
		Base.metadata.bind = engine
		#bucket to store instructions to send to db
		DBSession = sessionmaker(bind = engine)
		# create instance of session
		session = DBSession()
		try:
			self.send_response(200)
			self.send_header('Content-type',   'text/html')
			self.end_headers()
				
			output = ""
			output += "<html><body>"
			output += "<h3>self.path =: %s</h3>" % self.path
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				output += "<p><h2><a href='%s/new'>Create a new restaurant</a></h2></p>" % self.path
				for restaurant in restaurants:
					#print "loop"
					#print restaurant.name
					#print restaurant.id
					output += "<h1> %s </h1>" % restaurant.name
					output += '<p><a href= "http://localhost:8080%s/%s/edit">Edit</a></p>' % (self.path,restaurant.id)
					output += '<p><a href= "http://localhost:8080%s/%s/delete">Delete</a></p>' % (self.path,restaurant.id)
				print "....listing loop complete...................."
			elif self.path.endswith("/new"):
				output += "<h1>New!!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='%s/confirm'>" % self.path
				output += "<h2>Name of new restaurant?</h2>"
				output += "<input name='newName' type='text' value='New Restaurant Name'>" #the input text box, newName is a text variable sent to do_POST method
				output += "<input type='submit' value='Create'></form>" #the button
			elif self.path.endswith("/edit"):
				print ".../edit triggered...%s............." % self.path
				#print self.path
				#print self.path.find('ts/')+3
				rId = self.path[self.path.find('ts/')+3:self.path.find('/edit')]
				#rId = self.path.split("/")[2]
				#output += "rId: %s" % rId
				restaurant = session.query(Restaurant).filter_by(id = rId).first()
				output += "<h1>Edit!!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='%s/confirm'>" % self.path
				output += "<h2>What would you like to rename %s to?</h2>" % restaurant.name
				output += "<input name='reName' type='text' value='%s'>" % restaurant.name #the input text box, newName is a text variable sent to do_POST method
				output += "<input type='hidden' name='oldName' value='%s'>" % restaurant.name
				output += "<input type='submit' value='Edit'></form>" #the button
			elif self.path.endswith("/delete"):
				print "........../delete triggered...%s............." % self.path
				rId = self.path[self.path.find('ts/')+3:self.path.find('/delete')]
				#output += "rId: %s" % rId
				restaurant = session.query(Restaurant).filter_by(id = rId).first()
				output += "<h1>DELETE CONFIRMATION PAGE!</h1>"
				#print "::: %s" % output
				output += "<h2>Are you sure you want to delete %s ?</h2>" % restaurant.name
				#print "::: %s" % output	
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete/confirmed'>" %rId
				output += '<input type="hidden" name="newName" value="%s">' % restaurant.name
				output += "<input type='submit' value='Confirm'></form>" #the button
				print "..........::: %s" % output
			else:
				output += "<h3>Nothing was added to output!</h3>"
			output += "</body></html>"
			self.wfile.write(output)
			print ".do_GET complete............."
			return
				
		except IOError:
			print ".do_POST failed................"
			self.send_error(404, "File Not Found %s" % self.path)
	def do_POST(self):
		#create engine (connection to db)
		engine = create_engine('sqlite:///restaurantmenu.db')
		# Bind engine to Base class
		Base.metadata.bind = engine
		#bucket to store instructions to send to db
		DBSession = sessionmaker(bind = engine)
		# create instance of session
		session = DBSession()
		print ".do_POST tried......................"
		try:
			print "....inside do_POST try block......................"
			self.send_response(301)
			self.send_header('Content-type',   'text/html')
			#self.send_header('Location', '/restaurants')
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				
			output = ""
			output += "<html><body>"
			if self.path.endswith("/new/confirm"):
				print "..........new/confirm triggered...%s............." % self.path
				newName = fields.get('newName')
				print "..........newName : %s" % newName
				output += "<h1>CREATE CONFIRMATION PAGE!</h1>"
				#print "::: %s" % output
				output += "<h2>Are you sure you want to create a new restauant named %s ?</h2>" % newName[0]
				#print "::: %s" % output	
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new/confirmed'>"
				output += '<input type="hidden" name="newName" value="%s">' % newName[0]
				output += "<input type='submit' value='Confirm'></form>" #the button
				print "..........::: %s" % output
			elif self.path.endswith("/new/confirmed"):
				print "..........new/confirmed triggered...%s............." % self.path
				newName = fields.get('newName')
				print "..........newName : %s" % newName
			#...send command to db to create new record
				#update name, add to session and commit
				#create an instance of the restaurant class, this will create a row in the Restaurant table
				newRestaurant = Restaurant(name = newName[0])
				session.add(newRestaurant)
				session.commit()
				print "..........new restaurant added to db: %s.............." % newName[0]
				output += "<h2>%s has been added to the database.</h2>" % newName[0]
				output += "<br><p><a href='/restaurants'>Back to restaurants</a></p>"
			elif self.path.endswith("/edit/confirm"):
				print "..........edit/confirm triggered...%s............." % self.path
				oldName = fields.get('oldName')
				print "..........oldName : %s" % oldName
				reName = fields.get('reName')
				print "..........reName : %s" % reName
				rId = self.path[self.path.find('ts/')+3:self.path.find('/edit')]
				print "..........rId : %s" % rId
				output += "<h1>EDIT CONFIRMATION PAGE!</h1>"
				#print "::: %s" % output
				output += "<h2>Are you sure you want to rename %s to %s ?</h2>" % (oldName[0],reName[0])
				#print "::: %s" % output	
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit/confirmed'>" %rId
				output += '<input type="hidden" name="reName" value="%s">' % reName[0]
				output += "<input type='submit' value='Confirm'></form>" #the button
				print "..........::: %s" % output
			elif self.path.endswith("edit/confirmed"):
				print "..........edit/confirmed triggered...%s............." % self.path
				reName = fields.get('reName')
				print "..........reName : %s" % reName
				rId = self.path[self.path.find('ts/')+3:self.path.find('/edit')]
				print "..........rId : %s" % rId
			#...send command to db to update name
				# get restaurant object by id
				restaurant = session.query(Restaurant).filter_by(id = rId).one()
				oldName = restaurant.name
				print "..........oldName : %s" % oldName
				#update name, add to session and commit
				restaurant.name = reName[0]
				session.add(restaurant)
				session.commit()
				print "..........restaurant name updated to %s.............." % reName[0]
				output += "<h2>Then name of %s has been changed to %s </h2>" % (oldName,reName[0])
				output += "<br><p><a href='/restaurants'>Back to restaurants</a></p>"
			elif self.path.endswith("/delete/confirmed"):
				print "........../delete/confirmed triggered...%s............." % self.path
				rId = self.path[self.path.find('ts/')+3:self.path.find('/delete')]
				#output += "rId: %s" % rId
				restaurant = session.query(Restaurant).filter_by(id = rId).first()
				delName = restaurant.name
				print "delName : %s" % delName
				output += "<h1>DELETE CONFIRMATION PAGE!</h1>"
				#print "::: %s" % output
				#delete row, add to session and commit
				session.delete(restaurant)
				session.commit()
				print ".........deleted %s from database.............." % delName
				output += "<h2>%s has been deleted from the database</h2>" % delName
				output += "<br><p><a href='/restaurants'>Back to restaurants</a></p>"
			else:
				print "...else triggered...%s............." % self.path
				output += "<h2>I'm sorry, can you repeat that?</h2>"
				#output += "<h1> %s </h1>" % reName[0]
				#output += """<form method='POST' enctype='multipart/form-data' 
				#		action='/hello'><h2>What would you like me to say?</h2>
				#		<input name='message' type='text' ><input type='submit'
				#		value='Submit'></form>"""
			output += "</body></html>"
			self.wfile.write(output)
			print output
			print ".do_POST complete............."
			return
			
		except:
			print ".do_POST failed................"
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
		
		
		
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()
		
if __name__ == '__main__':
	main()
	
