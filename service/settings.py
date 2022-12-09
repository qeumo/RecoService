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
    models_dir: str = "models"
    tfidf_idf_offline: str = "tfidf_idf_offline.pkl"
    popular_name: str = "popular.pkl"
    tfidf_idf_online: str = "TFIDF_10.dill"
    train_name: str = "train.csv"
    dummy: str = "model.pkl"
    dummy_dataset: str = "dataset.pkl"

    log_config: LogConfig


def get_config() -> ServiceConfig:
    return ServiceConfig(
        log_config=LogConfig(),
    )
