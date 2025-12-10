import base64
from http import HTTPStatus
import sqlite3
from aiohttp import web
import validators
import requests

app = web.Application();
routes = web.RouteTableDef();
API_URL = 'http://127.0.0.1:8000';

app.add_routes(routes);


connection = sqlite3.connect("urlshortener.db");
cursor = connection.cursor();
cursor.execute("CREATE TABLE IF NOT EXISTS URLSHORTENER (id INTEGER PRIMARY KEY AUTOINCREMENT, longurl TEXT, shorturl TEXT, code TEXT unique)")

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def base62_encode(number: int) -> str :
    if number == 0:
        return BASE62_ALPHABET[0];

    base62 = ""
    while number > 0:
        number, remainder = divmod(number, 62);
        base62 = BASE62_ALPHABET[remainder] + base62;
    return base62;

def base62_decode(base62_str: str) -> int:
    number = 0
    for char in base62_str:
        value = BASE62_ALPHABET.index(char);
        number = number * 62 + value;
    return number;

encoded = base62_encode(125)
print(encoded)

decoded = base62_decode('21')
print(decoded)  

def validate_url_format(url: str):
    return validators.url(url);

def validate_url(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        response = requests.get(url, headers=headers);
        if response.status_code == HTTPStatus.OK or response.status_code == 503:
            return True;
        return False;
    except Exception as ex:
        print(ex);
        return False;

def shorten_url(url: str):
    short_url = '';
    try:
        cursor.execute("INSERT INTO URLSHORTENER (longurl) VALUES (?)",(url,))
        row_id = cursor.lastrowid
        code = base62_encode(row_id)
        short_url = API_URL + '/' + code;
        cursor.execute(
        "UPDATE URLSHORTENER SET code = ?, shorturl = ? WHERE id = ?",
        (code, short_url, row_id))
        connection.commit();
        return short_url;
    except Exception as ex:
        print(ex);

@routes.post('/shorten')
async def shorten(request):
    data = await request.post();
    longUrl = data['url'];
    if validate_url_format(longUrl) and validate_url(longUrl):
        short_url =  shorten_url(longUrl);
        return web.json_response({
            "success": True,
            "data": {
                "url": short_url
            }
        });
    else:
        return web.json_response({"success": False, "message": 'Invalid url' })
        
@routes.get("/{code}")
async def redirect_to_long_url(request):
    code = request.match_info["code"]
    result = cursor.execute(
        "SELECT longurl FROM URLSHORTENER WHERE code = ?", (code,)
    ).fetchone()

    if result:
        return web.HTTPFound(result[0])
    else:
        return web.Response(text="URL not found", status=404)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000));
    web.run_app(app, host="0.0.0.0", port=port);
