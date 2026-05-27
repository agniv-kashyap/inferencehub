from pydantic import BaseModel


class InferenceRequest(BaseModel):

    pipeline: str


class InferenceResponse(BaseModel):

    task_id: str

    status: str