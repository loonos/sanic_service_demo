from sanic.views import HTTPMethodView
from library.utils import common_request
from webargs_sanic.sanicparser import use_kwargs
from .reqargs import some_get_args, some_post_args
from ..service.services import some_get_svc, some_post_svc


class SomeAPI(HTTPMethodView):

    @common_request()
    @use_kwargs(some_get_args, location="query")
    async def get(self, request, **kwargs):
        type_ = kwargs["type"]
        page = kwargs["page"]
        size = kwargs["size"]
        return await some_get_svc(request, type_, page, size)

    @common_request()
    @use_kwargs(some_post_args)
    async def post(self, request, **kwargs):
        type_ = kwargs["type"]
        name = kwargs["name"]
        return await some_post_svc(request, type_, name)
