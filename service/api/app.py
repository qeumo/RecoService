import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from ..dummy import Dummy
from ..log import app_logger, setup_logging
from ..settings import ServiceConfig
from ..user_knn import OfflineUserKnnRecommender, OnlineUserKnnRecommender
from .exception_handlers import add_exception_handlers
from .middlewares import add_middlewares
from .views import add_views

__all__ = ("create_app",)


def setup_asyncio(thread_name_prefix: str) -> None:
    uvloop.install()

    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix)
    loop.set_default_executor(executor)

    def handler(_, context: Dict[str, Any]) -> None:
        message = "Caught asyncio exception: {message}".format_map(context)
        app_logger.warning(message)

    loop.set_exception_handler(handler)


def create_app(config: ServiceConfig) -> FastAPI:
    setup_logging(config)
    setup_asyncio(thread_name_prefix=config.service_name)

    app = FastAPI(debug=False)
    app.state.k_recs = config.k_recs
    app.state.models = {
        'tfidf_idf_offline': OfflineUserKnnRecommender(
            config.tfidf_idf_offline,
            Path(config.models_dir),
            config.popular_name),
        'tfidf_idf_online': OnlineUserKnnRecommender(
            config.tfidf_idf_online,
            Path(config.models_dir),
            config.popular_name,
            config.train_name),
        'recsys_model': Dummy(
            config.dummy,
            Path(config.models_dir),
            config.dummy_dataset),
    }

    add_views(app)
    add_middlewares(app)
    add_exception_handlers(app)

    return app
