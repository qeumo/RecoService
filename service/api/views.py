from typing import List

from fastapi import APIRouter, Depends, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.auth_bearer import JWTBearer
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()
available_models = ["recsys_model", "ann_model"]


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    responses={
        404: {
            "description": "Model not found"
        },
        401: {
            "description": "Not authenticated"
        }
    },
    dependencies=[Depends(JWTBearer())]
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if user_id > 1e9:
        # return RecoResponse(user_id=user_id, items=list(range(10)))
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    if model_name not in available_models:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    k_recs = request.app.state.k_recs
    db_collection_name = request.app.state.db_collection_name
    ann_index = request.app.state.ann_index
    cold_reco = request.app.state.cold_reco
    app_logger.info(cold_reco)

    try:
        hits = ann_index.client.search(
            collection_name=db_collection_name,
            query_vector=request.app.state.user_dataset.loc[user_id],
            query_filter=None,
            append_payload=True,
            with_vectors=False,
            limit=k_recs
        )
        recs = [h.id for h in hits]
    except KeyError:
        return RecoResponse(user_id=user_id, items=cold_reco)

    return RecoResponse(user_id=user_id, items=recs)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
