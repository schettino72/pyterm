"""pyterm - terminal output formatting

Ouput formatting to a terminal with curses capabilities

Curses mode (curses.initwin) is not used.
pyterm controls color, text attributes (bold, inverse,...) and
cursor position.

references:

 * http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
 * http://code.activestate.com/recipes/475116/


The MIT License
Copyright (c) 2012 Eduardo Naufel Schettino
see LICENSE file

"""

__version__ = (0, 1, 'dev')



import curses
import sys


# compatibility python2 and python3
if sys.version_info >= (3, 0): # pragma: nocover
    _ = lambda s: s.decode('utf-8')
else:
    _ = lambda s: s


# each element is a 2-value tuple mapping capability-name to capability-code
CAPABILITY = [
    # cursor movement
    ('BOL', 'cr'),     # carriage_return (go to beginning of line)
    ('UP', 'cuu1'),    # cursor_up
    ('DOWN', 'cud1'),  # cursor_down
    ('LEFT', 'cub1'),  # cursor_left
    ('RIGHT', 'cuf1'), # cursor_right

    # clear
    ('CLEAR_SCREEN', 'clear'), # clear_screen
    ('CLEAR_EOL', 'el'),       # clr_eol - clear to end of line
    ('CLEAR_EOS', 'ed'),       # clr_eos - clear to end of display

    # write mode
    ('BOLD', 'bold'),      # enter_bold_mode - turn on bold (extra bright) mode
    ('REVERSE', 'rev'),    # enter_reverse_mode - turn on reverse video mode
    ('UNDERLINE', 'smul'), # enter_underline_mode - start underscore mode
    ('NORMAL', 'sgr0'),    # exit_attribute_mode - turn off all attributes

    # colors
    ('A_COLOR', 'setaf'),    # set_a_foreground
    ('A_BG_COLOR', 'setab'), # set_a_background
    ]

ANSI_COLORS = ['BLACK', 'RED', 'GREEN', 'YELLOW',
               'BLUE', 'MAGENTA', 'CYAN', 'WHITE']


def get_term_codes():
    """get capabilities and color codes
    @return (dict) capability-name: capability-value
    """
    curses.setupterm()
    codes = dict((name, curses.tigetstr(code)) for name, code in CAPABILITY)
    for index, name in enumerate(ANSI_COLORS):
        codes[name] = curses.tparm(codes['A_COLOR'], index)
        codes['BG_'+name] = curses.tparm(codes['A_BG_COLOR'], index)
    return codes


class Term(object):
    """Ouput formatting to a terminal with curses capabilities

    @ivar codes: (dict) key: capability-name as exposed by API
                        value: capability-value for current terminal

    @ivar _buffer: content to be sent to terminal
    """
    def __init__(self, stream=None, default_end=('NORMAL',)):
        """
        @ivar stream: where the output will be written to (default: sys.stdout)
        @param default_end: sequence of codes to be appended to the
                            end of content on every write.
                            default: ['NORMAL']
        """
        self._buffer = ''
        self.codes = get_term_codes()

        self.stream = stream or sys.stdout
        self.set_style('DEFAULT', default_end)

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
        self._buffer += content + _(self['DEFAULT'])
        if flush:
            self.stream.write(self._buffer)
            self._buffer = ''
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



#### demo functions

def demo_capabilities(term):
    """display table with capabilities of current terminal"""
    term.set_style('HEADER', ('BOLD', 'UNDERLINE'))
    term.HEADER("API-name")("      ")
    term.HEADER("cap-code")("  ")
    term.HEADER("cap-value\n")
    for name, code in CAPABILITY:
        print("%-14s"  % name +
              "%-10s" % code +
              repr(term[name]))

def demo_color(term):
    """demo colors of current terminal """
    for color in ANSI_COLORS:
        getattr(term, color)("%-8s" % color)(' ')
        getattr(term, color).BOLD('bold')(' ')
        getattr(term, color).REVERSE('reverse')(' ')
        getattr(term, color).UNDERLINE('underline')(' ')
        getattr(term, color).BG_YELLOW('bg_yellow')(' ')
        getattr(term, color).UNDERLINE.BOLD('bold+under')(' ')
        term('\n')



if __name__ == "__main__":
    term = Term()

    term.BOLD.REVERSE("\n    *** Capabilities ***   \n")
    demo_capabilities(term)

    term.BOLD.REVERSE("\n    *** Colors ***    \n")
    demo_color(term)
    print("\n")
