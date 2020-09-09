# asyncio_condition.py
import asyncio


async def consumer(condition: asyncio.Condition, n):
    async with condition:
        print(f"consumer {n} is waiting")
        await condition.wait()
        print(f"consumer {n} triggered")
    print(f"ending consumer {n}")


async def manipulate_condition(condition: asyncio.Condition):
    print("starting manipulate_condition")

    # consumer의 시작을 잠깐 지연시킨다
    await asyncio.sleep(0.1)

    for i in range(1, 3):
        async with condition:
            print(f"notifying {i} condumers")
            condition.notify(i)
        await asyncio.sleep(0.1)

    async with condition:
        print("notifying remaining consumers")
        condition.notify_all()
    print("ending manupulate_condition")


async def main(loop: asyncio.AbstractEventLoop):
    # 컨디션 생성
    condition = asyncio.Condition()

    # 컨디션을 감시하는 작업 설정
    consumers = [consumer(condition, i) for i in range(5)]

    # 컨디션 변수를 처리하기 위한 작업 예약
    loop.create_task(manipulate_condition(condition))

    # consumer들의 완료를 대기
    await asyncio.wait(consumers)


event_loop = asyncio.get_event_loop()

try:
    result = event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
