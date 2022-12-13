from pydantic import BaseSettings


class Config(BaseSettings):

    class Config:
        case_sensitive = False


class LogConfig(Config):
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        case_sensitive = False
        fields = {
            "level": {
                "env": ["log_level"]
            },
        }


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10
    db_collection_name: str = 'reco'
    ann_index_ip: str = 'qdrant'
    user_dataset_filename: str = 'user_dataset.pkl'
    user_dataset_fileid: str = '1gMfP4iaSDK2cbXx--o4fuHWtc_s7Qswj'
    cold_reco_filename: str = 'cold_reco.pkl'
    cold_reco_fileid: str = '1SAhZjDdoO8SdiM4aRojsi-1sHpLSmTDi'
    item_dataset_filename: str = 'item_dataset.pkl'
    item_dataset_fileid: str = '1pNBUY3SUJCOfwBbYQsGzpum-NwO5caaT'

    log_config: LogConfig


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
