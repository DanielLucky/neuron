import io
import os
import uuid
from typing import Optional

import asyncpg
from PIL import Image
from aiohttp import web

from app.config import PATH_SAVE_PICTURE
from app.picture.models import Picture


async def add_picture(request: web.Request,
                      image: Image.open,
                      image_quality: int = None) -> Picture:

    byte_image = io.BytesIO()
    image.save(byte_image, format=image.format)

    id_slack = uuid.uuid4()
    path_new_file = os.path.join(PATH_SAVE_PICTURE, f'{id_slack}.{image.format}'.lower())

    async with request.app['db'].acquire() as connection:
        result = await connection.fetch(
            '''
                INSERT INTO 
                picture (id_slack, picture, picture_path, width, height, format, quality) 
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                returning *;
            ''',
            str(id_slack),
            byte_image.getvalue(),
            path_new_file,
            image.width,
            image.height,
            image.format,
            image_quality,
        )

    return Picture(**result[0])


async def get_picture(request: web.Request, id_: str):

    async with request.app['db'].acquire() as connection:
        result = await connection.fetch(
            '''
                SELECT * 
                FROM picture
                WHERE id_slack = $1;
            ''',
            id_
        )

    if result:
        return Picture(**result[0])
