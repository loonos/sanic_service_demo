from aioredis import ConnectionPool, StrictRedis
from sanic import Sanic


def init_redis(app: Sanic):
    host = app.config.get("REDIS_HOST")
    port = app.config.get("REDIS_PORT")
    db = app.config.get("REDIS_DB")
    username = app.config.get("REDIS_USERNAME")
    password = app.config.get("REDIS_PASSWORD")

    conf = {}
    if db:
        conf["db"] = db
    if username:
        conf["username"] = username
    if password:
        conf["password"] = password

    @app.after_server_start
    async def redis_connect(app, loop):
        pool = ConnectionPool.from_url(f"redis://{host}:{port}", **conf)
        redis = StrictRedis(connection_pool=pool)
        app.ctx.redis = redis

    # https://aioredis.readthedocs.io/en/latest/migration/#cleaning-up
    # @app.before_server_stop
    # async def redis_disconnect(app, loop):
    #     redis = app.ctx.redis
    #     await redis.connection_pool.disconnect()
