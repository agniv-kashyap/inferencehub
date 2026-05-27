import time

from fastapi import HTTPException
from fastapi import Depends

from app.core.redis import redis_client

from app.api.dependencies.auth import validate_api_key


WINDOW_SIZE = 60


FREE_TIER_LIMIT = 5

PREMIUM_TIER_LIMIT = 100

async def rate_limit_dependency(
    api_key=Depends(validate_api_key)
):

    developer_id = api_key.developer_email

    tier = api_key.tier

    current_time = time.time()

    window_start = current_time - WINDOW_SIZE

    redis_key = f"rate_limit:{developer_id}"

    if tier == "premium":

        request_limit = PREMIUM_TIER_LIMIT

    else:

        request_limit = FREE_TIER_LIMIT

    redis_client.zremrangebyscore(
        redis_key,
        0,
        window_start
    )

    request_count = redis_client.zcard(
        redis_key
    )

    if request_count >= request_limit:

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    
    redis_client.zadd(
        redis_key,
        {
            str(current_time): current_time
        }
    )

    redis_client.expire(
        redis_key,
        WINDOW_SIZE
    )

    return api_key