import aiohttp
from aiohttp import web, ClientSession
from database_connection import DatabaseConnection
from aiojobs.aiohttp import setup, spawn

async def websocket_handler(request):
    """Function that set WebSocket and wait for messages"""
    global ws
    ws = web.WebSocketResponse()

    await ws.prepare(request)

    async for message in ws:
        if message.type == aiohttp.WSMsgType.TEXT:
            if message.data == 'close':
                await ws.close()
            else:
                print(message.data)
                await ws.send_str(message.data)
                
        elif message.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws

async def insert_pokemons_in_database(pokemons):
    database_connection = DatabaseConnection()
    connection = database_connection.connect(r"database.db")
    cursor = connection.cursor()
    for pokemon in pokemons:
        print(pokemon["name"])
        cursor.execute(f'''
            INSERT INTO pokemon (name, url) VALUES(?, ?);
        ''', (pokemon.get("name"), pokemon.get("url")))
        connection.commit()
        print(f"Pokemin wiht ID: {cursor.lastrowid}")
    connection.close()
    await ws.send_str("New Pokemons!")

    
async def store_pokemons(request):
    pokemons = await request.json()
    await spawn(request, insert_pokemons_in_database(pokemons))
    return web.json_response({"success":"true"})

app = web.Application()
app.add_routes([web.post('/pokemon', store_pokemons), web.get('/ws', websocket_handler)])
setup(app)
if __name__ == '__main__':
    database_connection = DatabaseConnection()
    connection = database_connection.connect(r"database.db")
    connection.execute('''CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL
    )''')
    connection.commit()
    connection.close()
    web.run_app(app)