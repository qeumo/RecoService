from main import config
from service.db.ann_index import AnnIndex
from service.gdown_utils import gdrive_read

item_dataset = gdrive_read(config.item_dataset_filename,
                           config.item_dataset_fileid)

ann_index = AnnIndex(ann_index_ip=config.ann_index_ip)
ann_index.create_upload_col(vectors=item_dataset.to_numpy(),
                            ids=item_dataset.index.tolist(),
                            col_name=config.db_collection_name)
