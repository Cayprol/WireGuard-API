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

p1 = Peer({'PublicKey': 'key', 'AllowedIPs': 'IPs'})

# import subprocess
# result = subprocess.run(['wg', 'show'], stdout=subprocess.PIPE)
# print(result.stdout)
# print(result.stdout.decode('utf-8'))

# wg0 = WireGuard({'test1': 1})
# wg0.update({'test2': 2})
# wg0['test3'] = 3
# print("print wg0", wg0)
# print("print wg0.test1", wg0.test1)
# print("print wg0.test2", wg0.test2)
# print("print wg0.test3", wg0.test3)
# print("print wg0.__dict__", wg0.__dict__)
# p1 = Peer({'test1': 1})
# p1.update({'test2': 2})
# p1['test3'] = 3
# print("print p1", p1)
# print("print p1.test1", p1.test1)
# print("print p1.test2", p1.test2)
# print("print p1.test3", p1.test3)
# print("print p1.__dict__", p1.__dict__)