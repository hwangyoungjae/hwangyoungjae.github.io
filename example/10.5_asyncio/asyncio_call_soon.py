# asyncio_call_soon.py
import asyncio
import functools


def callback(arg, *, kwarg='default'):
    print(f"callback invoked with {arg} and {kwarg}")


async def main(loop: asyncio.events.AbstractEventLoop):
    print("registering callbacks")
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwarg='not default')
    loop.call_soon(wrapped, 2)

    await asyncio.sleep(0.1)


event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    event_loop.run_until_complete(main(event_loop))
finally:
    print("closing event loop")
    event_loop.close()
