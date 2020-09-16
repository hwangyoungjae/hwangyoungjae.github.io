# string_template_missing.py
import string

values = dict(var='foo')

t = string.Template("$var is here but $missing is not provided")
try:
    print('subtitute()     :', t.substitute(values))
except KeyError as err:
    print("ERROR", str(err))

print('safe_subtitute():', t.safe_substitute(values))
