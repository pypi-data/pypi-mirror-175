from lib2to3.pgen2.token import OP
from captur_ml_sdk.dtypes.generics import Image, Meta

from pydantic import (
    BaseModel
)
from typing import Optional


class Model(BaseModel):
    endpoint_id: str
    location: Optional[str] = "us-central1"
    task: Optional[str] = "classification"
    type: Optional[str] = "automl"
    serving_input: Optional[str] = "bytes_input"

    class Config:
        arbitrary_types_allowed = True


class ModelLivePredictRequest(BaseModel):
    meta: Optional[Meta] = None
    model: Model
    data: Image
