import time
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Header, HTTPException, Request, status

from .config import get_settings


@dataclass
class AuditEvent:
    action: str
    actor: str
    approved: bool


class InMemoryRateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> bool:
        now = time.monotonic()
        bucket = self._requests[key]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            return False
        bucket.append(now)
        return True


rate_limiter = InMemoryRateLimiter()


def client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def enforce_rate_limit(request: Request) -> None:
    if not rate_limiter.check(client_key(request)):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    settings = get_settings()
    if settings.env == "development" and settings.secret_key == "change-me":
        return "development-user"
    if not x_api_key or x_api_key != settings.secret_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return "api-user"


def require_human_approval(x_human_approval: str | None = Header(default=None)) -> None:
    if x_human_approval != "approved":
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail="Human approval required for risky write actions",
        )


def approved_action(action_name: str) -> Callable[[str | None], None]:
    def dependency(x_human_approval: str | None = Header(default=None)) -> None:
        require_human_approval(x_human_approval)

    return dependency
