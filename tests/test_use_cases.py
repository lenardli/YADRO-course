from datetime import date

from application.use_cases import AppService, CurrencyService
from domain.entitites import App, Author, Currency
from domain.interfaces import IAppRepository, IAuthorRepository, ICurrencyRepository


class FakeCurrencyRepo(ICurrencyRepository):
    def get_currency(self, currency_code, target_date):
        code = (currency_code or "USD").upper()
        return Currency(date=target_date, rates={code: 1.0})


class FakeAppRepo(IAppRepository):
    def get_app(self) -> App:
        return App(version="0.0.1", service="test")


class FakeAuthorRepo(IAuthorRepository):
    def get_author(self) -> Author:
        return Author(name="tester")


def test_currency_service_default_date() -> None:
    svc = CurrencyService(FakeCurrencyRepo())
    result = svc.get_currency_info("usd", None)
    assert result.rates["USD"] == 1.0
    assert result.date == date.today()


def test_currency_service_parses_date() -> None:
    svc = CurrencyService(FakeCurrencyRepo())
    result = svc.get_currency_info("eur", "2020-05-01")
    assert result.rates["EUR"] == 1.0
    assert result.date == date(2020, 5, 1)


def test_app_service_returns_app_and_author() -> None:
    svc = AppService(FakeAppRepo(), FakeAuthorRepo())
    app_obj, author = svc.get_app_info()
    assert app_obj.version == "0.0.1"
    assert app_obj.service == "test"
    assert author.name == "tester"
