# 16장 개발자 도구

시간이 지나면서 python은 처음부터 모든 것을 구축해야 하는 필요성을 없애고 파이썬 개발자의 삶을 좀 더 편안하게 만들어주고자 광범위한 module 생태계를 발전시켰다. 개발자가 작업에 사용하는 도구에도 동일한 철학이 적용돼 왔다. 16장에서는 test, debugging, profiling 등과 같이 일반적인 개발 작업에 도움을 주는 python module을 다룬다.

개발자를 위한 가장 기본적인 형태의 도움말은 code 문서다. `pydoc`은 import 가능한 모든 source code에 포함된 docstring에서 형식화된 reference 문서를 생성한다.

python은 자동으로 code를 실행하고 올바르게 동작하는지 검증할 수 있는 두가지 testing framework를 제공한다. `doctest`는 source 내에 또는 단일 file로 문서에 포함된 예제에서 test scenario를 추출한다. `unittest`는 fixture, 사전 정의된 test suite, test discovery 등을 지원하는 다기능의 자동화된 testing framework다.

`trace`는 python의 program 실행을 monitoring하고 각 줄이 몇 번 수행됐는지 보고한다. 이 정보는 자동화된 test suite가 test를 못하고 놓친 code를 찾거나, module간의 dependency를 알고자 function call graph를 연구할 때 사용할 수 있다.

test를 작성하고 실행하면 대부분의 program에서 문제가 발견된다. python에서 처리되지 않은 error는 traceback으로 console에 출력되므로 debugging하기 쉽다. program이 text console 환경에서 실행되지 않았다면 traceback을 사용해 log file이나 message 대화상자에 비슷한 결과를 출력할 수 있다. 표준 traceback의 정보가 부족하다면 `cgitb`를 사용해 각 stack별, source context별 local variable 설정과 같은 상세 정보를 볼 수 있다. 또한 `cgitb`는 web application에서 error를 보고하고자 traceback을 HTML로 형식화할 수 있다.

문제의 위치가 확인된 다음에 `pdb`의 interactive debugger를 통해 code를 단계별로 실행하면 코드가 어떻게 에러 상황에 이르렀는지 알 수 있으므로 쉽게 해결책을 이끌어낼 수가 있다. 또한 이 module은 실제 객체와 code를 사용해 변경사항을 실험할수 있으므로 error가 없는 최종 수정안을 찾을때까지 필요한 반복 횟수를 줄일수 있다.

program이 test되고 debugging된 후에 제대로 동작한다면 그 다음 단계는 performance을 향상시키는 것이다. `profile`과  `timeit`을 사용해 개발자는 program의 속도를 측정하고 느린 부분을 찾아 성능을 향상 시킬수 있다.

공백도 구문의 일부인 python에서는 source code에서 들여쓰기를 일관되게 사용하는 것이 중요하다. `tabnanny`은 모호한 들여쓰기를 알려주는 scanner를 제공한다. 이 module은 code를 repository에 올리기 전에 code가 최소한의 표준을 만족시키는지 확인하고자 사용할 수 있다.

python program은 interpreter가 원본 program source의 byte compile version을 실행한다. byte compile version은 필요에 따라 그때그때 생성하거나 program을 package로 만들 때 한번에 생성할 수 있다. `compileall`은 byte code file을 생성하고자 설치 program과 packaging 도구가 사용하는 interface를 제공한다. 또한 이 module은 개발 환경에서 source file에 syntax error가 있는지 확인하거나 program을 release 할때 packaging 할 byte compile file을 build하고자 사용할수 있다.

source code level에서 `pyclbr`은 text editor나 다른 program이 python source를 scan해 function나 class와 같은 특정 symbol을 찾을때 사용할수 있는 class browser를 제공한다. 이때 code를 import하지 않으므로 부작용이 발생할 가능성도 거의 없다.

`venv`에 의해 관리되는 python 가상 환경은 package를 설치하고 program을 실행하고자 따로 분리된 환경을 말한다. 가상 환경은 동일한 program을 다양한 version에서 쉽게 test하고 dependency conflict가 있는 서로 다른 program을 한 컴퓨터에 설치할 수 있게 해준다.

Expansion module, Framework, Python package index를 통해 사용할수 있는 도구 등 거대한 python 생태계를 활용하려면 package installer가 필요하다. python의 package installer인 `pip`은 interpreter 함께 배포되지 않는다. 이는 개발 도구의 일반적인 update 주기에 비해 개발 언어의 release 주기가 길기 때문이다. `ensurepip`은 최신 버전의  `pip` 를 설치해준다.

{% include list.liquid all=true %}
