from fastapi.responses import JSONResponse
from configs.constants import MESSAGES

def response(
    code: str,
    status_code: int = 200,
    data: dict = {},
    errors: list = []
):
    response_content = {
        "status": status_code == 200,
        "code": code,
        "message": MESSAGES.get(code, ""),
        "data": data
    }

    if errors:
        response_content["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=response_content
    )

def response_unauthenticated():
    return response("UNAUTHENTICATED", status_code=401)

def response_validation_issues(code: str, data: dict, errors: list):
    return response(code, status_code=422, data=data, errors=errors)

