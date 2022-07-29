import aiohttp
import asyncio
import json
from aiohttp import ClientSession

async def websocket():
    session = ClientSession()
    async with session.ws_connect('http://127.0.0.1:8080/ws') as ws:
        await ws.send_str("aaaaaa")
        async for message in ws:
            if message.type == aiohttp.WSMsgType.TEXT:
                    print(message.data)
            elif message.type == aiohttp.WSMsgType.CLOSED:
                print("ws is closed")
                break
            elif message.type == aiohttp.WSMsgType.ERROR:
                print(message)
                break

async def get_pokemons():
    """Get the pokemons from PokeAPI and send it to server"""

    async with aiohttp.ClientSession() as session:
        pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
        server_url = "http://127.0.0.1:8080/pokemon"
        async with session.get(pokemon_url) as pokemon_response:
            print("Status:", pokemon_response.status)
            if pokemon_response.ok:
                response_in_json = await pokemon_response.json()
                print("Pokemon's Count:", response_in_json.get("count"))
                results = response_in_json.get("results", [])
                results_in_bytes = json.dumps(results, indent=2).encode('utf-8')
                async with session.post(server_url, data=results_in_bytes) as server_response:
                    if server_response.ok:
                        print("Saving pokemons...")
                    else:
                        print("Can't save pokemons at server")
            else:
                print("Can't get pokemons")

async def main():
    """Main function where tasks ared defined"""
    websocket_task = asyncio.create_task(websocket())
    get_pokemons_task = asyncio.create_task(get_pokemons())
    await asyncio.gather(websocket_task, get_pokemons_task)
    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
# asyncio.run(main())
