import asyncpg
from aiohttp import web

from app.picture.routes import picture_routes
from database import db


async def create_app():
    application = web.Application()

    picture_routes(application)

    application.on_startup.append(on_start)
    application.on_cleanup.append(on_shutdown)

    return application


async def on_start(application):
    application['db'] = await asyncpg.create_pool(dsn=db.DSN)


async def on_shutdown(application):
    await application['db'].close()
