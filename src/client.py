from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient
)
from msrest.authentication import ApiKeyCredentials
# import time

# Replace with valid values
ENDPOINT = "https://cookiecv-prediction.cognitiveservices.azure.com/"
prediction_key = "3fcae069691347218a9e1afa117e2719"
prediction_resource_id = "17578923-d759-4d95-835f-3e1a5a8d2638"


prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key}
)

predictor = CustomVisionPredictionClient(
    ENDPOINT,
    prediction_credentials
)
