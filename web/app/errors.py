
from fastapi import HTTPException


S400_INVALID_URL = HTTPException(status_code=400, detail="Invalid url.")
