# references
# http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
# http://code.activestate.com/recipes/475116/


import curses
import sys


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
    # get capabilities and color codes
    curses.setupterm()
    codes = dict((name, curses.tigetstr(code)) for name, code in CAPABILITY)
    for index, name in enumerate(ANSI_COLORS):
        codes[name] = curses.tparm(codes['A_COLOR'], index)
        codes['BG_'+name] = curses.tparm(codes['A_BG_COLOR'], index)
    return codes

CODES = get_term_codes()


class Term(object):
    # TODO
    # * auto detect terminal. do not explode
    def __init__(self, stream=None, default=('NORMAL',)):
        self._buffer = ''
        self.codes = CODES.copy()

        self.stream = stream or sys.stdout
        self.set_style('DEFAULT', default)

    def __getitem__(self, key):
        return self.codes[key]

    def __getattr__(self, key):
        value = self.codes.get(key, None)
        if value is None:
            raise AttributeError(key)
        self._buffer += value
        return self

    def __call__(self, content='', flush=True):
        self._buffer += content + self['DEFAULT']
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
        self.codes[name] = ''.join([self[a] for a in args])



################################################################


# based on http://code.activestate.com/recipes/475116/
class ProgressBar:
    """
    A 3-line progress bar, which looks like::

                                Header
        20% [===========----------------------------------]
                           progress message

    The progress bar is colored, if the terminal supports color
    output; and adjusts to the width of the terminal.
    """

    def __init__(self, term, header):
        if not (term['CLEAR_EOL'] and term['UP'] and term['BOL']):
            raise ValueError("Terminal isn't capable enough -- you "
                             "should use a simpler progress dispaly.")
        self.term = term
        self._header_text = header
        self.width = self.term.cols or 75
        self.cleared = 1 #: true if we haven't drawn the bar yet.
        self.update(0, '')

    def bar(self, percent):
        width = self.width - 10
        progress = int(width * percent)
        remaining = width - progress
        self.term('%3d%%' % (percent*100))
        self.term.GREEN('[').GREEN.BOLD('='*progress + '-'*remaining).GREEN(']\n')

    def header(self):
        self.term.BOLD.CYAN(self._header_text.center(self.width))('\n\n')

    def update(self, percent, message):
        if self.cleared:
            self.header()
            self.cleared = 0
        self.term.BOL.UP.CLEAR_EOL
        self.bar(percent)
        self.term.CLEAR_EOL(message.center(self.width))

    def clear(self):
        if not self.cleared:
            self.term.BOL.CLEAR_EOL.UP.CLEAR_EOL.UP.CLEAR_EOL()
            self.cleared = 1



if __name__ == "__main__":

    # basic features demo
    myterm = Term()
    myterm.YELLOW('a yellow line\n').NORMAL('somethin else\n')
    myterm.UNDERLINE.GREEN("bit of green").UNDERLINE.RED(" and red\n")
    myterm('normal again\n')
    myterm.set_style('SUCCESS', ['GREEN', 'UNDERLINE'])
    myterm.SUCCESS('ok\n')

    # progress bar demo
    import time
    term = Term()
    progress = ProgressBar(term, 'Processing some files')
    filenames = ['this', 'that', 'other', 'foo', 'bar', 'baz']
    for i, filename in zip(range(len(filenames)), filenames):
        progress.update(float(i)/len(filenames), 'working on %s' % filename)
        time.sleep(.7)
    progress.clear()
