from pydantic import BaseModel


class UnAuthorizedError(BaseModel):
    status_code: int = 401
    reason: str = "Unauthorized credentials"
