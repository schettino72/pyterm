"""pyterm - terminal output style/positioning control

http://pythonhosted.org/pyterm

`pyterm` is tool designed to easy the use of colors,
formatting and positioning of text in a terminal without
the use of `curses` mode (curses.initwin).

By default the python `curses` module is used to get code info from the terminal.
If `curses` is not available ANSI codes are used.
The idea to use curses to get terminfo was taken from
blessings [https://pypi.python.org/pypi/blessings/]

references:

 * http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
 * http://code.activestate.com/recipes/475116/

The MIT License  (see LICENSE file)
Copyright (c) 2013 Eduardo Naufel Schettino

"""

__version__ = (0, 3, 'dev0')


import sys
import subprocess


# compatibility python2 and python3
if sys.version_info >= (3, 0): # pragma: nocover
    decode = lambda s: s.decode('utf-8')
    escape = lambda x: x.encode('unicode_escape').decode('utf-8')
    int2byte = lambda x: bytes(str(x), 'ascii')
else:
    decode = lambda s: s
    escape = lambda x: x.encode('string_escape')
    int2byte = lambda x: str(x)

# pair with friendly-name / capability-name
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


#http://en.wikipedia.org/wiki/ANSI_escape_code
ANSI_ESC = b'\x1b['
ANSI_CODES = [
    # cursor movement
    ('BOL', b'G'),   # begining of line
    ('UP', b'A'),
    ('DOWN', b'B'),
    ('LEFT', b'D'),
    ('RIGHT', b'C'),

    # clear
    ('CLEAR_SCREEN', b'H' + ANSI_ESC + b'2J'),
    ('CLEAR_EOL', b'K'),
    ('CLEAR_EOS', b'J'), # clear to end of display

    # write mode
    ('BOLD', b'1m'),
    ('REVERSE', b'7m'),
    ('UNDERLINE', b'4m'),
    ('NORMAL', b'm'),
    ]


def get_codes_curses(fd):
    """get capabilities and color codes using the curses module"""
    import curses
    curses.setupterm(None, fd)
    codes = dict((name, curses.tigetstr(code)) for name, code in CAPABILITY)
    for index, name in enumerate(ANSI_COLORS):
        codes[name] = curses.tparm(codes['A_COLOR'], index)
        codes['BG_'+name] = curses.tparm(codes['A_BG_COLOR'], index)
    return codes

def get_codes_dumb():
    """get all codes as empty string"""
    codes = dict((name, b'') for name, _ in CAPABILITY)
    for name in ANSI_COLORS:
        codes[name] = b''
        codes['BG_'+name] = b''
    return codes

def get_codes_ansi():
    """get all ANSI codes"""
    codes = dict((name, ANSI_ESC + code) for name, code in ANSI_CODES)
    for index, name in enumerate(ANSI_COLORS):
        codes[name] = ANSI_ESC + b'3' + int2byte(index) + b'm'
        codes['BG_'+name] = ANSI_ESC + b'4' + int2byte(index) + b'm'
    return codes



class Term(object):
    """Ouput formatting to a terminal with curses capabilities

    @ivar codes: (dict) key: capability-name as exposed by API
                        value: capability-code as understood by curses

    @ivar _buffer: content to be sent to terminal
    """
    def __init__(self, stream=None, start_code=('NORMAL',),
                 code=None, use_colors=None):
        """
        @ivar stream: where the output will be written to (default: sys.stdout)
        @param start_code: sequence of codes to be appended to the
                           end of content on every write.
                           default: [('NORMAL', )]
        @param code: use 'ansi' to use ANSI codes instead of quering
                     capabilities with curses
        @param use_colors: force enable/disable use of colors codes
        """
        self.stream = stream or sys.stdout
        # self.code is one of: curses, ansi, dumb
        self.code, self.codes = self.get_codes(code, use_colors)
        self.codes = dict((k, decode(v)) for k, v in self.codes.items())
        self.set_style('DEFAULT', start_code)
        self._buffer = self['DEFAULT']

    def get_codes(self, code=None, use_colors=None):
        """select source of codes (curses, ansi, dumb) and set self.codes"""
        if (use_colors is True or
            (use_colors is None and self.stream.isatty())):
            if code=='ansi':
                return 'ansi', get_codes_ansi()
            else:
                try:
                    return 'curses', get_codes_curses(self.stream.fileno())
                except:
                    return 'ansi', get_codes_ansi()
        else:
            return 'dumb', get_codes_dumb()


    def __getitem__(self, key):
        """@return (bytes) code of capability/color
        @param key: (str) capability/color name
        """
        return self.codes[key]

    def __getattr__(self, key):
        """adds attribute code to buffer
        @return self (in order to allow chaining)
        """
        self._buffer += self.codes[key]
        return self

    def __call__(self, content='', flush=True):
        """adds given content & default_end to buffer, writes buffer if 'flush
        @return self (in order to allow chaining)
        """
        self._buffer += content + self['NORMAL']
        if flush:
            self.stream.write(self._buffer)
            self._buffer = self['DEFAULT']
        return self

    def cols(self):
        """@return (int) number of columns on terminal window"""
        if self.code != 'curses':
            # FIXME py3.3 has a function with this functionality
            return int(subprocess.check_output(['stty', 'size']).split()[1])
        try:
            import curses
            return curses.tigetnum('cols')
        except:
            pass

    def lines(self):
        """@return (int) number of lines on terminal window"""
        if self.code != 'curses':
            return int(subprocess.check_output(['stty', 'size']).split()[0])
        try:
            import curses
            return curses.tigetnum('lines')
        except:
            pass

    def set_style(self, name, args):
        """set/create a new capability
        mostly used to create named sequence of codes
        """
        self.codes[name] = ''.join([(self[a]) for a in args])

    def demo(self):
        """demo colors and capabilities of your terminal """
        self.REVERSE('\n{:^56}\n'.format('ANSI COLORS'))
        for color in ANSI_COLORS:
            getattr(self, color)("%-8s" % color)(' ')
            getattr(self, color).BOLD('bold')(' ')
            getattr(self, color).REVERSE('reverse')(' ')
            getattr(self, color).UNDERLINE('underline')(' ')
            getattr(self, color).BG_YELLOW('bg_yellow')(' ')
            getattr(self, color).REVERSE.BOLD('bold+reverse')(' ')
            self('\n')

        line_fmt = "| {:15} | {:10} | {:15} |\n"
        self('\n')
        if self.code == 'curses':
            self.BOLD.REVERSE(line_fmt.format('NAME', 'CODE', 'VALUE'))
            for name, cap_name in CAPABILITY:
                self(line_fmt.format(name, cap_name, escape(self[name])))
            self.REVERSE('-' * 50 + '\n')
            self('\n')




if __name__ == '__main__': # pragma: no cover
    term = Term()
    term.demo()
