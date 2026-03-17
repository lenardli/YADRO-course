from fastapi import FastAPI

from infrastructure.controllers.app_author_controller import router as app_info_router
from infrastructure.controllers.currency_controller import router as currency_router


def create_app() -> FastAPI:
    app = FastAPI(title="YADRO Currency Service")
    app.include_router(app_info_router)
    app.include_router(currency_router)
    return app


app = create_app()
