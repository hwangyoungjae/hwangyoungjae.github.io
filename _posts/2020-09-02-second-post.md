---
title: "1. TEXT"
date: 2020-07-12 21:11:57 +0900
categories: Python3 StandardLibrary 10.5 asyncio: 비동기적 I/O, 이벤트 루프, 병렬 작업 도구
---

## 10.5 asyncio: 비동기적 I/O, 이벤트 루프, 병렬 작업 도구
`asyncio` 모듈은 coroutine을 사용해 병렬 작업 어플리케이션을 만들기 위한 도구를 제공한다. `threading` 모듈은 스레드를 통해 동시성을 구현하고, `multiprocessing`은 시스템 프로세스를 사용해 동시성을 구현하는 반면 `asyncio`는 어플리케이션의 각 부분이 협력해 최적의 시간에 명확하게 작업을 전환하도록 단일 스레드 단일 프로세스 방식을 사용한다. 대부분의 경우 이런 콘텍스트 전환은 데이터를 읽거나 쓰고자 대기하는 동안 프로그램이 블로킹을 할 때 발생하지만, `asyncio`는 시스템 시그널을 처리하거나 어떤 이유로 어플리케이션이 작업 중인 내용을 변경해야 하는 이벤트를 인식하게 하고자 하나의 코루틴이 다른 프로세스들의 완료를 기다리게 미래의 특정 시간에 코드가 실행되도록 예약하는 것도 지원한다.



### 10.5.1 비동기적 병렬 처리의 개념

다른 동시성 모델을 사용하는 대부분의 프로그램은 선형적으로 작성되며, 적절하게 콘텍스트를 변경하고자 해당 언어의 런타임이나 운영체제의 스레드 또는 프로세스 관리에 의존한다. `asyncio` 기반 어플리케이션은 명시적으로 콘텍스트 변경을 처리하는 코드가 있어야 하며, 이 기술을 올바르게 사용하려면 몇 가지 관련된 개념을 이해할 필요가 있다.

`asyncio`가 제공하는 프레임워크는 I/O 이벤트, 시스템 이벤트, 어플리케이션 콘텍스트 변경을 효율적으로 처리하는 객체인 이벤트 루프에 중점을 두고 있다. 다양한 루프 구현이 제공되므로 운영체제의 가용성에 따라 이점을 활용할 수 있다. 적정한 기본값이 자동으로 선택되지만 어플리케이션에서 특정 이벤트 루프 구현을 선택할 수도 있다. 예를 들어 일부 루프 클래스가 네트워크 I/O에서 어느 정도의 효율성을 희생하는 대신에 외부 프로세스에 대한 지원을 추가하는 윈도우에서 매우 유용하다.

어플리케이션은 이벤트 루프와 명시적으로 상호작용을 하면서 실행할 코드를 등록하고, 리소스가 가용할 때 이벤트 루프가 필요한 어플리케이션 코드를 호출하게 한다. 예를 들어 네트워크 서버는 소켓을 열고 소켓에서 입력 이벤트가 발생했을 때 알림을 받고자 소켓을 등록한다. 새로 들어오는 연결이 설정됐거나 데이터를 읽을 수 있을 때 이벤트 루프는 서버 코드에게 이를 알린다. 어플리케이션 코드는 현재 콘텍스트에서 수행할 작업이 더 이상 없으면 잠깐 후에 제어를 넘겨 준다. 예를 들어 소켓에 읽을 데이터가 더 이상 없으면 서버는 이벤트 루프에 제어를 돌려준다.

이벤트 루프에 제어를 돌려주는 메커니즘은 자신의 상태를 잃지 않으면서 호출자에서 제어를 양도하는 특수한 함수인 파이썬 코루틴에 달려 있다. 코루틴은 생성자 함수와 매우 비슷한다. 실제로 파이썬 3.5 이전 버전에서 생성자는 코루틴 객체에 대한 지원을 하는 것이 아니라 코루틴을 구현하는데 사용할 수 있었다. 또한 `asyncio`는 코루틴을 직접 작성하는 대신 콜백을 사용해 코드를 작성할 수 있는 프로토콜 계층 및 전송 계층의 클래스 기반 추상 계층을 제공한다. 클래스 기반 모델과 코루틴 모델 두 가지 모두에서 이벤트 루프 재진입으로 인한 명시적인 콘텍스트 변경은 파이썬의 스레딩 구현에서의 암시적인 콘텍스트 변경을 대체한다.
`Future`는 아직 완료되지 않은 작업의 결과를 나타내는 자료 구조다. 이벤트 루프는 future객체가 완료되는 것을 감시할 수 있기 때문에 어플리케이션의 한 부분을 다른 부분들이 작업을 끝낼 때까지 기다리게 한다. future외에도 `asyncio`는 락이나 세마포어와 같은 기본적인 동시성 도구를 포함한다.

task는 코루틴의 실행을 래핑하고 관리하는 future의 서브 클래스다. 이벤트 루프는 필요한 리소스가 가용할 때 실행돼 다른 코루틴에 의해 사용될 수 있는 결과를 생성하도록 task를 예약한다.



