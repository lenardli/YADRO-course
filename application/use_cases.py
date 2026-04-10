from datetime import date, datetime
from typing import Optional

from domain.entitites import App, Author, Currency
from domain.interfaces import IAppRepository, IAuthorRepository, ICurrencyRepository


class CurrencyService:
    def __init__(self, repository: ICurrencyRepository) -> None:
        self._repository = repository

    def get_currency_info(
        self,
        currency_code: Optional[str],
        date_str: Optional[str],
    ) -> Currency:
        today = date.today()
        target_date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d").date() if date_str else today)
        return self._repository.get_currency(currency_code, target_date)


class AppService:
    def __init__(self, app_repository: IAppRepository,
                 author_repository: IAuthorRepository) -> None:
        self._app_repository = app_repository
        self._author_repository = author_repository

    def get_app_info(self) -> tuple[App, Author]:
        app = self._app_repository.get_app()
        author = self._author_repository.get_author()
        return app, author
