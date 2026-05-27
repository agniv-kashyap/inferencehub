from pydantic import BaseModel


class InferenceResponse(BaseModel):

    task_id: str

    status: str