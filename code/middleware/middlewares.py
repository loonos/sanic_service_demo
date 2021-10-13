from json import dumps
from sanic import Request, HTTPResponse
from sanic.log import logger


async def request_log(request: Request):
    body = dumps(request.json) if request.json else request.body.decode()
    logger.info(
        f"[#{request.id}] Request: {request.method} {request.url}, body: {body}"
    )


async def response_log(request: Request, response: HTTPResponse):
    body = response.body.decode()
    logger.info(
        f"[#{request.id}] Response: {body}"
    )
