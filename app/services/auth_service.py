from sqlalchemy.orm import Session

from app.models.api_key import APIKey

from app.core.security import generate_api_key
from app.core.security import hash_api_key


def create_api_key(
    db: Session,
    developer_email: str,
    tier: str
):

    raw_api_key = generate_api_key()

    hashed_key = hash_api_key(
        raw_api_key
    )

    api_key_record = APIKey(
        developer_email=developer_email,
        hashed_key=hashed_key,
        tier=tier
    )

    db.add(api_key_record)

    db.commit()

    db.refresh(api_key_record)

    return raw_api_key