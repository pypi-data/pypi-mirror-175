from pydantic import BaseModel, root_validator
from typing import Optional

from captur_ml_sdk.dtypes.interfaces.MLGateway.MLMetaRequest import ModelMetaRequest
from captur_ml_sdk.dtypes.interfaces.MLGateway.MLPredictRequest import ModelPredictRequest
from captur_ml_sdk.dtypes.interfaces.MLGateway.MLLivePredictRequest import ModelLivePredictRequest
from captur_ml_sdk.dtypes.interfaces.MLGateway.MLTrainRequest import ModelTrainRequest
from captur_ml_sdk.dtypes.interfaces.MLGateway.MLEvalRequest import ModelEvaluateRequest
from captur_ml_sdk.dtypes.interfaces.MLGateway.MLRegisterModel import ModelRegisterRequest


class GatewayRequest(BaseModel):
    meta: Optional[ModelMetaRequest]
    predict: Optional[ModelPredictRequest]
    live_predict: Optional[ModelLivePredictRequest]
    train: Optional[ModelTrainRequest]
    evaluate: Optional[ModelEvaluateRequest]
    register_model: Optional[ModelRegisterRequest]

    @root_validator
    def request_must_have_predict_live_predict_train_or_evaluate(cls, values):
        if not values.get("predict") \
                and not values.get("live_predict") \
                and not values.get("train") \
                and not values.get("evaluate") \
                and not values.get("register_model"):
            raise ValueError(
                "Request must include either 'predict', 'live_predict', 'train', 'evaluate' or 'register_model'")

        return values

# if __name__ == "__main__":
#     print(MLGatewayRequest.schema_json(indent=2))
