# asyncio_event.py
import asyncio
import functools


def set_event(event: asyncio.Event):
    print("setting event in callback")
    event.set()


async def coro1(event: asyncio.Event):
    print("coro1 waiting for event")
    await event.wait()
    print("coro1 triggered")


async def coro2(event: asyncio.Event):
    print("coro2 waiting for event")
    await event.wait()
    print("coro2 triggered")


async def main(loop: asyncio.AbstractEventLoop):
    # 공유 이벤트 생성
    event = asyncio.Event()
    print(f"event start state: {event.is_set()}")

    loop.call_later(0.1, functools.partial(set_event, event))

    await asyncio.wait([coro1(event), coro2(event)])
    print(f"event end state: {event.is_set()}")


event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
