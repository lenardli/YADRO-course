from fastapi import APIRouter, Query

from application.use_cases import CurrencyService
from infrastructure.presenters.api_presenter import APICurrencyService

router = APIRouter()


@router.get("/info/currency")
def get_currency_info(
    currency: str | None = Query(default=None),
    date: str | None = Query(default=None),
) -> dict:
    service = CurrencyService(repository=APICurrencyService())
    currency_entity = service.get_currency_info(
        currency_code=currency,
        date_str=date,
    )

    return {
        "service": "currency",
        "data": currency_entity.rates,
    }
