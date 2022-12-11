import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.conversions.common_types import CollectionInfo
from qdrant_client.http.models import Distance, VectorParams


class AnnIndex:
    def __init__(self, ann_index_ip: str, port: int = 6333):
        self.client = QdrantClient(host=ann_index_ip, port=port)

    def create_upload_col(self,
                          vectors: np.ndarray,
                          ids: list,
                          col_name: str,
                          payload: list = None,
                          upload_batch_size: int = 512,
                          distance: Distance = Distance.DOT) -> CollectionInfo:
        self.client.recreate_collection(collection_name=col_name,
                                        vectors_config=VectorParams(
                                            size=vectors.shape[1],
                                            distance=distance),
                                        on_disk_payload=False)
        self.client.upload_collection(
            collection_name=col_name,
            vectors=vectors,
            payload=payload,
            ids=ids,
            batch_size=upload_batch_size,
            parallel=6
        )
        col = self.client.get_collection(col_name)
        return col
