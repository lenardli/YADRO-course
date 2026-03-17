import os

from domain.entitites import App, Author
from domain.interfaces import IAppRepository, IAuthorRepository


class ConfigAppService(IAppRepository, IAuthorRepository):
    DEFAULT_VERSION = "1.0.0"
    DEFAULT_AUTHOR = "a.sheynova"
    DEFAULT_SERVICE = "currency"

    def get_app(self) -> App:
        version = os.getenv("VERSION", self.DEFAULT_VERSION)
        service = os.getenv("SERVICE", self.DEFAULT_SERVICE)
        return App(version=version, service=service)

    def get_author(self) -> Author:
        name = os.getenv("AUTHOR", self.DEFAULT_AUTHOR)
        return Author(name=name)
