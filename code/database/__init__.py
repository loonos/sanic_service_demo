from contextvars import ContextVar
from sanic import Sanic, Request, HTTPResponse
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def init_databases(app: Sanic):
    host = app.config.get("MYSQL_HOST")
    port = app.config.get("MYSQL_PORT")
    user = app.config.get("MYSQL_USER")
    password = app.config.get("MYSQL_PASSWORD")
    db = app.config.get("MYSQL_DB")
    pool_recycle = app.config.get("MYSQL_POOL_RECYCLE", 1800)
    url = URL.create(drivername="mysql+aiomysql",
                     username=user,
                     password=password,
                     host=host,
                     port=port,
                     database=db)

    _bind = create_async_engine(url, pool_recycle=pool_recycle)
    _session_ctx = ContextVar("session")

    @app.on_request
    async def inject_db_session(request: Request):
        request.ctx.session = sessionmaker(
            _bind, AsyncSession, expire_on_commit=False
        )()
        request.ctx.session_ctx_token = _session_ctx.set(
            request.ctx.session
        )

    @app.on_response
    async def close_db_session(request: Request, response: HTTPResponse):
        if hasattr(request.ctx, "session_ctx_token"):
            _session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
