import pickle
from main import config
from service.db.ann_index import AnnIndex

item_dataset_filename = 'item_dataset.pkl'
item_dataset = pickle.load(open(item_dataset_filename, 'rb'))

ann_index = AnnIndex(ann_index_ip=config.ann_index_ip)
ann_index.create_upload_col(vectors=item_dataset.to_numpy(),
                            ids=item_dataset.index.tolist(),
                            col_name=config.db_collection_name)
