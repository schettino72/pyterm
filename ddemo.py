"""Fake output as if code was typed in an interactive interpreter

This is used to generate docs
"""

import ast
import sys

from pyterm import Term


# copy from doit.action
class Writer(object):
    """write to many streams"""
    def __init__(self, *writers):
        """@param writers - file stream like objects"""
        self.writers = []
        self._isatty = True
        for writer in writers:
            self.add_writer(writer)

    def add_writer(self, stream, isatty=None):
        """adds a stream to the list of writers
        @param isatty: (bool) if specified overwrites real isatty from stream
        """
        self.writers.append(stream)
        isatty = stream.isatty() if (isatty is None) else isatty
        self._isatty = self._isatty and isatty

    def write(self, text):
        """write 'text' to all streams"""
        for stream in self.writers:
            stream.write(text)

    def flush(self):
        """flush all streams"""
        for stream in self.writers:
            stream.flush()

    def isatty(self):
        return self._isatty

    def fileno(self):
        return 0 #return whatever

# fake our sys.stdout to be always considered a tty
new_out = Writer()
new_out.add_writer(sys.stdout, isatty=True)
sys.stdout = new_out




source = open('tutorial.py').read()

term = Term()
block = []
for line in source.splitlines():
    if block and (not line or line[0] != ' '):
        # previous block finished
        term.BOLD('...\n')
        exec(compile('\n'.join(block), '<string>', 'exec'))
        block = []

    if not line:
        term.BOLD('>>>\n')
    else:
        if line[0] != ' ':
            # single line or block start
            try:
                term.BOLD('''>>> {}\n'''.format(line))
                ast.parse(line)
                exec(compile(line, '<string>', 'exec'))
            except:
                block.append(line)
        else:
            term.BOLD('''... {}\n'''.format(line))
            block.append(line)

if block:
    exec(compile('\n'.join(block), '<string>', 'exec'))
