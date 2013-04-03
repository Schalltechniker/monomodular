# emacs-mode: -*- python-*-
#from _Framework_old.NotifyingControlElement import NotifyingControlElement
#from _MXDCore import *
#from _Framework_old.ButtonElement import ButtonElement
#from _Framework_old.ButtonMatrixElement import ButtonMatrixElement

from __future__ import with_statement
import contextlib
from _Framework.SubjectSlot import SubjectEvent
from _Framework.Signal import Signal
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.Util import in_range
from _Framework.Debug import debug_print
from _Framework.Disconnectable import Disconnectable

class InputSignal(Signal):
	"""
	Special signal type that makes sure that interaction with input
	works properly. Special input control elements that define
	value-dependent properties should use this kind of signal.
	"""

	def __init__(self, sender = None, *a, **k):
		super(InputSignal, self).__init__(sender=sender, *a, **k)
		self._input_control = sender

	@contextlib.contextmanager
	def _listeners_update(self):
		old_count = self.count
		yield
		diff_count = self.count - old_count
		self._input_control._input_signal_listener_count += diff_count
		listener_count = self._input_control._input_signal_listener_count
		#if diff_count > 0 and listener_count == diff_count or diff_count < 0 and listener_count == 0:
		#	self._input_control._request_rebuild()

	def connect(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).connect(*a, **k)

	def disconnect(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).disconnect(*a, **k)

	def disconnect_all(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).disconnect_all(*a, **k)

class SwitchboardElement(NotifyingControlElement):
	__module__ = __name__
	__doc__ = ' Class that connects and disconnects monomodular clients'


	__subject_events__ = (SubjectEvent(name='value', signal=InputSignal, override=True),)
	_input_signal_listener_count = 0

	def __init__(self, host, clients, *a, **k):
		super(SwitchboardElement, self).__init__(host, clients, *a, **k)
		self._host = host
		self._value_notifications = []
		self._devices = []
		self.client_0 = clients[0]
		self.client_1 = clients[1]
		self.client_2 = clients[2]
		self.client_3 = clients[3]
		self.client_4 = clients[4]
		self.client_5 = clients[5]
		self.client_6 = clients[6]
		self.client_7 = clients[7]
		self.client_8 = clients[8]
		self.client_9 = clients[9]
		self.client_10 = clients[10]
		self.client_11 = clients[11]
		self.client_12 = clients[12]
		self.client_13 = clients[13]
		self.client_14 = clients[14]
		self.client_15 = clients[15]
		self._client = clients
	

	def disconnect(self):
		for client in self._client:
			client = None
		self._client = []
		NotifyingControlElement.disconnect(self)
	

	def send_swing(self, client, val):
		#self._host._script.log_message('send_swing' + ' ' + str(client) + ' ' + str(val))
		self._host._client[client].receive_swing(val)
	

	def receive_swing(self, client, val):
		#self._host.log_message('send_swing' + ' ' + str(client) + ' ' + str(val))
		self._send('receive_swing', client, val)
	

	def disconnect_client(self, device):
		for index in range(16):
			if self._client[index].device == device:
				self._client[index]._disconnect_client()
	

	def reset(self):
		pass
	

	def _send(self, args1 = None, args2 = None, args3 = None, args4 = None):
		self.notify_value(args1, args2, args3, args4)
		#self._host.log_message('switchboard send' + str(self._host._in_build_midi_map) + str(self._host._enabled) + str(args1) + str(args2) + str(args3) + str(args4))
		#for entry in self._value_notifications:
		#	callback = entry['Callback']
		"""try:
			callback(args1, args2, args3, args4)
		except:
			self._host.log_message('failed callback ' + str(callback) + ' removing')
			self.remove_value_listener(callback)"""

	

	def reset_callbacks(self):
		for entry in self._value_notifications:
			callback = entry['Callback']
			self.remove_value_listener(callback)
		self._value_notifications = []
	

	def request_connection(self, device, version, inLive = 0):
		#self._host.log_message('request_connection ' + str(device))
		if version == self._host._version_check:
			client_num = 16
			for index in range(16):
				if self._client[index].device == device:
					self._client[index]._disconnect_client()
			for index in range(16): 
				if self._client[index]._connected is False:
					self._client[index]._connect_to(device)
					client_num = self._client[index]._number
					break
		else:
			client_num = self._host._version_check
		return client_num
	

	def force_connection(self, device, client_number, version):
		#self._host.log_message('force ' + str(device) + ' ' + str(client_number) + ' build ' + str(self._host._in_build_midi_map))
		if version == self._host._version_check:
			for index in range(16):
				if self._client[index].device == device:
					self._client[index]._disconnect_client()
			self._client[client_number]._disconnect_client(True)
			self._client[client_number]._connect_to(device)
		else:
			client_number = self._host._version_check
		return client_number
	

	def editor_connection(self, device, version):
		#self._host.log_message('editor_connection ' + str(device) + ' ' + ' build ' + str(self._host._in_build_midi_map))
		if version == self._host._version_check:
			client_num = 16
			for index in range(16): 
				if self._client[index]._connected is False:
					self._client[index]._connect_to(device)
					client_num = self._client[index]._number
					break
		else:
			client_num = self._host._version_check
		return client_num
	

	def set_client_enabled(self, client_num, enabled):
		self._client[client_num].set_enabled(enabled)
	

# local variables:
# tab-width: 4
