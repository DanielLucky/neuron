import logging
import os

import jwt
import asyncpg
from aiohttp import web

from app.config import PATH_LOGS, PATH_SAVE_PICTURE
from app.picture.routes import picture_routes
from database import db
from middleware import jwt_protect
from middleware.jwt_protect import protect_jwt

logger = logging.getLogger('app')


def init_logger():
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(PATH_LOGS, 'logs.log'))
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatters
    format_ = logging.Formatter('%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: %(levelname)s: %(message)s')
    f_handler.setFormatter(format_)
    c_handler.setFormatter(format_)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.setLevel(logging.INFO)


async def create_app():
    application = web.Application(middlewares=[protect_jwt])

    # Routers
    picture_routes(application)
    application.router.add_get("/get_token", jwt_protect.get_token)

    application.on_startup.append(on_start)
    application.on_cleanup.append(on_shutdown)

    return application


async def on_start(application):
    application['db'] = await asyncpg.create_pool(dsn=db.DSN)


async def on_shutdown(application):
    await application['db'].close()


# Create catalogs
if not os.path.exists(PATH_LOGS):
    os.mkdir(PATH_LOGS)

if not os.path.exists(PATH_SAVE_PICTURE):
    os.mkdir(PATH_SAVE_PICTURE)

init_logger()
