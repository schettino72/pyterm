from pyterm import Term


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
        self.width = self.term.cols() or 75
        self.cleared = True #: true if we haven't drawn the bar yet.
        self.update(0, '')

    def header(self):
        """prints the header of the progress bar (first line)"""
        self.term.BOLD.CYAN(self._header_text.center(self.width))('\n\n')

    def bar(self, percent):
        """print the progress bar (second line)"""
        bar_width = self.width - 10
        progress = int(bar_width * percent)
        remaining = bar_width - progress
        self.term('%3d%%' % (percent*100))
        self.term.GREEN('[').GREEN.BOLD('='*progress + '-'*remaining).GREEN(']\n')

    def update(self, percent, message):
        """ """
        if self.cleared:
            self.header()
            self.cleared = False
        # remove the second last line (progress-bar line) and redraw it
        self.term.BOL.UP.CLEAR_EOL
        self.bar(percent)
        # update third line (progress message)
        self.term.CLEAR_EOL(message.center(self.width))

    def clear(self):
        """clear the last 3 lines"""
        if not self.cleared:
            self.term.BOL.CLEAR_EOL.UP.CLEAR_EOL.UP.CLEAR_EOL()
            self.cleared = True



if __name__ == "__main__":
    myterm = Term()

    # progress bar demo
    import time
    term = Term()
    progress = ProgressBar(term, 'Processing some files')
    filenames = ['this', 'that', 'other', 'foo', 'bar', 'baz']
    for i, filename in enumerate(filenames):
        progress.update(float(i)/len(filenames), 'working on %s' % filename)
        time.sleep(.5)
    progress.clear()
