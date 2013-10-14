import sys
try:
    from StringIO import StringIO
except: # pragma: no cover
     # py3
    from io import StringIO

from pyterm import Term, get_codes_curses, get_codes_dumb, get_codes_ansi



def pytest_funcarg__term(request):
    def create():
        stream = StringIO()
        stream.fileno = lambda : 0 # fake whatever fileno
        term = Term(stream=stream)
        # replace real codes with <code-name>
        for name in term.codes.keys():
            if sys.version_info >= (3, 0): # pragma: nocover
                term.codes[name] = bytes('<{}>'.format(name), 'ascii')
            else:
                term.codes[name] = '<{}>'.format(name)
        term.codes['NORMAL'] = b'<NORMAL>'
        term.codes['DEFAULT'] = b'<DEFAULT>'
        term() # flush initial streeam that contains real code
        stream.seek(0)
        stream.truncate(0)
        return term
    return request.cached_setup(setup=create, scope="function")


def test_codes_curses():
    with open('/tmp/xxx', 'w') as my_stream:
        codes = get_codes_curses(my_stream.fileno())
        assert b'\n' == codes['DOWN']
        assert b'\x1b[34m' == codes['BLUE']

def test_codes_dumb():
    codes = get_codes_dumb()
    assert b'' == codes['DOWN']
    assert b'' == codes['BLUE']

def test_codes_ansi():
    codes = get_codes_ansi()
    assert b'\x1b[B' == codes['DOWN']
    assert b'\x1b[34m' == codes['BLUE']


class TestTerm(object):
    def test_init_defaults(self):
        term = Term()
        assert sys.stdout == term.stream
        assert term.codes['NORMAL'] == term.codes['DEFAULT']

    def test_init_params(self):
        with open('/tmp/xxx', 'w') as my_stream:
            term = Term(stream=my_stream, start_code=[])
            assert my_stream == term.stream

    def test_get_codes(self, monkeypatch):
        stream_no_tty = StringIO()
        stream_no_tty.fileno = lambda : 0 # fake whatever fileno
        stream_no_tty.isatty = lambda : False
        tty = StringIO()
        tty.fileno = lambda : 0 # fake whatever fileno
        tty.isatty = lambda : True
        # class used is based on stream being a tty or not
        assert 'curses' == Term(stream=tty).code
        assert 'dumb' == Term(stream=stream_no_tty).code
        # force use of capabilities
        assert 'curses' == Term(stream=tty, use_colors=True).code
        assert 'curses' == Term(stream=stream_no_tty, use_colors=True).code
        # use of ansi codes forced/no curses available
        assert 'ansi' == Term(stream=tty, code='ansi').code
        import curses
        monkeypatch.setattr(curses, 'tparm', lambda : 5/0)
        assert 'ansi' == Term(stream=tty).code

    def test_get_code(self, term):
        assert b"<BLUE>" == term['BLUE']
        assert b"<UP>" == term['UP']

    def test_write_code(self, term):
        assert term == term.BLUE
        assert '<DEFAULT><BLUE>' == term._buffer
        assert '' == term.stream.getvalue()

    def test_write(self, term):
        assert term == term.BLUE('sky')
        assert '<DEFAULT>' == term._buffer
        assert '<DEFAULT><BLUE>sky<NORMAL>' == term.stream.getvalue()

    def test_write_no_flush(self, term):
        assert term == term.BLUE('sky', flush=False)
        assert '<DEFAULT><BLUE>sky<NORMAL>' == term._buffer
        assert '' == term.stream.getvalue()

    def test_set_style(self, term):
        term.set_style('BR', ['BLUE', 'BG_RED'])
        assert '' == term.stream.getvalue()
        term.BR('blue-red')
        assert '<DEFAULT><BLUE><BG_RED>blue-red<NORMAL>' == term.stream.getvalue()

    def test_lines_cols(self, monkeypatch):
        # using curses
        tty = StringIO()
        tty.fileno = lambda : 0 # fake whatever fileno
        tty.isatty = lambda : True
        term = Term(stream=tty)
        assert isinstance(term.cols(), int)
        assert isinstance(term.lines(), int)

        # curses not available gets None
        import curses
        monkeypatch.setattr(curses, 'tigetnum', lambda : 5/0)
        assert None == term.cols()
        assert None == term.lines()

        # uses stty
        term2 = Term(stream=tty, code='ansi')
        assert isinstance(term2.cols(), int)
        assert isinstance(term2.lines(), int)


class TestDemo(object):
    def test_color(self, term):
        term.demo()
