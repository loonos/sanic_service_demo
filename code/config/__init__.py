import os
from sanic import Sanic


REQUIRES = [
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DB",
    "REDIS_HOST",
    "REDIS_PORT"
]


class CheckConfigException(Exception):
    ...


def check_configs(app):
    for k in REQUIRES:
        v = app.config.get(k)
        if not v:
            raise CheckConfigException(f"Missing config: {k}")


def init_configs(app: Sanic):
    try:
        check_configs(app)
        return
    except CheckConfigException:
        ...

    work_dir = os.getcwd()
    app_conf = os.path.join(work_dir, "./config/settings.py")
    if os.path.isfile(app_conf):
        app.config.update_config(app_conf)

    check_configs(app)
