from __future__ import annotations

from .import util
from .. import dap
from .. import core

import os

class MyLuaInstaller(util.vscode.AdapterInstaller):
    type = 'mylua'

    async def install(self, version: str|None, log: core.Logger):
        path = 'D:\\lua-debug\\publish'
        await self.install_local(path, log=log)

    async def installable_versions(self, log: core.Logger) -> list[str]:
        return ["default"]

class MyLua(dap.AdapterConfiguration):
    type = 'mylua'
    docs = 'https://github.com/huanzai/lua-debug'
    installer = MyLuaInstaller()

    async def start(self, log: core.Logger, configuration: dap.ConfigurationExpanded):
        install_path = self.installer.install_path()
        command = [
            f'{install_path}/bin/lua-debug.exe'
        ]
        return dap.StdioTransport(command)
