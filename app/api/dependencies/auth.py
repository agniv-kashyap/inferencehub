from fastapi import Header
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.models.api_key import APIKey

from app.core.security import hash_api_key


async def validate_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):

    hashed_key = hash_api_key(
        x_api_key
    )

    api_key_record = db.query(APIKey).filter(
        APIKey.hashed_key == hashed_key,
        APIKey.is_active == True
    ).first()

    if not api_key_record:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return api_key_record