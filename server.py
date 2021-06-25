from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
from wireguard import Peer
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", type=int, help="HTTPServer hosting port")
# parser.add_argument("config", help="Path of WireGuard Interface config file")
# action = "store_true" | "count"
# choices=[0, 1, 2]

args = parser.parse_args()

PORT = args.port or 80
HOST = ''

p1 = Peer({'PublicKey': 'key', 'AllowedIPs': 'IPs'})

class Handler(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		# self.send_header('Content-type', 'text/html')
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	# do_GET method name cannot be changed for handling GET request
	def do_GET(self):
		# self.path
		self._set_response()
		content_length = int(self.headers['Content-Length'])
		data = self.rfile.read(content_length)
		self.wfile.write(data)

	def do_POST(self):
		self._set_response()
		content_length = int(self.headers['Content-Length'])
		data = self.rfile.read(content_length)
		self.wfile.write(data)

def main():
	server = HTTPServer((HOST, PORT), Handler)
	print("Server running on address {}:{}".format(HOST,PORT))
	server.serve_forever()

if __name__ == '__main__':
	main()
