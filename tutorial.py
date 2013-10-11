# pyterm - Color manipulation tutorial
from pyterm import Term, escape


# create a terminal instance
term = Term()


# you can check the code for a capability in your terminal
print(escape(term.codes['BLUE']))
print(escape(term['BLUE']))


# and check all the available capabilities
print(term.codes.keys())


# to print something call your terminal with the desired string
term('a string in normal colors\n')


# to add a color access the capability name as a property
term.YELLOW('a yellow line\n')


# note how the colors are reset after any ouput
term('again in normal colors\n')


# you can chain codes and output to a stream
term.BOLD.BG_MAGENTA.GREEN("bit of green").UNDERLINE.RED(" and red\n")


# you can create new named "styles" combining different codes
term.set_style('ERROR', ['RED', 'UNDERLINE'])
term.ERROR('fail\n')


# by default every output is flushed, you can disable that with a parameter
term.GREEN('part one -> \n', flush=False).GREEN('part two \n')


# the default colors can be configured on terminal creation
term2 = Term(start_code=('BLUE', 'BOLD'))
term2('this is the default font\n')
term2.NORMAL.RED('a bit of red\n')
term2('back to the default (blue)\n')


# by default the stream is sent to stdout (sys.stdout)
# If the selected stream is not a tty all codes are disabled
with open('/tmp/pyt.txt', 'w') as my_file:
    term3 = Term(stream=my_file)
    term3.RED('ignore color when writting to file')
with open('/tmp/pyt.txt', 'r') as my_file:
    print(my_file.read())


# to force the use of colors use `color=True`
with open('/tmp/pyt.txt', 'w') as my_file:
    term3 = Term(stream=my_file, color=True)
    term3.RED('force color when writting to file')
with open('/tmp/pyt.txt', 'r') as my_file:
    print(my_file.read())


# you can also force disable the use of colors
term4 = Term(color=False)
term4.RED('dont use colors!\n')


# check the demo to see the colors and available capabilities
term.demo()
