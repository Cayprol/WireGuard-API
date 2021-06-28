from http.server import BaseHTTPRequestHandler, HTTPServer
from wireguard import Peer
import argparse, ast, platform, re, subprocess
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", type=int, help="HTTPServer hosting port")
# parser.add_argument("config", help="Path of WireGuard Interface config file")
# action = "store_true" | "count"
# choices=[0, 1, 2]

args = parser.parse_args()

PORT = args.port or 80
HOST = 'localhost'
NEW_LINE = "\r\n" if platform.system() == "Windows" else "\n" 
# p1 = Peer({'PublicKey': 'key', 'AllowedIPs': 'IPs'})

class Handler(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		# self.send_header('Content-type', 'text/html')
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def _identify_path(self, path: str):
		path = path.lower()
		if path == '/interfaces':
			return str(self._get_interfaces())

		if path[:11] == '/interface/':
			interface = path[11:]
			conf = subprocess.run(['wg', 'showconf', interface], stdout=subprocess.PIPE).stdout.decode('utf-8')
			print(conf)
			return conf

	def _get_interfaces(self):
		show = subprocess.run(['wg', 'show'], stdout=subprocess.PIPE).stdout.decode('utf-8')
		print(show)
		interfaces = [re.search(r'(?<=^interface: ).*', line).group(0) for line in show.split(NEW_LINE) if re.search(r'(?<=^interface: ).*', line)]
		return interfaces

	# do_GET method name cannot be changed for handling GET request
	def do_GET(self):
		# self.path
		self._set_response()
		response = self._identify_path(self.path)
		self.wfile.write(response.encode('utf-8'))

		# content_length = int(self.headers['Content-Length'])
		# raw_data = self.rfile.read(content_length)

		# data_dict = ast.literal_eval(raw_data.decode('utf-8'))
		# print(type(raw_data), type(data_dict))
		# print(data_dict)
		# print(self.path)
		# self.wfile.write(raw_data)

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
