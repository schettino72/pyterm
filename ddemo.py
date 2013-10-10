import ast

source = open('sample_tutorial.py').read()

block = []
for line in source.splitlines():
    if block and (not line or line[0] != ' '):
        # previous block finished
        print('...')
        exec(compile('\n'.join(block), '<string>', 'exec'))
        block = []

    if not line:
        print('>>>')
    else:
        if line[0] != ' ':
            # single line or block start
            try:
                print('''>>> {}'''.format(line))
                ast.parse(line)
                exec(compile(line, '<string>', 'exec'))
            except:
                block.append(line)
        else:
            print('''... {}'''.format(line))
            block.append(line)

if block:
    exec(compile('\n'.join(block), '<string>', 'exec'))
