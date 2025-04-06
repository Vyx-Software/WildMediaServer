from pydantic import BaseModel
from typing import Optional

class HTTPError(BaseModel):
    detail: str
    code: Optional[str] = None
    context: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Resource not found",
                "code": "not_found",
                "context": {"resource_id": "123"}
            }
        }

class ValidationErrorItem(BaseModel):
    loc: list[str]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: list[ValidationErrorItem]