from sanic import Sanic


def register_middlewares(app: Sanic):
    from .middlewares import request_log, response_log

    app.register_middleware(request_log, attach_to="request")
    app.register_middleware(response_log, attach_to="response")
