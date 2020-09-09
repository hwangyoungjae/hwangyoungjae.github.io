# asyncio_queue.py
import asyncio


async def consumer(n, q: asyncio.Queue):
    print(f"consumer {n}: starting")
    while True:
        print(f"consumer {n}: waiting for item")
        item = await q.get()
        print(f"consumer {n}: has item {item}")
        if item is None:
            # None은 멈추라는 시그널
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
        q.task_done()
    print(f"consumer {n}: ending")


async def producer(q: asyncio.Queue, num_workers):
    print("producer: starting")
    # 작업을 시뮬레이션하고자 큐에 몇 개의 수를 추가
    for i in range(num_workers * 3):
        await q.put(i)
        print(f"producer: added task {i} to the queue")
    # consumer들에게 종료 시그널을 주고자 큐에 None 항목 추가
    for i in range(num_workers):
        await q.put(None)
    print("producer: waiting for queue to empty")
    await q.join()
    print("producer: ending")


async def main(loop: asyncio.AbstractEventLoop, num_consumers):
    # 고정된 크기의 큐를 생성해 consumer가 항목을 추출할 때까지 producer 가 블로킹한다.
    q = asyncio.Queue(maxsize=num_consumers)

    # consumer 작업 예약
    consumers = [loop.create_task(consumer(i, q)) for i in range(num_consumers)]

    # producer 작업 예약
    prod = loop.create_task(producer(q, num_consumers))

    # 모든 코루틴이 완료될 때까지 대기
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()

try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()
