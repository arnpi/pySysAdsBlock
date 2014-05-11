#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import settings

body = "ADS Blocked by<br>" + settings.PROGRAM_NAME + """
<script  language=javascript>
window.onload=window.close();
</script>
"""
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write( body)
		return

        def do_QUIT (self):
            """send 200 OK response, and set server.stop to True"""
            self.send_response(200)
            self.end_headers()
	    self.server.socket.close()
            # self.server.stop = True


def run():
    try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer((settings.IP_REDIRECTION, settings.PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , settings.PORT_NUMBER, " and IP: " + settings.IP_REDIRECTION
	print "To kill, press ^C"
	# recuperation du pid du script pour pouvoir etre kill
	print os.getpid()
	#Wait forever for incoming htto requests
	server.serve_forever()

    except (Exception, KeyboardInterrupt):
	print '^C received, shutting down the web server'
	server.socket.close()
def stop():
    server.socket.close()
