# Color manipulation tutorial

from pyterm import Term

# create a terminal instance
myterm = Term()

# you can check the code for a capability in your terminal
print(myterm.codes['BLUE'].encode('string_escape'))
print(myterm['BLUE'].encode('string_escape'))

# and check all the available capabilities
print(myterm.codes.keys())

# to print something call your terminal with the desired string
myterm('a string in normal colors\n')

# to add a color access the capability name as a property
myterm.YELLOW('a yellow line\n')

# note how the colors are reset after any ouput
myterm('again in normal colors\n')

# you can chain adding codes and output to a stream
myterm.BG_MAGENTA.GREEN("bit of green").UNDERLINE.RED(" and red\n")

# you can create new named "styles" combining different codes
myterm.set_style('ERROR', ['RED', 'UNDERLINE'])
myterm.ERROR('fail\n')

# by default every output is flushed, you can disable that with a parameter
myterm.GREEN('part one -> ', flush=False)

# the default colors can be configured on terminal creation
term2 = Term(start_code=('BLUE', 'BOLD'))
term2('this is the default font\n')
term2.NORMAL.RED('a bit of red\n')
term2('back to the default (blue)\n')

# by default the stream is sent to stdout (sys.stdout)
# If the selected stream is not a tty all codes are disabled
with open('/tmp/pyt.txt', 'w') as my_file:
    # make it hard
    term3 = Term(stream=my_file)
    term3.RED('ignore color when writting to file')
with open('/tmp/pyt.txt', 'r') as my_file:
    print(my_file.read())

# to force the use of colors use `color=True`
with open('/tmp/pyt.txt', 'w') as my_file:
    # make it hard
    term3 = Term(stream=my_file, color=True)
    term3.RED('force color when writting to file')
with open('/tmp/pyt.txt', 'r') as my_file:
    print(my_file.read())

# you can also force disable the use of colors
term4 = Term(color=False)
term4.RED('dont use colors!\n')
