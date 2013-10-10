"""pyterm - terminal output formatting

http://???

Ouput formatting to a terminal with curses capabilities

Curses mode (curses.initwin) is not used.
It controls color, text attributes (bold, inverse,...) and
cursor position.

references:

 * http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
 * http://code.activestate.com/recipes/475116/

The MIT License  (see LICENSE file)
Copyright (c) 2012 Eduardo Naufel Schettino

"""

__version__ = (0, 1, 'dev')



import curses
import sys


# compatibility python2 and python3
if sys.version_info >= (3, 0): # pragma: nocover
    _ = lambda s: s.decode('utf-8')
else:
    _ = lambda s: s


CAPABILITY = [
    # cursor movement
    ('BOL', 'cr'),   # begining of line
    ('UP', 'cuu1'),
    ('DOWN', 'cud1'),
    ('LEFT', 'cub1'),
    ('RIGHT', 'cuf1'),

    # clear
    ('CLEAR_SCREEN', 'clear'),
    ('CLEAR_EOL', 'el'),
    ('CLEAR_EOS', 'ed'), # clear to end of display

    # write mode
    ('BOLD', 'bold'),
    ('REVERSE', 'rev'),
    ('UNDERLINE', 'smul'),
    ('NORMAL', 'sgr0'),

    # colors
    ('A_COLOR', 'setaf'),
    ('A_BG_COLOR', 'setab'),
    ]

ANSI_COLORS = ['BLACK', 'RED', 'GREEN', 'YELLOW',
               'BLUE', 'MAGENTA', 'CYAN', 'WHITE']



class CapTerm(object):
    """Ouput formatting to a terminal with curses capabilities

    @ivar codes: (dict) key: capability-name as exposed by API
                        value: capability-code as understood by curses

    @ivar _buffer: content to be sent to terminal
    """
    def __init__(self, stream=None, start_code=('NORMAL',) ):
        """
        @ivar stream: where the output will be written to (default: sys.stdout)
        @param start_code: sequence of codes to be appended to the
                           end of content on every write.
                           default: []
        """
        self.stream = stream or sys.stdout
        self.codes = self.get_term_codes(self.stream.fileno())
        self.set_style('DEFAULT', start_code)
        self._buffer = _(self['DEFAULT'])


    @staticmethod
    def get_term_codes(fd=None):
        """get capabilities and color codes"""
        curses.setupterm(None, fd)
        codes = dict((name, curses.tigetstr(code)) for name, code in CAPABILITY)
        for index, name in enumerate(ANSI_COLORS):
            codes[name] = curses.tparm(codes['A_COLOR'], index)
            codes['BG_'+name] = curses.tparm(codes['A_BG_COLOR'], index)
        return codes


    def __getitem__(self, key):
        """@return (bytes) code of capability/color
        @param key: (str) capability/color name
        """
        return self.codes[key]

    def __getattr__(self, key):
        """adds attribute code to buffer
        @return self (in order to allow chaining)
        """
        self._buffer += _(self.codes[key])
        return self

    def __call__(self, content='', flush=True):
        """adds given content & default_end to buffer, writes buffer if 'flush
        @return self (in order to allow chaining)
        """
        self._buffer += content + _(self['NORMAL'])
        if flush:
            self.stream.write(self._buffer)
            self._buffer = _(self['DEFAULT'])
        return self

    @staticmethod
    def cols():
        """@return (int) number of columns on terminal window"""
        return curses.tigetnum('cols')

    @staticmethod
    def lines():
        """@return (int) number of lines on terminal window"""
        return curses.tigetnum('lines')

    def set_style(self, name, args):
        """set/create a new capability
        mostly used to create named sequence of codes
        """
        self.codes[name] = b''.join([(self[a]) for a in args])


    # FIXME -m
    # TODO include table with all tested capabilities
    def demo(self):
        """demo colors and capabilities of your terminal """
        for color in ANSI_COLORS:
            getattr(self, color)("%-8s" % color)(' ')
            getattr(self, color).BOLD('bold')(' ')
            getattr(self, color).REVERSE('reverse')(' ')
            getattr(self, color).UNDERLINE('underline')(' ')
            getattr(self, color).BG_YELLOW('bg_yellow')(' ')
            getattr(self, color).UNDERLINE.BOLD('bold+under')(' ')
            self('\n')



class DumbTerm(CapTerm):
    """Same interface as Term but for a stream without any capability"""

    @staticmethod
    def get_term_codes(fd=None):
        """get capabilities and color codes"""
        curses.setupterm(None, fd)
        codes = dict((name, '') for name, _ in CAPABILITY)
        for name in ANSI_COLORS:
            codes[name] = ''
            codes['BG_'+name] = ''
        return codes


class Term(object):
    def __new__(self, stream=None, start_code=('NORMAL',), color=None):
        stream = stream or sys.stdout
        if color is True or (color is None and stream.isatty()):
            return CapTerm(stream, start_code)
        else:
            return DumbTerm(stream, start_code)
