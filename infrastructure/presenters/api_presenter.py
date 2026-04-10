from datetime import date, datetime
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from domain.entitites import Currency
from domain.interfaces import ICurrencyRepository


class APICurrencyService(ICurrencyRepository):
    BASE_URL = "https://www.cbr.ru/scripts"

    def get_currency(
        self,
        currency_code: Optional[str],
        date: date,
    ) -> Currency:
        target_date = date or datetime.today().date()
        if currency_code:
            all_rates = self._fetch_all_currencies(target_date)
            code = currency_code.upper()
            rate = all_rates.get(code)
            rates = {code: rate} if rate is not None else {}
        else:
            rates = self._fetch_all_currencies(target_date)

        return Currency(date=target_date, rates=rates)

    def _fetch_all_currencies(self, target_date: date) -> dict[str, float]:
        cbr_date = target_date.strftime("%d/%m/%Y")
        query = urlencode({"date_req": cbr_date})
        url = f"{self.BASE_URL}/XML_daily.asp?{query}"

        with urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        rates: dict[str, float] = {}

        for valute in root.findall("Valute"):
            char_code_el = valute.find("CharCode")
            value_el = valute.find("Value")
            if (
                char_code_el is None
                or value_el is None
                or not char_code_el.text
                or not value_el.text
            ):
                continue
            rates[char_code_el.text.upper()] = float(
                value_el.text.replace(",", "."))

        return rates
