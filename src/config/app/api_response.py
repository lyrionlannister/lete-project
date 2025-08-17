
from typing import Union, Dict, List
from fastapi.responses import JSONResponse

async def make_api_response(
    success: bool,
    status_code: int = 200,
    data: Union[Dict, List] | None = None,
    message: str | None = None
) -> JSONResponse:
    response_dict = {
        "success": success,
        "status_code": status_code,
    }

    if data is not None:
        response_dict["data"] = data

    if message is not None:
        response_dict["message"] = message

    return JSONResponse(content=response_dict, status_code=status_code)
