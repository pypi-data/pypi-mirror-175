import importlib
import os
import sys
from pathlib import Path

import aiohttp_session
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from jija import middlewares
from jija.app import App
from jija import commands
from jija.utils.collector import collect_subclasses
from jija import config
from jija.config.base import Base


class AppGetter(type):
    def __getattr__(self, item):
        """
        :type item: str
        :rtype: App
        """

        app = Apps.apps.get(item)
        if app:
            return app

        raise AttributeError(item)


class Apps(metaclass=AppGetter):
    apps = {}
    commands = {
        'system': commands.COMMANDS
    }

    @classmethod
    def load(cls):
        cls.__init_configs()
        Apps.apps['core'] = cls.__create_base_app()
        cls.__collect(config.StructureConfig.APPS_PATH, Apps.apps['core'])
        cls.__register_apps()

    @staticmethod
    def __init_configs():
        for config_class in collect_subclasses(config, config.base.Base):
            if not config_class.INITED and config_class.REQUIRED:
                config_class()

    @classmethod
    def __create_base_app(cls):
        """
        :rtype: web.Application
        """

        aiohttp_app = web.Application()
        aiohttp_session.setup(aiohttp_app, EncryptedCookieStorage(config.ProjectConfig.SECRET_KEY))

        aiohttp_app.middlewares.extend([
            middlewares.print_request.PrintRequest(),
        ])

        if cls.app_exists(config.StructureConfig.CORE_PATH):
            app_class = cls.get_modify_class(config.StructureConfig.CORE_PATH)
        else:
            app_class = App

        app = app_class(path=config.StructureConfig.CORE_PATH, aiohttp_app=aiohttp_app, name='core')

        return app

    @staticmethod
    def app_exists(path: Path) -> bool:
        return path.joinpath('app.py').exists()

    @classmethod
    def __collect(cls, path: Path, parent: App):
        if not path.exists():
            return

        for sub_app_name in os.listdir(path):

            next_path = path.joinpath(sub_app_name)
            if App.is_app(next_path):
                app = cls.get_modify_class(next_path)(path=next_path, parent=parent, name=sub_app_name)
                cls.commands[sub_app_name] = app.commands
                cls.apps[sub_app_name] = app
                cls.__collect(path.joinpath(sub_app_name), app)

    @staticmethod
    def get_modify_class(path: Path) -> type:
        modify_class_path = path.joinpath('app')
        import_path = ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

        module = importlib.import_module(import_path)
        modify_class = list(collect_subclasses(module, App))
        return modify_class[0] if modify_class else App

    @classmethod
    def __register_apps(cls, app=None):
        """
        :type app: App
        """

        if not app:
            app = cls.apps['core']

        if not app.childes and app.name != 'core':
            app.parent.aiohttp_app.add_subapp(f'/{app.name}', app.aiohttp_app)

        for child in app.childes:
            cls.__register_apps(child)

    @classmethod
    def get_command(cls, module, command):
        """
        :type module: str
        :type command: str
        :rtype: type
        """

        if module is None:
            module = 'system'

        return cls.commands[module][command]

    @classmethod
    def run_command(cls):
        args = sys.argv
        command = args[1].split('.')
        Apps.load()

        if len(command) == 1:
            module = None
            command = command[0]
        else:
            module, command = command

        command_class = cls.get_command(module, command)
        command_obj = command_class()
        command_obj.run()
