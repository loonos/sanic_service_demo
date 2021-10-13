import math
from datetime import datetime
from library.utils import use_cache
from sqlalchemy import select, func
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

        query = await session.execute(stmt.limit(size).
                                      offset((page - 1) * size))
        query_res = query.all()

        total = await session.execute(select(func.count().label("total")).
                                      select_from(stmt.subquery()))
        total = total.fetchone().total

    schema = SomeModelSchema(many=True)
    return {"page": page, "size": size, "total": total,
            "pages": int(math.ceil(total / float(size))),
            "items": schema.dump(query_res)}


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