### 10.5.2 코루틴과 협업 멀티태스킹
코루틴은 병렬 처리를 위해 설계된 언어 구조다. 코루틴 함수는 호출될 때 코루틴 객체를 생성하며, 호출자는 코루틴의 send() 메서드를 사용해 함수의 코드를 실행할 수 있다. 코루틴은 다른 코루틴과 함께 await 키워드를 사용해 해당 객체의 실행을 일시 중지시킬 수 있다. 일시 중지된 동안에도 코루틴의 상태는 유지돼 나중에 깨어나면 중지된 지점부터 나머지를 실행한다.



#### 10.5.2.1 코루틴 시작
`asyncio` 이벤트 루프는 여러 가지 방법으로 코루틴을 시작할 수 있다. 가장 간단한 방법은 코루틴을 run_until_coplete() 메서드에 직접 전달하는 것이다.

```python
# asyncio_coroutine.py
import asyncio

async def coroutine():
    print("in coroutine")

event_loop = asyncio.get_event_loop()
try:
    print("Starting coroutine")
    coro = coroutine()
    print("entering event loop")
    event_loop.run_until_complete(coro)
finally:
    print("closing event loop")
    event_loop.close()
```

첫번째 단계는 이벤트 루프에 대한 참조를 얻는 것이다. 기본 루프 타입을 사용하거나 특정 루프 클래스를 인스턴스화 할 수 있다. 이 예제에서는 기본 루프를 사용했다. run_until_complete() 메서드는 코루틴 객체와 함께 루프를 시작하고, 코루틴이 종료될 때 루프를 멈춘다.

```
$ python38 asyncio_coroutine.py
Starting coroutine
entering event loop
in coroutine
closing event loop
```



#### 10.5.2.2 코루틴의 값 반환

코루틴의 반환값은 코루틴의 시작과 대기를 위한 코드에서 되돌려 받는다.

```python
# asyncio_coroutine_return.py
import asyncio

async def coroutine():
    print("in coroutine")
    return 'result'

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(coroutine())
    print(f"it returned : {return_value!r}")
finally:
    event_loop.close()
```

이 경우 run_until_complete()이 코루틴의 결과를 반환한다.

```
$ python38 asyncio_coroutine_return.py
in coroutine
it returned : 'result'
```



#### 10.5.2.3 코루틴 체인

하나의 코루틴은 다른 코루틴을 시작하고 결과를 기다릴 수 있기 때문에 이를 이용하면 작업을 재사용 가능한 조각으로 분해하기 쉬워진다. 다음 예제는 순차적으로 실행해야 하는 두 개의 단계를 갖고 있지만 이 둘은 동시에 실행될 수 있다.

```python
# asyncio_coroutine_chain.py
import asyncio

async def outer():
    print("in outer")
    print("waiting for result1")
    result1 = await phase1()
    print("waiting for result2")
    result2 = await phase2(result1)
    return result1, result2

async def phase1():
    print(" - in phase1")
    return "result1"

async def phase2(arg):
    print(" - in phase2")
    return f"result2 derived from {arg}"

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print(f"return value : {return_value!r}")
finally:
    event_loop.close()
```

await 키워드는 루프에 새 코루틴을 추가하는 대신 사용한다. 제어 흐름은 이미 루프에 의해 관리되는 코루틴 내부에 있기 때문에 루프에게 새 코루틴을 관리하라고 지시할 필요가 없다.

```
$ python38 asyncio_coroutine_chain.py
in outer
waiting for result1
 - in phase1
waiting for result2
 - in phase2
return value : ('result1', 'result2 derived from result1')
```



#### 10.5.2.4 코루틴 대신 생성자 사용

코루틴 함수는 `asyncio` 의 핵심 구성 요소다. 코루틴 함수는 프로그램 일부의 실행을 중지시키고 해당 호출의 상태를 유지하며 나중에 해당 상태로 재진입하기 위한 언어 구조를 제공한다. 이런 모든 동작은 동시성 프레임워크에서 매우 중요한 능력이다.

파이썬 3.5는 async def 를 사용해 코루틴을 정의하고 await를 사용해 제어를 내어주는 새로운 기능을 도입했으므로 이곳의 asyncio 관련 예제들은 이 새로운 기능을 활용한다. 파이썬 3의 초기 버전들은 asyncio.coroutine() 데코레이터로 래핑된 생성자 함수와 yield from을 사용해 동일한 효과를 얻을 수 있다.

```python
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
```

이 예제는 코루틴 대신 생성자 함수를 사용해 async_coroutine_chain.py를 재현한다.

```
$ python38  asyncio_generator.py
in outer
waiting for result1
 - in phase1
waiting for result2
 - in phase2
return value : ('result1', 'result2 derived from result1')
```



### 10.5.3 정규 함수 호출 예약

코루틴과 I/O 콜백 외에도 `asyncio` 이벤트 루프는 루프 내에서 유지되는 타이머를 기반으로 정규 함수에 대한 호출을 예약할 수 있다.



