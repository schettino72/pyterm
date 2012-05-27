#  py.test --cov pyterm.py --cov test_pyterm.py --cov-report term-missing

import sys
from StringIO import StringIO

from pyterm import Term, demo_capabilities, demo_color


def pytest_funcarg__term(request):
    def create():
        term = Term(stream=StringIO())
        # replace real codes with <code-name>
        for name in term.codes.iterkeys():
            term.codes[name] = '<%s>' % name
        return term
    return request.cached_setup(setup=create, scope="function")


class TestTerm(object):
    def test_init_defaults(self):
        term = Term()
        assert sys.stdout == term.stream
        assert term.codes['NORMAL'] == term.codes['DEFAULT']

    def test_init_params(self):
        term = Term(stream="Fake", default_end=[])
        assert "Fake" == term.stream
        assert '' == term.codes['DEFAULT']

    def test_get_code(self, term):
        assert "<BLUE>" == term['BLUE']
        assert "<UP>" == term['UP']

    def test_write_code(self, term):
        assert term == term.BLUE
        assert '<BLUE>' == term._buffer
        assert '' == term.stream.getvalue()

    def test_write(self, term):
        assert term == term.BLUE('sky')
        assert '' == term._buffer
        assert '<BLUE>sky<DEFAULT>' == term.stream.getvalue()

    def test_write_no_flush(self, term):
        assert term == term.BLUE('sky', flush=False)
        assert '<BLUE>sky<DEFAULT>' == term._buffer
        assert '' == term.stream.getvalue()

    def test_set_style(self, term):
        term.set_style('BR', ['BLUE', 'BG_RED'])
        assert '' == term.stream.getvalue()
        term.BR('blue-red')
        assert '<BLUE><BG_RED>blue-red<DEFAULT>' == term.stream.getvalue()

    def test_no_raise(self, term):
        # no way to test this in any significant way
        # if they dont raise an exception they are good enough
        term.cols()
        term.lines()


class TestDemo(object):
    def test_capability(self, term):
        demo_capabilities(term)
    def test_color(self, term):
        demo_color(term)
