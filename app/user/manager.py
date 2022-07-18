import inspect
import logging

from aiohttp import web

from app.user.models import User

logger = logging.getLogger('app')


async def add_user(request: web.Request) -> User:
    async with request.app['db'].acquire() as connection:
        result = await connection.fetch(
            '''
                INSERT INTO public."user" (name)
                VALUES ($1)
                returning *;
            ''',
            request['user'].get('user_name')
        )
    logger.info('Add user () in DB',
                extra={'route': request.path_qs,
                       'functionName': inspect.getframeinfo(inspect.currentframe()).function})
    return User(**result[0])


async def get_user(request: web.Request) -> User:
    async with request.app['db'].acquire() as connection:
        result = await connection.fetch(
            '''
                SELECT * 
                FROM public."user"
                WHERE id = $1;
            ''',
            request['user'].get('user_id')
        )
    logger.info('Get user () for DB',
                extra={'route': request.path_qs,
                       'functionName': inspect.getframeinfo(inspect.currentframe()).function})

    # request['user'].update({'user_model': User(**result[0])})
    if result:
        return User(**result[0])
