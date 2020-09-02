# asyncio_coroutine.py
import asyncio


async def coroutine():
    print("in coroutine")


event_loop = asyncio.get_event_loop()
try:
    print("Starting coroutine")
    coro = coroutine()
    print("entering event loop")
    event_loop.run_until_complete(coro)
finally:
    print("closing event loop")
    event_loop.close()
