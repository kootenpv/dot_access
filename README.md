## qdot

qdot will help you quickly dive into data. Either you have a value, or you have a `None`.
This is what you want when you are looking for something convenient like in JavaScript, yet at the same time allow for more Pythonic code.


### Case 0: Hello Dot

```python
from qdot import Dot

d = {"a": 1, "long name": 2}
d = Dot(d)
assert d.a == 1
assert d.a.a.a == None
assert d["long name"] == 2
```

### Case 1: Quick default / ternary

```python
from qdot import Dot

result = Dot(None) or Dot(10)
assert result == 10  # comparison operators have been implemented: no surprises

# and
result = Dot({}).a.a.a.a
result = result if result else 15
assert result == 15
```


### Case 2: Getting data from an API

```python
from qdot import dot

@dot
def get_from_api(arg):
    return {"a": arg}

assert get_from_api(1).a.a.a == None
```

### Setting values

Is not allowed directly

but, it works by having an "original_object".

You only have to do 1 comparison in total:

```python
from qdot import dot

@dot
def get_data_from_api():
    return {"a": {"b": {"c": 1}}}

data = get_data_from_api()
interesting = data.a.b.original_object
if interesting:
    interesting["d"] = 2
    interesting
    {'c': 1, 'd': 2}
data
Dot({'a': {'b': {'c': 1, 'd': 2}}})
```


### JSON Serialization

```python
d = Dot(1)
json.dumps(d.original_object)
json.dumps(Dot(1), default=lambda d: d.original_object)
```

### Bonus: Getting data from a function which might throw

This is probably frowned upon? Caught exceptions will return `Dot(None)`.

```python
from qdot import trydot

@trydot(TypeError)
def return_impossible():
    return {} + []

assert return_impossible() == None
```
