import io
import json
import os

import uuid

import PIL
from PIL import Image
from aiohttp import web

from app.config import PATH_SAVE_PICTURE
from app.picture import manager


async def post_picture(request: web.Request) -> web.Response:
    """
    Accepts image format (jpeg, png, ...)
    :param request:
    :return:
    """
    quality = request.rel_url.query.get('quality')
    width = request.rel_url.query.get('x')
    height = request.rel_url.query.get('y')

    if content_data := await request.content.read():
        try:
            image = Image.open(io.BytesIO(content_data))
            if image.format != 'JPEG':
                image = image.convert('RGB')
                image.format = 'JPEG'

            if width and height:
                image = image.resize((int(height), int(width)))

            picture_model = await manager.add_picture(request=request, image=image, image_quality=int(quality) if quality else 100)
            image.save(picture_model.picture_path, quality=picture_model.quality if picture_model.quality else 100)

            return web.Response(body=picture_model.to_json(), status=201)

        except PIL.UnidentifiedImageError as _ex:
            return web.Response(body=json.dumps({'error_message': 'invalid format file'}), status=400)
        except ValueError as _ex:
            return web.Response(body=json.dumps({'error_message': 'failed parse parameters'}), status=400)

    return web.Response(body=json.dumps({'error_message': 'file not found'}), status=400)


async def get_picture(request: web.Request):
    id_ = request.rel_url.query.get('id')
    if id_:
        if picture_model := await manager.get_picture(request=request, id_=id_):
            return web.FileResponse(picture_model.picture_path)

    else:
        return web.Response(body=json.dumps({'error_message': f'failed parse parameters'}), status=400)
    return web.Response(body=json.dumps({'error_message': f'picture {id_} not found'}), status=400)




