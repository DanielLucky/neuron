import json

import jwt
from aiohttp import web
from aiohttp.web_middlewares import middleware

from app.user import manager

secret = "секретный секрет"


@middleware
async def protect_jwt(request, handler):

    white_list = ['/logs', '/get_token']
    if request.path not in white_list:
        token = request.headers.get('Authorization', None)
        if token:
            try:
                id_user = jwt.decode(token.split()[1], secret, algorithms=["HS256"])
                request['user'] = id_user
                user_model = await manager.get_user(request)
                if user_model:
                    request['user'].update({'user_model': user_model})
                    return await handler(request)
            except jwt.exceptions.InvalidSignatureError as _ex:
                return web.Response(body=json.dumps({'error_message': 'token is not valid'}), status=401)

        return web.Response(body=json.dumps({'error_message': 'token not found'}), status=401)

    return await handler(request)


async def get_token(request: web.Request):
    try:
        user_name = request.rel_url.query.get('user_name')
        if user_name:
            request['user'] = {'user_name': user_name}
            user_model = await manager.add_user(request)
            jwt_token = jwt.encode({"user_id": user_model.id}, secret, algorithm="HS256")
            return web.Response(body=json.dumps({'token': 'Bearer '+jwt_token}), status=201)
    except Exception as _ex:
        raise _ex




