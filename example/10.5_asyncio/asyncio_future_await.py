# asyncio_future_await.py
import asyncio


def mark_done(future: asyncio.Future, result):
    print(f"setting future result to {result!r}")
    future.set_result(result)


async def main(loop: asyncio.events.AbstractEventLoop):
    all_done = asyncio.Future()

    print("scheduling mark_done")
    loop.call_soon(mark_done, all_done, 'the result')

    result = await all_done
    print(f"returned result {result!r}")


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
