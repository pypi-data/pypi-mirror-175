import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from saika.app import SaikaApp


class Environ:
    app = None  # type: SaikaApp
    debug: bool

    program_dir: str
    data_dir: str

    config_path: str

    @staticmethod
    def into_app_context_do(f, *args, **kwargs):
        with Environ.app.app_context():
            return f(*args, **kwargs)

    @staticmethod
    def into_request_context_do(environ, f, *args, **kwargs):
        with Environ.app.request_context(environ):
            return f(*args, **kwargs)

    @staticmethod
    def is_gunicorn():
        return "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")

    @staticmethod
    def is_pyinstaller():
        return hasattr(sys, '_MEIPASS')
