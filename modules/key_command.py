import sublime
import sublime_plugin

from . import core
from .debugger import Debugger

class KeyCommand:
	@staticmethod
	def get_debugger(window):
		debugger = Debugger.get(window)
		if not debugger or not debugger.is_open():
			debugger = Debugger.create(window, skip_project_check = False)
		return debugger

	@staticmethod
	def open_debugger(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)
		try:
			if debugger.current_session and Debugger.is_paused:
				debugger.resume()
		except:
			debugger.start(False)

	@staticmethod
	def step_over(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)
		try:
			if Debugger.is_paused:
				debugger.step_over()
		except core.Error as e:
			self.console.error(f'Unable to step over: {e}')

	@staticmethod
	def step_in(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)
		try:
			if Debugger.is_paused:
				debugger.step_in()
		except core.Error as e:
			self.console.error(f'Unable to step in: {e}')