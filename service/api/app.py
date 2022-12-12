import asyncio
import os
import pickle
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from ..db.ann_index import AnnIndex
from ..gdown_utils import download_file_from_google_drive
from ..log import app_logger, setup_logging
from ..settings import ServiceConfig
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


user_dataset_filename = 'user_dataset.pkl'
user_dataset_fileid = '1gMfP4iaSDK2cbXx--o4fuHWtc_s7Qswj'
if not os.path.exists(user_dataset_filename):
    download_file_from_google_drive(user_dataset_fileid, user_dataset_filename)
user_dataset = pickle.load(open(user_dataset_filename, 'rb'))

cold_reco_filename = 'cold_reco.pkl'
cold_reco_fileid = '1SAhZjDdoO8SdiM4aRojsi-1sHpLSmTDi'
if not os.path.exists(cold_reco_filename):
    download_file_from_google_drive(cold_reco_fileid, cold_reco_filename)
cold_reco = pickle.load(open(cold_reco_filename, 'rb'))


def create_app(config: ServiceConfig) -> FastAPI:
    setup_logging(config)
    setup_asyncio(thread_name_prefix=config.service_name)

    app = FastAPI(debug=False)
    app.state.k_recs = config.k_recs
    app.state.db_collection_name = config.db_collection_name
    app.user_dataset = user_dataset
    app.cold_reco = cold_reco
    app.ann_index = AnnIndex(ann_index_ip=config.ann_index_ip)

    add_views(app)
    add_middlewares(app)
    add_exception_handlers(app)

    return app
