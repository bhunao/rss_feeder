from src.routers.articles import router as articles
from src.routers.sources import router as sources
from src.routers.users import router as users
from src.routers.subscriptions import router as subscriptions
from src.routers.database_test import router as database_test

routers_list = [
        articles,
        sources,
        users,
        subscriptions,
        ]
