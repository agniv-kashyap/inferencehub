# Business logic for inference operations

from app.utils.fake_ml import fake_model_inference

class InferenceService:
    def run(self, input_data: str):
        return fake_model_inference(input_data)
