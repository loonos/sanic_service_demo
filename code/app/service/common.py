import math
from sqlalchemy import func, select


async def paginate(session, stmt, page, size):
    class Paginate:
        def __init__(self, items, page, size, total):
            self.items = items
            self.page = page
            self.size = size
            self.total = total
            self.pages = int(math.ceil(total / float(size)))

    query_items = await session.execute(stmt.limit(size).
                                        offset((page - 1) * size))
    items = query_items.all()

    query_total = await session.execute(select(func.count().label("total")).
                                        select_from(stmt.order_by(None).subquery()))
    total = query_total.fetchone().total

    return Paginate(items, page, size, total)
