# asyncio_lock.py
import asyncio
import functools


def unlock(lock: asyncio.Lock):
    print("callback releasing lock")
    lock.release()


async def coro1(lock: asyncio.Lock):
    print("coro1 waiting for the lock")
    async with lock:
        print("coro1 acquired lock")
    print("coro1 released lock")


async def coro2(lock: asyncio.Lock):
    print("coro2 waiting for the lock")
    await lock.acquire()
    try:
        print("coro2 acquired lock")
    finally:
        print("coro2 released lock")
    lock.release()


async def main(loop: asyncio.AbstractEventLoop):
    # 공유 락의 생성과 획득
    lock = asyncio.Lock()
    print("acquiring the lock before starting coroutines")
    await lock.acquire()
    print(f"lock acquired: {lock.locked()}")

    # 락을 해제하기 위한 콜백 예약
    loop.call_later(0.1, functools.partial(unlock, lock))

    # 락을 사용하려는 코루틴을 실행
    print("waiting for coroutines")
    await asyncio.wait([coro1(lock), coro2(lock)])


event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
