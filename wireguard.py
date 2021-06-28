import platform
NEW_LINE = "\r\n" if platform.system() == "Windows" else "\n" 
class WireGuard(dict):
	"""
	__setitem__ is called when assigning value by indices
	setattr() function store {key: value} into __dict__
	
	if the indice key is a str and also a valid formatting variable name, e.g. wg['key_name'], wg.key_name is available
	wg.key_name fetch what's in wg.__dict__

	Standard dict class has no __dict__ attribute, therefore, dict.key_name return AttributeError

	When printing the instance, __repr__ is printed, __dict__ is not
	super() __init__(), __setitem__(), update() contains logic to __repr__
	"""
	_requirements = []
	def __init__(self, iterable):
		self._init_requirement(iterable)
		super().__init__(iterable)
		for key in iterable:
			setattr(self, key, iterable[key])

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		setattr(self, key, value)

	# def __getitem__(self, key):
	# 	return getattr(self, key)

	def update(self, iterable):
		super().update(iterable)
		for key in iterable:
			setattr(self, key, iterable[key])

	def _init_requirement(self, iterable):
		for requirement in self._requirements:
			if requirement not in iterable:
				raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, requirement))

class Peer(WireGuard):
	_requirements = ['PublicKey', 'AllowedIPs']


class Interface(WireGuard):
	_requirement = ['PrivateKey', 'Address']

# p1 = Peer({'PublicKey': 'key', 'AllowedIPs': 'IPs'})

# 1. Get names of all interfaces by 'wg show'
# 2. Get each interface running status in config format by 'wg showconf <interface>'
# 3. Turn config format into dictionary
# import subprocess, json, re

# def peers(lines):
# 	peers = [line_number for line_number, line in enumerate(lines) if '[Peer]' in line]
# 	return peers

# def stanza(conf):
# 	lines = conf.split(NEW_LINE)
# 	peer_stanzas = peers(lines)
# 	print(peer_stanzas)
# 	interface_stanza = lines[:peer_stanzas[0]-1]
# 	return interface_stanza



# show = subprocess.run(['wg', 'show'], stdout=subprocess.PIPE).stdout.decode('utf-8')
# interfaces = [re.search(r'(?<=^interface: ).*', line).group(0) for line in show.split(NEW_LINE) if re.search(r'(?<=^interface: ).*', line)]
# for interface in interfaces:
# 	conf = subprocess.run(['wg', 'showconf', interface], stdout=subprocess.PIPE).stdout.decode('utf-8')
# 	print(stanza(conf))

try: 
	subprocess.run(['wg', 'showconf', 'test'], stdout=subprocess.PIPE).stdout.decode('utf-8')
except:
	print("error")