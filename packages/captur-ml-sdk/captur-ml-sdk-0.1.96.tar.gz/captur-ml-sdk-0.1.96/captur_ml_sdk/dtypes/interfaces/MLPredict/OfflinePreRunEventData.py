from pydantic import (
    BaseModel,
    HttpUrl, root_validator
)

from typing import Optional, List

from captur_ml_sdk.dtypes.generics import Image, PredictMeta
from captur_ml_sdk.dtypes.interfaces.validators import check_images_or_imagefile_has_data


class OfflinePreRunEventData(BaseModel):
    request_id: str
    meta: Optional[PredictMeta]
    images: Optional[List[Image]]
    imagesfile: Optional[str]
    model_name: str
    model_id: str
    model_type: str
    labels_source: Optional[str]

    root_validator(check_images_or_imagefile_has_data)
