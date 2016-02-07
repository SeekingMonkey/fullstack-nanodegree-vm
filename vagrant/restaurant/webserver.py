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
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				rname = restaurant.name
				print rname
				output += "<h1> %s </h1>" % restaurant.name
				output += "<p>Edit</p>"
				output += "<p>Delete</p>"
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
				messagecontent = fields.get('message')
			
			output = ""
			output += "<html><body>"
			output += "<h2>Okay, how about this: </h2>"
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
	
