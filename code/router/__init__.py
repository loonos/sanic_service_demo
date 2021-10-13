from sanic import Sanic
from app.api.apis import SomeAPI


def register_routes(app: Sanic):
    app.add_route(SomeAPI.as_view(), f"/api")
