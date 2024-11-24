from __future__ import annotations

from .import util
from .. import dap
from .. import core

import os

class MyLuaInstaller(util.vscode.AdapterInstaller):
    type = 'lua'

    async def install(self, version: str|None, log: core.Logger):
        # path = 'D:\\lua-debug\\publish'
        # await self.install_local(path, log=log)
        url = 'https://github.com/huanzai/lua-debug/releases/download/2.0.11/lua-debug-2.0.11.vsix'
        await self.install_vsix(url, log = log)

    async def installable_versions(self, log: core.Logger) -> list[str]:
        return ["default"]

class MyLua(dap.AdapterConfiguration):
    type = 'lua'
    docs = 'https://github.com/huanzai/lua-debug'
    installer = MyLuaInstaller()

    async def start(self, log: core.Logger, configuration: dap.ConfigurationExpanded):
        install_path = self.installer.install_path()
        command = [
            f'{install_path}/bin/lua-debug.exe'
        ]
        return dap.StdioTransport(command)

    def resolve_config(self, config: dap.Configuration):
        json = config.copy()
        if json.get('stopOnThreadEntry', None) == None:
            json['stopOnThreadEntry'] = False

        if json.get('luaVersion', None) == None:
            json['luaVersion'] = 'lua54'

        if json.get('luaArch', None) == None:
            json['luaArch'] = 'x86_64'

        if json.get('console', None) == None:
            json['console'] = 'integratedTerminal'

        if json.get('sourceCoding', None) == None:
            json['sourceCoding'] = 'utf8'

        if json.get('outputCapture', None) == None:
            json['outputCapture'] = []

        if json.get('pathFormat', None) == None:
            json['pathFormat'] = 'path'

        if json.get('inject', None) == None:
            json['inject'] = 'none'

        if json.get('client', None) == None:
            json['client'] = True

        if json.get('configuration', None) == None:
            json['configuration'] = {
                'variables':{'showIntegerAsHex':False}
            }
        new_config = dap.Configuration(config.name, -1, config.type, config.request, json, config.source)
        new_config.id_ish = config.id_ish
        return new_config

