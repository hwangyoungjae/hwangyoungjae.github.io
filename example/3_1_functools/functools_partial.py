# functools_partial.py
import functools


def myfunc(a, b=2):
    """Docstirng for myfunc()."""
    print(f"  called myfunc with: {a} {b}")


def show_details(name, f, is_partial=False):
    """Show details of a callable object."""
    print(f"{name}:")
    print("  object:", f)
    if not is_partial:
        print("  __name__:", f.__name__)
    if is_partial:
        print("  func:", f.func)
        print("  args:", f.args)
        print("  keywordss:", f.keywords)
    return


show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# 'b'의 기본값을 다르게 설정한다.
# 'a'는 호출자가 제공해야 한다.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

# 'a'와 'b' 모두의 기본값을 설정한다.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print()

print("Insufficient arguemtns:")
p1()
