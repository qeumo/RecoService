import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from ..db.ann_index import AnnIndex
from ..gdown_utils import gdrive_read
from ..log import app_logger, setup_logging
from ..settings import ServiceConfig, get_config
from .exception_handlers import add_exception_handlers
from .middlewares import add_middlewares
from .views import add_views

__all__ = ("create_app",)
config = get_config()
user_dataset = gdrive_read(config.user_dataset_filename,
                           config.user_dataset_fileid)
cold_reco = gdrive_read(config.cold_reco_filename,
                        config.cold_reco_fileid)


def setup_asyncio(thread_name_prefix: str) -> None:
    uvloop.install()

    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix)
    loop.set_default_executor(executor)

    def handler(_, context: Dict[str, Any]) -> None:
        message = "Caught asyncio exception: {message}".format_map(context)
        app_logger.warning(message)

    loop.set_exception_handler(handler)


def create_app(app_config: ServiceConfig) -> FastAPI:
    setup_logging(app_config)
    setup_asyncio(thread_name_prefix=app_config.service_name)

    app = FastAPI(debug=False)
    app.state.k_recs = app_config.k_recs
    app.state.db_collection_name = app_config.db_collection_name
    app.state.user_dataset = user_dataset
    app.state.cold_reco = cold_reco
    app.state.ann_index = AnnIndex(ann_index_ip=app_config.ann_index_ip)

    add_views(app)
    add_middlewares(app)
    add_exception_handlers(app)

    return app
