from dot_access import Dot

d = {"a": 1, "long name": 2}
d = Dot(d)
assert d.a == 1
assert d.a.a.a == None
assert d["long name"] == 2
