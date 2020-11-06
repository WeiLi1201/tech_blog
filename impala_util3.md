def test_numeric():
    dt("select * from test where int = 1",
       "select * from test where int = :1",
       [1])
    dt("select * from test where str = 'foo'",
       "select * from test where str = :1",
       ["foo"])
    dt("select * from test where flt = 0.123",
       "select * from test where flt = :1",
       [0.123])
    dt("select * from test where nul = NULL",
       "select * from test where nul = :1",
       [None])
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = :1 and str = " +
       ":2 and flt = :3 and nul = :4",
       [1, "foo", 0.123, None])
    # reverse list
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = :4 and str = " +
       ":3 and flt = :2 and nul = :1",
       [None, 0.123, "foo", 1])
    # characters around them
    dt("select * from test where int=1 and str='foo' and " +
       "flt=(0.123) and nul=NULL",
       "select * from test where int=:1 and str=" +
       ":2 and flt=(:3) and nul=:4",
       [1, "foo", 0.123, None])
    # tuple instead of list
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = :1 and str = " +
       ":2 and flt = :3 and nul = :4",
       (1, "foo", 0.123, None))
    # more than 9
    dt("select * from test where a=1 and b=2 and c=3 and d=4 " +
       "and e=5 and f=6 and g=7 and h=8 and i=9 and j=10",
       "select * from test where a=:1 and b=:2 and c=:3 and d=:4 " +
       "and e=:5 and f=:6 and g=:7 and h=:8 and i=:9 and j=:10",
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    dt("select * from test where a='a' and b='b' and c='c' " +
       "and d='d' and e='e' and f='f' and g='g' and h='h' " +
       "and i='i' and j='j' and k='k'",
       "select * from test where a=:1 and b=:2 and c=:3 and " +
       "d=:4 and e=:5 and f=:6 and g=:7 and h=:8 and i=:9 and " +
       "j=:10 and k=:11",
       ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'])


def test_qmark():
    dt("select * from test where int = 1",
       "select * from test where int = ?",
       [1])
    dt("select * from test where str = 'foo'",
       "select * from test where str = ?",
       ["foo"])
    dt("select * from test where flt = 0.123",
       "select * from test where flt = ?",
       [0.123])
    dt("select * from test where nul = NULL",
       "select * from test where nul = ?",
       [None])
    dt("select * from test where int = 1 and str = 'foo' and " +
       "flt = 0.123 and nul = NULL",
       "select * from test where int = ? and str = " +
       "? and flt = ? and nul = ?",
       [1, "foo", 0.123, None])
    # no spaces around =
    # characters around them
    dt("select * from test where int=1 and str='foo' and " +
       "flt=(0.123) and nul=NULL",
       "select * from test where int=? and str=" +
       "? and flt=(?) and nul=?",
       [1, "foo", 0.123, None])
    # tuple instead of list
    dt("select * from test where int=1 and str='foo' and " +
       "flt=0.123 and nul=NULL",
       "select * from test where int=? and str=" +
       "? and flt=? and nul=?",
       (1, "foo", 0.123, None))
    # bad number of bindings
    bad_bindings = [
        ("select * from test where int = ?", []),
        ("select * from test where int = ? or int = ?", [1]),
        ("select * from test where int = ?", [1, 2]),
        ("select * from test where int = ? or int = ? or int = ?",
         [1, 2, 3, 4])]
    for q in bad_bindings:
        with raises(ProgrammingError):
            dt("should have raised exception", q[0], q[1])
