import math
from datetime import datetime
from library.utils import use_cache
from sqlalchemy import select, func
from .common import paginate
from ..model.models import SomeModel
from ..model.schemas import SomeModelSchema


@use_cache()
async def some_get_svc(request, type_, page, size):
    query_res = []
    total = 0

    session = request.ctx.session
    async with session.begin():
        stmt = select(SomeModel.type,
                      SomeModel.name,
                      SomeModel.add_time).where(SomeModel.type == type_)

        paged = await paginate(session, stmt, page, size)

    schema = SomeModelSchema(many=True)
    return {"page": paged.page, "size": paged.size,
            "pages": paged.pages, "total": paged.total,
            "items": schema.dump(paged.items)}


async def some_post_svc(request, type_, name):
    query_res = 0

    session = request.ctx.session
    async with session.begin():
        item = SomeModel(type=type_,
                         name=name,
                         add_time=datetime.now())
        session.add(item)
        await session.flush()
        query_res = item.id

    return query_res
