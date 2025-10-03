from fastapi.responses import JSONResponse
from configs.constants import MESSAGES

def response_ok(code: str, data: dict):
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "code": code,
            "message": MESSAGES.get(code, ""),
            "data": data
        }
    )

def response_ok_issues(code: str, data: dict):
    return JSONResponse(
        status_code=202,
        content={
            "status": False,
            "code": code,
            "message": MESSAGES.get(code, ""),
            "data": data
        }
    )

def response_validation_issues(code: str, data: dict, errors: list):
    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "code": code,
            "message": MESSAGES.get(code, ""),
            "data": data,
            "errors": errors
        }
    )

def response_server_error():
    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "code": "SERVER_ERROR",
            "message": MESSAGES.get("SERVER_ERROR", ""),
            "data": {}
        }
    )

def response_unauthenticated():
    return JSONResponse(
        status_code=401,
        content={
            "status": False,
            "code": "UNAUTHENTICATED",
            "message": MESSAGES.get("UNAUTHENTICATED", ""),
            "data": {}
        }
    )

