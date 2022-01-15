from __future__ import annotations
import sys
import sublime
import sublime_plugin

if sublime.version() < '4000':
	raise Exception('This version of Debugger requires st4, use the st3 branch')

module_starts_with = __package__ + '.'

modules_to_remove = list(filter(lambda m: m.startswith(module_starts_with) and m != __name__, sys.modules.keys()))
for m in modules_to_remove:
	del sys.modules[m]


# import all the commands so that sublime sees them
from .modules.command import CommandsRegistry, DebuggerExecCommand, DebuggerCommand, DebuggerInputCommand

from .modules.core.sublime import DebuggerAsyncTextCommand, DebuggerEventsListener
from .modules.autocomplete import AutocompleteEventListener
from .modules.typecheck import *

from .modules import core
from .modules import ui
from .modules import dap

from .modules.debugger import Debugger
from .modules.views.variable import VariableComponent

from .modules.adapters import * 
#import all the adapters so Adapters.initialize() will see them

from .modules.adapters_registry import AdaptersRegistry
from .modules.settings import SettingsRegistery, Settings

was_opened_at_startup: Set[int] = set()


def plugin_loaded() -> None:
	core.log_info('startup')
	ui.startup()
	SettingsRegistery.initialize()
	AdaptersRegistry.initialize()
	CommandsRegistry.initialize()

	for window in sublime.windows():
		open(window)


def plugin_unloaded() -> None:
	core.log_info('shutdown')
	for key, instance in dict(Debugger.instances).items():
		instance.dispose()
	Debugger.instances = {}
	ui.shutdown()


def open(window_or_view: Union[sublime.View, sublime.Window]):
	if isinstance(window_or_view, sublime.View):
		window = window_or_view.window()
	else:
		window = window_or_view

	if not window:
		return

	if Settings.open_at_startup and (not window.id() in was_opened_at_startup) and Debugger.should_auto_open_in_window(window):
		was_opened_at_startup.add(window.id())
		Debugger.get(window, create=True)

# if there is a debugger running in the window then that is the most relevant one
# otherwise all debuggers are relevant
def most_relevant_debuggers_for_view(view: sublime.View) -> Iterable[Debugger]:
	if debugger := debugger_for_view(view):
		return [debugger]

	return list(Debugger.instances.values())

def debugger_for_view(view: sublime.View) -> Debugger|None:
	if window := view.window():
		if debugger := Debugger.get(window):
			return debugger
	return None

class Listener (sublime_plugin.EventListener):

	def ignore(self, view: sublime.View):
		return not bool(Debugger.instances)

	def on_new_window(self, window: sublime.Window):
		open(window)

	def on_pre_close_window(self, window: sublime.Window):
		if debugger := Debugger.get(window):
			debugger.dispose()

	def on_exit(self):
		core.log_info('saving project data: {}'.format(Debugger.instances))
		for key, instance in dict(Debugger.instances).items():
			instance.save_data()

	def on_load_project(self, window: sublime.Window):
		if debugger := Debugger.get(window):
			debugger.project.reload()

	@core.schedule
	async def on_hover(self, view: sublime.View, point: int, hover_zone: int):
		if self.ignore(view): return

		debugger = debugger_for_view(view)
		if not debugger:
			return

		project = debugger.project

		if hover_zone != sublime.HOVER_TEXT or not project.is_source_file(view):
			return

		if not debugger.session:
			return

		session = debugger.session

		r = session.adapter_configuration.on_hover_provider(view, point)
		if not r:
			return
		word_string, region = r

		try:
			response = await session.evaluate_expression(word_string, 'hover')
			await core.sleep(0.25)
			variable = dap.types.Variable("", response.result, response.variablesReference)
			view.add_regions('selected_hover', [region], scope="comment", flags=sublime.DRAW_NO_OUTLINE)

			def on_close() -> None:
				view.erase_regions('selected_hover')

			component = VariableComponent(dap.Variable(session, variable))
			component.toggle_expand()
			ui.Popup(ui.div(width=100)[component], view, region.a, on_close=on_close)

		# errors trying to evaluate a hover expression should be ignored
		except dap.Error as e:
			core.log_error('adapter failed hover evaluation', e)

	def on_text_command(self, view: sublime.View, cmd: str, args: dict[str, Any]) -> Any:
		if self.ignore(view): return

		if (cmd == 'drag_select' or cmd == 'context_menu') and 'event' in args:
			# on_view_drag_select_or_context_menu(view)

			event = args['event']
			x: int = event['x']
			y: int = event['y']

			view_x, _ = view.layout_to_window(view.viewport_position()) #type: ignore

			margin = view.settings().get('margin') or 0
			offset = x - view_x #type: ignore

			if offset < -30 - margin:
				pt = view.window_to_text((x, y))
				line = view.rowcol(pt)[0]

				# only rewrite this command if someone actually consumed it
				# otherwise let sublime do its thing
				if self.on_view_gutter_clicked(view, line, event['button']):
					return ('null', {})

	def on_view_gutter_clicked(self, view: sublime.View, line: int, button: int) -> bool:
		line += 1 # convert to 1 based lines

		debuggers = most_relevant_debuggers_for_view(view)
		if not debuggers:
			return False

		items: list[ui.InputListItem] = []

		for debugger in debuggers:
			breakpoints = debugger.breakpoints
			file = view.file_name()
			if not file: continue

			if window := view.window():
				window.focus_view(view)
			
			if button == 1:
				debugger.breakpoints.source.toggle_file_line(file, line)

			elif button == 2:
				source_breakpoints = breakpoints.source.get_breakpoints_on_line(file, line)
				if source_breakpoints:
					debugger.breakpoints.source.edit_breakpoints(source_breakpoints)

		return True