from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from .entitites import App, Author, Currency


class ICurrencyRepository(ABC):
    @abstractmethod
    def get_currency(
        self,
        currency_code: Optional[str],
        date: date,
    ) -> Currency:
        pass


class IAuthorRepository(ABC):
    @abstractmethod
    def get_author(self) -> Author:
        pass


class IAppRepository(ABC):
    @abstractmethod
    def get_app(self) -> App:
        pass
