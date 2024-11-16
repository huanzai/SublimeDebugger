from __future__ import annotations
from typing import Any, Protocol

import sublime
import traceback
import sys
import shutil
import os

_should_log_exceptions = True
_should_log_error = True
_should_log_info = True
_log_tofile = False
_log_file_path = None

def _custom_print(*args, **kwargs):
	if _log_tofile:
		with open(_log_file_path, mode='a') as f:
			print(*args, **kwargs, file=f)
	else:
		print(*args, **kwargs)


def log_configure(log_info: bool, log_errors: bool, log_exceptions: bool, log_tofile: bool = False, log_file_path: str = None):
	global _should_log_exceptions
	global _should_log_error
	global _should_log_info
	global _log_tofile
	global _log_file_path

	_should_log_exceptions = log_exceptions
	_should_log_error = log_errors
	_should_log_info = log_info
	_log_tofile = log_tofile
	_log_file_path = log_file_path

def info(*args: Any) -> None:
	if not _should_log_info:
		return
	_custom_print('Debugger:', *args)

def error(*args: Any) -> None:
	if not _should_log_error:
		return
	_custom_print('Debugger: error:', *args)

def alert(*args: Any) -> None:
	sublime.error_message(str(args))

	if not _should_log_error:
		return
	_custom_print('Debugger: error:', *args)

def exception(*args: Any) -> None:
	if not _should_log_exceptions:
		return

	if args:
		_custom_print('Debugger: error:', *args)
	_custom_print(traceback.format_exc())


def debug(*args: Any) -> None:
	if not _should_log_info:
		return
	_custom_print('Debugger:', *args)


class Logger(Protocol):
	def log(self, type: str, value: Any):
		_custom_print(f'Debugger: {type}: {value}')

	def __call__(self, type: str, value: Any):
		self.log(type, value)

	def error(self, text: str):
		self.log('error', text)

	def warn(self, text: str):
		self.log('warn', text)

	def info(self, text: str):
		self.log('info', text)

class StdioLogger(Logger):
	def log(self, type: str, value: Any):
		_custom_print(f'Debugger: {type}: {value}')


stdio = StdioLogger()
