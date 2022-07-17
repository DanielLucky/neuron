# настраиваем пути, которые будут вести к нашей странице
from aiohttp import web

from app.picture import views


def picture_routes(app: web.Application):
    app.router.add_post("/", views.post_picture)
    app.router.add_get("/", views.get_picture)
