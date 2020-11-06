## 如何写 impyla executemany 批量执行语法
以下代码是官方的例子，认真看看你就会了。  路径:/impala/test/test_query_parameters

```python
from pytest import raises

from impala.interface import _bind_parameters
from impala.dbapi import ProgrammingError


def dt(expected, query, params, **kwargs):
    result = _bind_parameters(query, params, **kwargs)
    assert expected == result


def test_pyformat():
    # technically these tests shouldn't need the full sql query
    # syntax, but it makes it easier to show how the formats are
    # used
    dt("select * from test where int = 1",
       "select * from test where int = %(int)s",
       {'int': 1})
    dt("select * from test where str = 'foo'",
       "select * from test where str = %(str)s",
       {'str': "foo"})
    dt("select * from test where flt = 0.123",
       "select * from test where flt = %(flt)s",
       {'flt': 0.123})
    dt("select * from test where nul = NULL",
       "select * from test where nul = %(nul)s",
       {'nul': None})
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = %(int)s and str = " +
       "%(str)s and flt = %(flt)s and nul = %(nul)s",
       {'int': 1, 'str': "foo", 'flt': 0.123, 'nul': None})
    # Make sure parameters are not replaced twice
    dt("select * from test where a=':b' and b=':c' and c=':a'",
       "select * from test where a=%(a)s and b=%(b)s and c=%(c)s",
       {'a': ":b", 'b': ":c", 'c': ":a"})
    # Unused parameters should be fine
    dt("select * from test where a=1",
       "select * from test where a=1",
       {'unused': 3})
    # But nonexistent should not
    with raises(KeyError):
        dt("select * from test where int = 1",
           "select * from test where int = %(nosuchkeyword)s",
           {'wrong': 1})


def test_named():
    dt("select * from test where int = 1",
       "select * from test where int = :int",
       {'int': 1})
    dt("select * from test where str = 'foo'",
       "select * from test where str = :str",
       {'str': "foo"})
    dt("select * from test where flt = 0.123",
       "select * from test where flt = :flt",
       {'flt': 0.123})
    dt("select * from test where nul = NULL",
       "select * from test where nul = :nul",
       {'nul': None})
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = :int and str = " +
       ":str and flt = :flt and nul = :nul",
       {'int': 1, 'str': "foo", 'flt': 0.123, 'nul': None})
    # Characters around keywords
    dt("select * from test where int=(1) and str='foo' and " +
       "flt=0.123 and nul=NULL",
       "select * from test where int=(:int) and str=" +
       ":str and flt=:flt and nul=:nul",
       {'int': 1, 'str': "foo", 'flt': 0.123, 'nul': None})
    # Partially overlapping names
    dt("select * from test where a=1 and b=2 and c=3",
       "select * from test where a=:f and b=:fo and c=:foo",
       {'f': 1, 'fo': 2, 'foo': 3})
    dt("select * from test where a=1 and b=2 and c=3",
       "select * from test where a=:foo and b=:fo and c=:f",
       {'foo': 1, 'fo': 2, 'f': 3})
    # Make sure parameters are not replaced twice
    dt("select * from test where a=':b' and b=':c' and c=':a'",
       "select * from test where a=:a and b=:b and c=:c",
       {'a': ":b", 'b': ":c", 'c': ":a"})
    with raises(KeyError):
        dt("select * from test where int = 1",
           "select * from test where int = :nosuchkeyword",
           {'wrong': 1})
