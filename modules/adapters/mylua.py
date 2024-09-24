from __future__ import annotations

from .import util
from .. import dap
from .. import core

import os

class MyLuaInstaller(util.vscode.AdapterInstaller):
    type = 'mylua'

    async def install(self, version: str|None, log: core.Logger):
        path = ''
        await self.install_vsix(path, log=log)

    async def post_install(self, version: str|None, log: core.Logger):
        ...

class MyLua(dap.AdapterConfiguration):

    type = 'mylua'
    docs = 'https://github.com/huanzai/lua-debug'
    development = True
    installer = MyLuaInstaller()

    async def start(self, log: core.Logger, configuration: dap.ConfigurationExpanded):
        node = await util.get_and_warn_require_node(self.type, log)
        install_path = self.installer.install_path()
        command = [
            node,
            f'{install_path}/out/debugAdapter.js'
        ]
        return dap.StdioTransport(command)
