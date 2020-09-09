# asyncio_wait_timeout.py
import asyncio


async def phase(i):
    print(f"in phase {i}")
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print(f"phase {i} canceled")
        raise
    else:
        print(f"done with phase {i}")
        return f"phase {i} result"


async def main(num_phases):
    print("starting main")
    phases = [phase(i) for i in range(num_phases)]
    print("waiting 0.1 for phases to complete")
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print(f"{len(completed)} completed and {len(pending)} pending")
    # 남아있는 작업들이 완료되지 않은 채 종료될 때 에러를 발생하지 않게 남은 작업들을 취소한다.
    if pending:
        print("canceling tasks")
        for t in pending:
            t.cancel()
    print("exiting main")


event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
