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
			self.send_header('Content-type', 'text/html')
			self.end_headers()
				
			output = ""
			output += "<html><body>"
			output += "<h3>self.path =: %s</h3>" % self.path
			if self.path.endswith("new"):
				output += "<h1>New!!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='new'>"
				output += "<h2>Name of new restaurant?</h2>"
				output += "<input name='name' type='text' >" #the input text box, newName is a text variable sent to do_POST method
				output += "<input type='submit' value='Create'></form>" #the button
			elif self.path.endswith("edit"):
				rId = self.path[1:self.path.find('/edit')]
				#output += "rId: %s" % rId
				restaurant = session.query(Restaurant).filter_by(id = rId).first()
				output += "<h1>Edit!!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='%s/confirm'>" % self.path
				output += "<h2>What would you like to rename %s to?</h2>" % restaurant.name
				output += "<input name='newName' type='text' >" #the input text box, newName is a text variable sent to do_POST method
				output += "<input type='submit' value='Edit'></form>" #the button
			elif self.path.endswith("delete"):
				output += "<h1>Delete!!</h1>"
			else:
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					print restaurant.name
					print restaurant.id
					output += "<h1> %s </h1>" % restaurant.name
					output += '<p><a href= "http://localhost:8080/%s/edit">Edit</a></p>' % restaurant.id
					output += '<p><a href= "http://localhost:8080/%s/delete">Delete</a></p>' % restaurant.id
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
				
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)
	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newName')
			
			output = ""
			output += "<html><body>"
			if self.path.endswith("edit/confirm"):
				output += "<h1>EDIT PAGE!<h2>"
				output += "<h2>Are you sure you want to rename %s to %s ?" % messagecontent
			
			else:
				output += "<h2>I'm sorry, can you repeat that?</h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += """<form method='POST' enctype='multipart/form-data' 
						action='/hello'><h2>What would you like me to say?</h2>
						<input name='message' type='text' ><input type='submit'
						value='Submit'></form>"""
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
			
		except:
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
	
