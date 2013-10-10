import sys
from StringIO import StringIO

from pyterm import CapTerm, DumbTerm


def pytest_funcarg__term(request):
    def create():
        stream = StringIO()
        stream.fileno = lambda : 0 # fake whatever fileno
        term = CapTerm(stream=stream)
        # replace real codes with <code-name>
        for name in term.codes.iterkeys():
            term.codes[name] = '<{}>'.format(name)
        term.codes['NORMAL'] = '<NORMAL>'
        term.codes['DEFAULT'] = '<DEFAULT>'
        term() # flush initial streeam that contains real code
        stream.seek(0)
        stream.truncate(0)
        return term
    return request.cached_setup(setup=create, scope="function")


class TestCapTerm(object):
    def test_init_defaults(self):
        term = CapTerm()
        assert sys.stdout == term.stream
        assert term.codes['NORMAL'] == term.codes['DEFAULT']

    def test_init_params(self):
        my_stream = open('/tmp/xxx', 'w')
        term = CapTerm(stream=my_stream, start_code=[])
        assert my_stream == term.stream
        assert '' == term.codes['DEFAULT']
        assert '' != term.codes['BLUE']

    def test_get_code(self, term):
        assert "<BLUE>" == term['BLUE']
        assert "<UP>" == term['UP']

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

    def test_no_raise(self, term):
        # no way to test this in any significant way
        # if they dont raise an exception they are good enough
        term.cols()
        term.lines()


class TestDumbTerm(object):
    def test_get_term_codes(self):
        my_stream = open('/tmp/xxx', 'w')
        term = DumbTerm(stream=my_stream, start_code=[])
        assert my_stream == term.stream
        assert '' == term.codes['DEFAULT']
        assert '' == term.codes['BLUE']



class TestDemo(object):
    def test_color(self, term):
        term.demo()
