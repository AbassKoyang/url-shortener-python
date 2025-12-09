from http import HTTPStatus
import sqlite3
from aiohttp import web
import validators
import requests

routes = web.RouteTableDef();

async def validate_url_format(url: str):
    return validators.url(url);

async def validate_url(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        response = requests.get(url, headers=headers);
        if response.status_code == HTTPStatus.OK or response.status_code == 503:
            return True;
        return False;
    except Exception as ex:
        print(ex);
        return False;

async def shorten_url(url: str):
    pass

@routes.post('/shorten')
async def shorten(request):
    data = await request.post();
    longUrl = data['url'];
    return web.Response(text=longUrl);

if __name__ == "__main__":
    connection = sqlite3.connect("urlshortener.db");
    cursor = connection.cursor();
    cursor.execute("CREATE TABLE IF NOT EXISTs URLSHORTENER (longurl TEXT, shorturl TEXT, code TEXT unique)")
    app = web.Application();
    app.add_routes(routes);
    web.run_app(app, host="127.0.0.1", port=8000);
