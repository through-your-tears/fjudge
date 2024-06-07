from aiohttp import web
from aiohttp_cors import setup, ResourceOptions


app = web.Application()
urls = [

]
app.add_routes(urls)
cors = setup(app, defaults={
    '*': ResourceOptions(
        allow_credentials=True,
        expose_headers='*',
        allow_headers='*',
        allow_methods='*'
    )
})
for route in list(app.router.routes()):
    cors.add(route)
web.run_app(app)
