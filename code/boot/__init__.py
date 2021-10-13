from sanic import Sanic
from config import init_configs
from cache import init_redis
from database import init_databases
from middleware import register_middlewares
from router import register_routes


def init():

    app = Sanic(__name__)
    init_configs(app)
    init_redis(app)
    init_databases(app)
    register_routes(app)
    register_middlewares(app)

    return app
