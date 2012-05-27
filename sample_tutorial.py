from pyterm import Term

if __name__ == "__main__":
    myterm = Term()

    # basic features demo
    myterm.YELLOW('a yellow line\n').NORMAL('somethin else\n')
    myterm.BG_MAGENTA.GREEN("bit of green").UNDERLINE.RED(" and red\n")
    myterm('normal again\n')
    myterm.set_style('SUCCESS', ['GREEN', 'UNDERLINE'])
    myterm.SUCCESS('ok\n')