#### 10.5.3.1 콜백 Soon 예약

콜백의 시점이 중요하지 않다면 call_soon() 을 사용해 루프의 다음번 회차에 호출을 예약할 수 있다. 함수명 뒤에 오는 모든 인자는 콜백이 호출 될 때 콜백에 전달된다. 콜백에 키워드 인자를 전달할 때는 `functools` 모듈의 partial()을 사용한다.

```python
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

```

콜백은 예약된 순서대로 호출된다.

```
$ python38 asyncio_call_soon.py
entering event loop
registering callbacks
callback invoked with 1 and default
callback invoked with 2 and not default
closing event loop
```



#### 10.5.3.2 지연시간을 갖는 콜백 예약

일정 시간동안 콜백 호출을 연기하려면 call_later() 를 사용한다. 이 메서드의 첫번째 인자는 지연시키고자 하는 초 단위 시간이며, 두번째 인자는 콜백이다.

```python
# asyncio_call_later.py
import asyncio

def callback(n):
    print(f"callback {n} invoked")

async def main(loop: asyncio.events.AbstractEventLoop):
    print("registering callbacks")
    loop.call_later(0.2, callback, 1)
    loop.call_later(0.1, callback, 2)
    loop.call_soon(callback, 3)

    await asyncio.sleep(0.4)

event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    event_loop.run_until_complete(main(event_loop))
finally:
    print("closing event loop")
    event_loop.close()

```

이 예제에서는 동일한 콜백 함수가 서로 다른 인자와 함께 여러 번 다른 시간에 예약된다. call_soon()을 사용한 마지막 인스턴스는 시간 예약된 다른 인스턴스들이 발생하기 전에 인자 3으로 콜백을 호출하는데, 이를 통해 soon이 아주 짧은 지연시간을 나타냄을 알 수 있다.

```
$ python38 asyncio_call_later.py
entering event loop
registering callbacks
callback 3 invoked
callback 2 invoked
callback 1 invoked
closing event loop
```



#### 10.5.3.3 콜백을 특정 시간으로 예약

```python
# asyncio_call_at.py
import asyncio
import time

def callback(n, loop):
    print(f"callback {n} invoked at {loop.time()}")

async def main(loop: asyncio.events.AbstractEventLoop):
    now = loop.time()
    print(f"clock time : {time.time()}")
    print(f"loop time  : {now}")

    print("registering callbacks")
    loop.call_at(now + 0.2, callback, 1, loop)
    loop.call_at(now + 0.1, callback, 2, loop)
    loop.call_soon(callback, 3, loop)

    await asyncio.sleep(1)

event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    event_loop.run_until_complete(main(event_loop))
finally:
    print("closing event loop")
    event_loop.close()
```

루프에 따르는 시간은 time.time()이 반환하는 값과 일치하지 않는다.

```
$ python38 asyncio_call_at.py
entering event loop
clock time : 1599034919.75954
loop time  : 0.075539773
registering callbacks
callback 3 invoked at 0.075638149
callback 2 invoked at 0.176595721
callback 1 invoked at 0.277277437
closing event loop
```

### 10.5.4 비동기적으로 결과 생성

Future는 아직 완료되지 않은 작업의 결과를 나타낸다. 이벤트 루프는 작업 완료 여부를 표시하는 `Future` 객체의 상태를 감시하기 때문에 다른 부분들이 작업을 완료할 때까지 어플리케이션의 한 부분을 기다리게 할 수 있다.



#### 10.5.4.1 Future에 대한 대기

`Future`는 코루틴처럼 동작하므로 완료 여부를 표시하는 등의 코루틴에서 사용되는 기법을 `Future`에서도 사용할 수 있다. 다음 예제는 이벤트 루프의 run_until_complete() 메서드에 future를 전달한다.

```python
# asyncio_futre_event_loop.py
import asyncio

def mark_done(future: asyncio.Future, result):
    print(f"setting future result to {result!r}")
    future.set_result(result)

event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    print("scheduling mark_done")
    event_loop.call_soon(mark_done, all_done, 'the result')

    print("entering event loop")
    result = event_loop.run_until_complete(all_done)
    print(f"returned result {result!r}")
finally:
    print("closing event loop")
    event_loop.close()

print(f"future result : {all_done.result()!r}")

```

set_result() 가 호출되면 `Future`의 상태는 완료로 변경되며, `Future` 인스턴스는 나중에 사용하고자 메서드에 주어진 결과를 유지한다.

```
$ python38 asyncio_futre_event_loop.py
scheduling mark_done
entering event loop
setting future result to 'the result'
returned result 'the result'
closing event loop
future result : 'the result'
```



또한 `Future` 는 다음 예제처럼 await 키워드와 함께 사용할 수 있다.

```python
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

```

`Future` 의 결과는 await에 의해 반환되므로, 종종 코루틴과 Future 인스턴스에 동일한 코드를 사용할 수 있다.

```
$ python38 asyncio_future_await.py
scheduling mark_done
setting future result to 'the result'
returned result 'the result'
```









