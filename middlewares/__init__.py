from .throttling import ThrottlingMiddleware
from .big_brother import BigBrother
from .acl import ACLMiddleware
from .sentinel import Sentinel

from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware())
    dp.middleware.setup(BigBrother())
    dp.middleware.setup(Sentinel())
