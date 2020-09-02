---
title: "1. TEXT"
date: 2020-07-12 21:11:57 +0900
categories: Python3 StandardLibrary
---
# 1. Text
`str` class는 Python programmer가 사용 할 수 있는 가장 확실한 text 처리 도구지만, standard library에는 간단한 방법으로 고급 text 조작을 할 수 있는 다른 도구가 많다.

application은 문자열을 매개변수로 간단히 사용하고자 `str`객체의 기능을 사용하지 않고 `string`.`Template`을 사용할 수도 있다. python package index에서 제공하는 수 많은 web framework나 확장 module이 정의하는 template만큼 기능이 풍부하지는 않지만, `string`.`Template`은 정적 text에 동적 값을 삽입할 수 있고, 사용자가 어느정도 수정할 수 있는 template이다.

`textwrap` 모듈은 출력되는 문단의 폭을 제한하거나 들여쓰기 추가, 줄 바꿈 문자를 추가해 여러 줄을 보기 좋게 만드는 방법 등을 사용해 text 형식을 맞춰줄 수 있는 도구를 포함한다.

text 비교에 있어 일치 여부나 정렬, 비교 기능이 python에 기본적으로 포함되지만, standard library는 이 기능보다 훨씬 뛰어난 두 module을 제공한다. `re`는 빠른 속도를 위해 C로 구현된 완벽한 정규 표현식 라이브러리다. 정규 표현식은 좀 더 큰 데이터 세트에서 하위 문자열을 검색하거나 다른 고정 문자열보다 복잡한 패턴과 비교하고, 간단한 파싱 작업에 적합하다.

반면 `difflib`는 문자열 추가나 삭제, 변경을 추적한다. `difflib`을 이용한 비교 출력물을 보면 사용자에게 좀 더 자세한 피드백을 제공한다는 것을 알 수 있다. 두 문서를 비교해보면 어디서 변경이 발생하는지 시간별로 문서가 어떻게 변하는지 등을 알 수 있다.

## 1.1 string: 텍스트 상수와 템플릿
`string` 모듈의 기원은 파이썬 초기 버전까지 거슬러 올라간다. 이전에 구현됐던 많은 기능은 `str` 객체로 이관됐다. 하지만 `string` 모듈은 아직도 `str` 객체와 작업에 유용한 일부 상수와 클래스를 갖고 있다. 1장에서는 이 부분을 집중적으로 다룬다.

### 1.1.1 Function
capwords() 함수는 문자열에서 모든 단어의 첫 알파벳을 대문자로 바꿔준다.

`리스트 1.1: string_capwords.py`
```python
import string

s = 'The quick brown fox jumped over the lazy dog.'
print(s)
print(string.capwords(s))
```
실행 결과는 주어진 문자열에 대해 split()을 호출한 후 단어의 첫 글자를 대문자로 바꾸고 다시 이 결과에 join을 호출해 하나의 문자열을 만들어낸 것과 동일하다.
```
$ string_capwords.py

The quick brown fox jumped over the lazy dog.
The Quick Brown Fox Jumped Over The Lazy Dog.
```

### 1.1.2 Template
문자열 템플릿은 PEP 292(www.python.org/dev/peps/pep-0292)의 일환으로 내장된 보간(_built-in interpolation_)문법을 대체할 의도로 추가됐다. string.Template을 사용하면 변수명에 $ 접두어를 추가해 식별할 수 있다. 예를 들어 $var과 같다. 또 다른 방법으로는 필요에 따라 중괄호를 사용해 텍스트를 분리시킬 수 있다. 예를 들면 ${var}와 같다. 다음 예제는 % 연산자를 사용한 유사 문자열 보간을 가진 단순한 템플릿과 str.format()을 사용하는 새로운 문자열 문법을 비교한다.

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
