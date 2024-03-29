

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
		if diff_count > 0 and listener_count == diff_count or diff_count < 0 and listener_count == 0:
			self._input_control._request_rebuild()

	def connect(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).connect(*a, **k)

	def disconnect(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).disconnect(*a, **k)

	def disconnect_all(self, *a, **k):
		with self._listeners_update():
			super(InputSignal, self).disconnect_all(*a, **k)
	


class MonoBridgeElement(NotifyingControlElement):
	__module__ = __name__
	__doc__ = ' Class representing a 2-dimensional set of buttons '

	__subject_events__ = (SubjectEvent(name='value', signal=InputSignal, override=True),)
	_input_signal_listener_count = 0

	def __init__(self, script, *a, **k):
		super(MonoBridgeElement, self).__init__(script, *a, **k)
		self._script = script
		
	def refresh_state(self):
		self._script.refresh_state()

	def _send(self, args1 = None, args2 = None, args3 = None, args4 = None):
		#self._button_value(args1, args2, args3, args4)
		self.notify_value(args1, args2, args3, args4)
	

	def reset(self):
		pass

