import sublime
import sublime_plugin

from . import core
from .debugger import Debugger

class KeyCommand:
	@staticmethod
	def get_debugger(window):
		debugger = Debugger.get(window)
		if not debugger:
			debugger = Debugger.create(window, skip_project_check = True)
		return debugger

	@staticmethod
	def open_debugger(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)

		try:
			if debugger.current_session and debugger.is_paused():
				debugger.resume()
		except:
			if not debugger.is_open():
				debugger.open()
			else:
				debugger.start(False)

	@staticmethod
	def toggle_breakpoint(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)
		debugger.toggle_breakpoint()

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

	@staticmethod
	def step_out(view: sublime.View):
		window = view.window()
		debugger = KeyCommand.get_debugger(window)
		try:
			if Debugger.is_paused:
				debugger.step_out()
		except core.Error as e:
			self.console.error(f'Unable to step out: {e}')