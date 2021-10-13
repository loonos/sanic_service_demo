import traceback
from functools import wraps
from hashlib import md5
from ujson import dumps, loads
from sanic import Request
from sanic.response import json
from sanic.log import logger


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def titlecase(s):
    parts = iter(s.split("_"))
    return "".join(i.title() for i in parts)


def common_request():
    def decorator(func):
        @wraps(func)
        async def wrapper(view, request: Request, *args, **kwargs):

            status_code = 200
            res = {"success": True, "message": "success"}
            try:
                resp = await func(view, request, *args, **kwargs)
                res["data"] = resp
            except Exception as ex:
                logger.debug(traceback.format_exc())
                status_code = ex.status_code\
                    if hasattr(ex, "status_code") else 400
                try:
                    err = dumps(ex.data.get("messages"))
                except:
                    err = str(ex)
                res["success"] = False
                res["message"] = err
                res["data"] = None

            return json(res, status_code)

        return wrapper
    return decorator


def use_cache(timeout=30):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            redis = request.app.ctx.redis
            args_hash = md5(str(args).encode()).hexdigest()[:8]
            cache_key = f"{func.__name__}.{args_hash}"

            cached = await redis.get(cache_key)
            if cached is not None:
                try:
                    return loads(cached)
                except:
                    return cached

            res = await func(request, *args, **kwargs)
            await redis.setex(cache_key, timeout, dumps(res))
            return res

        return wrapper
    return decorator
