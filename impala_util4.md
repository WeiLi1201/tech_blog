def test_format():
    dt("select * from test where int = 1",
       "select * from test where int = %s",
       [1])
    dt("select * from test where str = 'foo'",
       "select * from test where str = %s",
       ["foo"])
    dt("select * from test where flt = 0.123",
       "select * from test where flt = %s",
       [0.123])
    dt("select * from test where nul = NULL",
       "select * from test where nul = %s",
       [None])
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = %s and str = " +
       "%s and flt = %s and nul = %s",
       [1, "foo", 0.123, None])
    # no spaces around =
    # characters around them
    dt("select * from test where int=1 and str='foo' and " +
       "flt=(0.123) and nul=NULL",
       "select * from test where int=%s and str=" +
       "%s and flt=(%s) and nul=%s",
       [1, "foo", 0.123, None])
    # tuple instead of list
    dt("select * from test where int=1 and str='foo' and " +
       "flt=0.123 and nul=NULL",
       "select * from test where int=%s and str=" +
       "%s and flt=%s and nul=%s",
       (1, "foo", 0.123, None))
    # bad number of bindings
    bad_bindings = [
        ("select * from test where int = %s", []),
        ("select * from test where int = %s or int = %s", [1]),
        ("select * from test where int = %s", [1, 2]),
        ("select * from test where int = %s or int = %s or int = %s",
         [1, 2, 3, 4])]
    for q in bad_bindings:
        with raises(ProgrammingError):
            dt("should have raised exception", q[0], q[1])

def test_avoid_substitution():
  """Regression tests for cases where a parameter *should not* be substituted."""
  # Only markers matching the specified paramstyle should be replaced, including
  # if the parameter is embedded in a substituted string.
  dt("select :2, ?, :named from test where a='string' and b='42'",
     "select :2, ?, :named from test where a=%s and b=%s",
     ['string', '42'], paramstyle='format')
  dt("select * from test where a='string :2 ? %s :named' and b='42'",
     "select * from test where a=%s and b=%s",
     ['string :2 ? %s :named', '42'], paramstyle='format')

  dt("select :2, %s, :named from test where a='string' and b='42'",
     "select :2, %s, :named from test where a=? and b=?",
     ['string', '42'], paramstyle='qmark')
  dt("select * from test where a='string :2 ? %s :named' and b='42'",
     "select * from test where a=? and b=?",
     ['string :2 ? %s :named', '42'], paramstyle='qmark')

  dt("select ?, %s, :named from test where a='string' and b='42'",
     "select ?, %s, :named from test where a=:1 and b=:2",
     ['string', '42'], paramstyle='numeric')
  dt("select * from test where a='string :2 ? %s :named' and b='42'",
      "select * from test where a=:1 and b=:2",
     ['string :2 ? %s :named', '42'], paramstyle='numeric')

  # BUG: %s picks up named parameters as stringified dict when dict is passed.
  dt('select ?, {\'x\': "\'string\'"}, :1 from test where a=\'string\'',
     "select ?, %s, :1 from test where a=:x",
     {'x': 'string'}, paramstyle='named')
  dt("select * from test where a='string :2 ? %s :named' and b='42'",
      "select * from test where a=:x and b=:y",
      {'x': 'string :2 ? %s :named', 'y':'42'}, paramstyle='named')

  # BUG: if a parameter is substituted with a string containing another parameter
  # specifier, double substitution can occur.
  dt("select * from test where a='string '42'' and b='42'",
     "select * from test where a=%s and b=%s",
     ['string :2', '42'])

def test_date_type():
    import datetime
    today = datetime.date(2016, 5, 7)
    query = 'select %(today)s'
    dt("select '2016-05-07'", query, {'today': today})

    today = datetime.datetime(2016, 5, 7, 12, 0)
    query = 'select %(today)s'
    dt("select '2016-05-07 12:00:00'", query, {'today': today})


def test_bad_argument_type():
    with raises(ProgrammingError):
        _bind_parameters("select * from test", 1)
    with raises(ProgrammingError):
        _bind_parameters("select * from test", "a")

def test_marker_replacement():
    dt("select * from test where x = '%s'",
       "select * from test where x = %s",
       [r'%s'])

```
### 参考

 [1]: [https://github.com/mkleehammer/pyodbc/issues/431](https://github.com/cloudera/impyla/issues/213)
 [2]: [https://github.com/cloudera/impyla/issues/213](https://github.com/cloudera/impyla/issues/213)
