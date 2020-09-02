# asyncio_generator.py
import asyncio


@asyncio.coroutine
def outer():
    print("in outer")
    print("waiting for result1")
    result1 = yield from phase1()
    print("waiting for result2")
    result2 = yield from phase2(result1)
    return result1, result2


@asyncio.coroutine
def phase1():
    print(" - in phase1")
    return "result1"


@asyncio.coroutine
def phase2(arg):
    print(" - in phase2")
    return f"result2 derived from {arg}"


event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print(f"return value : {return_value!r}")
finally:
    event_loop.close()
