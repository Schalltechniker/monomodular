# emacs-mode: -*- python-*-
from __future__ import with_statement
import Live
import time



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
		self._devices = []
		self.client_0 = clients[0]
		self.client_1 = clients[1]
		self.client_2 = clients[2]
		self.client_3 = clients[3]
		self.client_4 = clients[4]
		self.client_5 = clients[5]
		self._client = clients
	


	def disconnect(self):
		for client in self._client:
			client = None
		self._client = []
		NotifyingControlElement.disconnect(self)
	

	def _send(self, args1 = None, args2 = None, args3 = None, args4 = None):
		self.notify_value(args1, args2, args3, args4)
		#self._host.log_message('switchboard send' + str(self._host._in_build_midi_map) + str(self._host._enabled) + str(args1) + str(args2) + str(args3) + str(args4))
		"""for entry in self._value_notifications:
			callback = entry['Callback']
			try:
				callback(args1, args2, args3, args4)
			except:
				self._host.log_message('failed callback ' + str(callback) + ' removing')
				self.remove_value_listener(callback)"""	

	def reset(self):
		pass
	

	def request_connection(self, device, version, inLive = 0):
		#self._host.log_message('request_connection ' + str(device))
		if version == self._host._version_check:
			client_num = 6	
			for client in self._client:
				if client.device == device:
					client._disconnect_client()
			for client in self._client: 
				if client._connected is False:
					client._connect_to(device)
					client_num = client._number
					break
		else:
			client_num = self._host._version_check
		return client_num
	

	def force_connection(self, device, client_number, version):
		#self._host.log_message('force ' + str(device) + ' ' + str(client_number) + ' build ' + str(self._host._in_build_midi_map))
		if version == self._host._version_check:
			for client in self._client:
				if client.device == device:
					client._disconnect_client()
			self._client[client_number]._disconnect_client(True)
			self._client[client_number]._connect_to(device)
		else:
			client_number = self._host._version_check
		return client_number
	

	def set_client_enabled(self, client_num, enabled):
		self._client[client_num].set_enabled(enabled)
	

# local variables:
# tab-width: 4
