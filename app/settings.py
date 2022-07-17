import logging
import os

import asyncpg
from aiohttp import web

from app.picture.routes import picture_routes
from database import db

#  SETTINGS LOGGER
log_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/log.log'))
console_handler = logging.StreamHandler()
logging.basicConfig(handlers=(log_handler, console_handler),
                    format='%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: %(levelname)s: %(message)s',
                    level=logging.INFO)
factory = logging.getLogRecordFactory()
logging.getLogger('concurrent').setLevel(logging.CRITICAL)
logging.getLogger('aiohttp').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('asyncpg').setLevel(logging.CRITICAL)
logging.getLogger('PIL').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)


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
