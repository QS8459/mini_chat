from fastapi import (
    Request,
    status,
    HTTPException,
    Response
)
from fastapi.responses import JSONResponse
from src.conf.loging import log


async def logger(request: Request, call_next):
    try:
        # log.info("")
        response = await call_next(request)
    except Exception as e:
        log.error("Exception happened while handling request \n{}".format(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Something Went Wrong"}
        )
    return response
