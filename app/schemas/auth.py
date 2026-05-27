from pydantic import BaseModel
from pydantic import EmailStr


class APIKeyCreateRequest(BaseModel):

    developer_email: EmailStr

    tier: str = "free"


class APIKeyResponse(BaseModel):

    api_key: str

    message: str