import os.path
import pickle
from pathlib import Path

from service.gdown_utils import download_file_from_google_drive


class Dummy:
    def __init__(self, model_name: str,
                 models_dir: Path = Path('models'),
                 data_name: str = 'dataset.sav'):
        if not os.path.exists(models_dir / model_name):
            download_file_from_google_drive(
                '1-FOStMxn6Z-VA22xE70aeLa0noWZEfIq',
                models_dir / model_name)
        if not os.path.exists(models_dir / data_name):
            download_file_from_google_drive(
                '1HCALVMCHKVPekBPq8_8HXW6oubM5Kgjv',
                models_dir / data_name)
        with open(models_dir / model_name, 'rb') as f:
            self.model = pickle.load(f)
        with open(models_dir / data_name, 'rb') as f:
            self.dataset = pickle.load(f)

    def recommend(self, user: int, k: int = 10):
        return self.model.recommend(
            [user],
            dataset=self.dataset,
            k=k,
            filter_viewed=False)['item_id'].values.tolist()
