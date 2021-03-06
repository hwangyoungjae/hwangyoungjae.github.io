# asyncio_wait.py
import asyncio


async def phase(i):
    print(f"in phase {i}")
    await asyncio.sleep(0.1 * i)
    print(f"done with phase {i}")
    return f"phase {i} result"


async def main(num_phase):
    print("starting main")
    phases = [phase(i) for i in range(num_phase)]
    print("waiting for phases to complete")
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print(f"results: {results!r}")


event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
