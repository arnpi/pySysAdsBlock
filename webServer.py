#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sudo ifconfig eth0:1 127.0.0.2 netmask 255.255.255.0 up
sudo ifconfig eth0:1 down
# sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 127.0.0.2:800
#sudo iptables -t nat -A PREROUTING -p tcp -d 127.0.0.2 --dport 80 -j DNAT --to-destination 127.0.0.1:8000
sudo iptables -t nat -A PREROUTING -p tcp -d 127.0.0.2  --dport 80 -j DNAT --to-destination 127.0.0.2:8000

iptables -t nat -A PREROUTING -d 8.8.8.8 -j DNAT --to-destination 192.168.1.20
iptables -t nat -A POSTROUTING -s 192.168.1.20 -j SNAT --to-source 8.8.8.8

sudo iptables -t nat -A PREROUTING -d 127.0.0.2 -j DNAT --to-destination 127.0.0.2:8000
sudo iptables -t nat -A POSTROUTING -s 127.0.0.2 -j SNAT --to-source 127.0.0.2:8000

sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -L

sudo iptables -t nat -A PREROUTING -p tcp -d 127.0.0.2  --dport 80 -j DNAT --to-destination 127.0.0.2:8000
sudo -s iptables-save -c



iptables -t nat -A PREROUTING -d 127.0.0.2 -p tcp --dport 80 -j REDIRECT --to-port 8000
"""
"""
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 80
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()

"""
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

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

