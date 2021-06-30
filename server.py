from http.server import BaseHTTPRequestHandler, HTTPServer
# from wireguard import Peer
import argparse, ast, platform, re, subprocess
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", type=int, help="HTTPServer hosting port")
# parser.add_argument("config", help="Path of WireGuard Interface config file")
# action = "store_true" | "count"
# choices=[0, 1, 2]

args = parser.parse_args()

PORT = args.port or 80
HOST = 'localhost'
NEW_LINE = '\r\n' if platform.system() == 'Windows' else '\n'
# p1 = Peer({'PublicKey': 'key', 'AllowedIPs': 'IPs'})

class Handler(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json') # 'text/html', 'image/x-icon'
		self.end_headers()

	def _path_finder(self, path: str, request='GET', data={}):
		if path == '/interfaces':
			show = subprocess.run(['wg', 'show'], capture_output=True).stdout.decode('utf-8')
			interfaces = [re.search(r'(?<=^interface: ).*', line).group(0) for line in show.split(NEW_LINE) if re.search(r'(?<=^interface: ).*', line)]
			return str(interfaces)

		if path[:11] == '/interface/':
			interface = path[11:]
			if request == 'GET':
				conf = subprocess.run(['wg', 'showconf', interface], capture_output=True).stdout.decode('utf-8')
				return conf
			if request == 'POST':
				# PublicKey, AllowedIPs = data.get('PublicKey'), data.get('AllowedIPs')				
				keys = {data.get('PublicKey'): 'PublicKey', data.get('AllowedIPs'): 'AllowedIPs'}

				if keys.get(None):
					return "{} cannot be None".format(keys.get(None))

				add_peer = subprocess.run(['wg', 'set', interface, 'peer', data.get('PublicKey'), 'allowed-ips', data.get('AllowedIPs')], capture_output=True)

				if add_peer.stderr:
					return add_peer.stderr.decode('utf-8')
				else:
					# return str(add_peer.stdout.decode('utf-8'))
					show = subprocess.run(['wg', 'show'], capture_output=True).stdout.decode('utf-8')
					show_stripped = [line.strip() for line in show.split(NEW_LINE)]
					for line_number, line in enumerate(show_stripped):
						if 'peer: {}'.format(data.get('PublicKey')) in line:
							return str(show_stripped[line_number: line_number+4])
					return "fail"

			if request == 'DELETE':
				keys = {data.get('PublicKey'): 'PublicKey'}
				if keys.get(None):
					return "{} cannot be None".format(keys.get(None))
				remove_peer = subprocess.run(['wg', 'set', interface, 'peer', data.get('PublicKey'), 'remove'], capture_output=True)
				if remove_peer.stderr:
					return remove_peer.stderr.decode('utf-8')
				else:
					show = subprocess.run(['wg', 'show'], capture_output=True).stdout.decode('utf-8')
					show_stripped = [line.strip() for line in show.split(NEW_LINE)]
					for line_number, line in enumerate(show_stripped):
						if 'peer: {}'.format(data.get('PublicKey')) in line:
							return str(show_stripped[line_number: line_number+4])
					return "success"


	# do_GET method name cannot be changed
	def do_GET(self):
		self._set_response()
		response = self._path_finder(self.path) or ''
		self.wfile.write(response.encode('utf-8'))

	def do_POST(self):
		self._set_response()
		content_length = int(self.headers['Content-Length'])
		encoded_data = self.rfile.read(content_length)
		dict_data = ast.literal_eval(encoded_data.decode('utf-8'))
		response = self._path_finder(self.path, request='POST', data=dict_data) or ''
		self.wfile.write(response.encode('utf-8'))

def main():
	server = HTTPServer((HOST, PORT), Handler)
	print("Server running on address {}:{}".format(HOST,PORT))
	server.serve_forever()

if __name__ == '__main__':
	main()
