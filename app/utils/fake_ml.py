# Fake ML helper for local testing

def fake_model_inference(input_data: str):
    return {"output_data": input_data[::-1], "confidence": 0.9}
