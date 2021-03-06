from aiohttp import web

from app.settings import create_app


app = create_app()


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0')
