from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.auth import APIKeyCreateRequest
from app.schemas.auth import APIKeyResponse

from app.services.auth_service import create_api_key


router = APIRouter()


@router.post(
    "/auth/keys",
    response_model=APIKeyResponse
)
async def generate_key(
    request: APIKeyCreateRequest,
    db: Session = Depends(get_db)
):

    api_key = create_api_key(
        db=db,
        developer_email=request.developer_email,
        tier=request.tier
    )

    return {
        "api_key": api_key,
        "message": (
            "Store this key securely. "
            "It will not be shown again."
        )
    }