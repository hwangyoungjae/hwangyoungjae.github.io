# asyncio_cancel_task.py
import asyncio


async def task_func():
    print("in task_func")
    return "the result"


async def main(loop: asyncio.events.AbstractEventLoop):
    print("creating task")
    task = loop.create_task(task_func())

    print("canceling task")
    task.cancel()

    print(f"canceled task {task!r}")
    try:
        await task
    except asyncio.CancelledError:
        print("caught error from canceled task")
    else:
        print(f"task result : {task.result()!r}")


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
