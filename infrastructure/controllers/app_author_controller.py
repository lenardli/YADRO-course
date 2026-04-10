from fastapi import APIRouter

from application.use_cases import AppService
from infrastructure.presenters.config_presenter import ConfigAppService

router = APIRouter()


@router.get("/info")
def get_app_info() -> dict:
    config_repository = ConfigAppService()
    service = AppService(
        app_repository=config_repository,
        author_repository=config_repository)

    app, author = service.get_app_info()

    return {
        "version": app.version,
        "service": app.service,
        "author": author.name,
    }
