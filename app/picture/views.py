import inspect
import io
import json
import logging

import PIL
from PIL import Image
from aiohttp import web

from app.picture import manager


async def post_picture(request: web.Request) -> web.Response:
    """
    POST Method
    Accepts image format (jpeg, png, ...)
    :param request:
    :return:
    """
    try:
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
                    image.format = 'JPEG'

                picture_model = await manager.add_picture(request=request, image=image,
                                                          image_quality=int(quality) if quality else None)
                image.save(picture_model.picture_path, quality=picture_model.quality if picture_model.quality else 100)

                logging.info(
                    'Save image, id_slack = {} | path = {}'.format(picture_model.id_slack, picture_model.picture_path),
                    extra={'route': request.path_qs,
                           'functionName': inspect.getframeinfo(inspect.currentframe()).function})

                return web.Response(body=picture_model.to_json(), status=201)

            except PIL.UnidentifiedImageError:
                logging.warning('Convert byte to picture failed',
                                extra={'route': request.path_qs,
                                       'functionName': inspect.getframeinfo(inspect.currentframe()).function})
                return web.Response(body=json.dumps({'error_message': 'invalid format file'}), status=400)
            except ZeroDivisionError:
                logging.warning(
                    'Parce parameters failed quality: int={}, x: int={}, y: int={}'.format(quality, width, height),
                    extra={'route': request.path_qs,
                           'functionName': inspect.getframeinfo(inspect.currentframe()).function})
                return web.Response(body=json.dumps({'error_message': 'failed parse parameters'}), status=400)

        logging.error('File not found len(request.content)={}'.format(len(content_data)),
                      extra={'route': request.path_qs,
                             'functionName': inspect.getframeinfo(inspect.currentframe()).function})
        return web.Response(body=json.dumps({'error_message': 'file not found'}), status=400)

    except Exception as _ex:
        logging.error('BaseException', exc_info=True,
                      extra={'route': request.path_qs,
                             'functionName': inspect.getframeinfo(inspect.currentframe()).function})
        raise _ex


async def get_picture(request: web.Request):
    """
    GET Method
    :param request:
    :return:
    """
    try:
        if id_ := request.rel_url.query.get('id'):
            if picture_model := await manager.get_picture(request=request, id_=id_):

                logging.info('Get image id_slack - {}'.format(picture_model.id_slack),
                             extra={'route': request.path_qs,
                                    'functionName': inspect.getframeinfo(inspect.currentframe()).function})

                return web.FileResponse(picture_model.picture_path)

        else:
            logging.warning('Failed search `id` in params ({})'.format(dict(request.rel_url.query)),
                            extra={'route': request.path_qs,
                                   'functionName': inspect.getframeinfo(inspect.currentframe()).function})
            return web.Response(body=json.dumps({'error_message': f'failed parse parameters'}), status=400)
        logging.warning('Failed search `id-{}` in DB'.format(id_),
                        extra={'route': request.path_qs,
                               'functionName': inspect.getframeinfo(inspect.currentframe()).function})
        return web.Response(body=json.dumps({'error_message': f'picture {id_} not found'}), status=400)

    except Exception as _ex:
        logging.error('BaseException', exc_info=True,
                      extra={'route': request.path_qs,
                             'functionName': inspect.getframeinfo(inspect.currentframe()).function})
        raise _ex
