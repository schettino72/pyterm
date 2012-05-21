# references
# http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
# http://code.activestate.com/recipes/475116/


import curses
import sys


# compatibility python2 and python3
if sys.version_info >= (3,0):
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


def get_term_codes():
    """get capabilities and color codes"""
    curses.setupterm()
    codes = dict((name, curses.tigetstr(code)) for name, code in CAPABILITY)
    for index, name in enumerate(ANSI_COLORS):
        codes[name] = curses.tparm(codes['A_COLOR'], index)
        codes['BG_'+name] = curses.tparm(codes['A_BG_COLOR'], index)
    return codes


class Term(object):
    def __init__(self, stream=None, default=('NORMAL',)):
        self._buffer = ''
        self.codes = get_term_codes()

        self.stream = stream or sys.stdout
        self.set_style('DEFAULT', default)

    def __getitem__(self, key):
        return self.codes[key]

    def __getattr__(self, key):
        value = self.codes.get(key, None)
        if value is None:
            raise AttributeError(key)
        self._buffer += _(value)
        return self

    def __call__(self, content='', flush=True):
        self._buffer += content + _(self['DEFAULT'])
        if flush:
            self.stream.write(self._buffer)
            self._buffer = ''
        return self

    @property
    def cols(self):
        return curses.tigetnum('cols')

    @property
    def lines(self):
        return curses.tigetnum('lines')

    def set_style(self, name, args):
        self.codes[name] = b''.join([(self[a]) for a in args])


    def demo(self):
        """demo colors and capabilities of your terminal """
        for color in ANSI_COLORS:
            getattr(self, color)("%-8s" % color)(' ')
            getattr(self, color).BOLD('bold')(' ')
            getattr(self, color).REVERSE('reverse')(' ')
            getattr(self, color).UNDERLINE('underline')(' ')
            getattr(self, color).BG_YELLOW('bg_yellow')(' ')
            getattr(self, color).UNDERLINE.BOLD('rev+under')(' ')
            self('\n')
