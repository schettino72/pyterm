import os
import glob


DOIT_CONFIG = {'default_tasks': ['checker', 'test']}


PY_FILES = glob.glob('*.py')

def task_checker():
    """run pyflakes on all project files"""

    def add_pyflakes_builtins():
        os.environ['PYFLAKES_BUILTINS'] = 'unicode'
    yield {
        'basename': '_pyflakes_builtins',
        'actions': [add_pyflakes_builtins]
        }

    for module in PY_FILES:
        yield {'actions': ["pyflakes %(dependencies)s"],
               'name':module,
               'file_dep':(module,),
               'setup':['_pyflakes_builtins'],
               'title': (lambda task: task.name)
               }

def task_test():
    return {
        'actions': ['py.test'],
        'file_dep': PY_FILES,
        }

def task_coverage():
    return {
        'actions': ['py.test --cov pyterm.py --cov test_pyterm.py --cov-report term-missing'],
        'verbosity': 2,
        }


def task_docs():
    yield {
        'name': 'terminal',
        'actions': ['python ddemo.py | ansi2html --partial --scheme=xterm > tutorial.html'],
        'file_dep': ['pyterm.py', 'tutorial.py', 'ddemo.py',],
        'targets': ['_tutorial.html'],
        }

    def render_template():
        from ansi2html import Ansi2HTMLConverter
        with open('index.tmpl', 'r') as f: template = f.read()
        with open('_tutorial.html', 'r') as f: terminal = f.read()
        header = Ansi2HTMLConverter(scheme='xterm').produce_headers()
        with open('index.html', 'w') as html:
            html.write(template.format(
                header=header,
                terminal=terminal))

    yield {
        'name': 'page',
        'file_dep': ['index.tmpl', '_tutorial.html'],
        'actions': [render_template],
        'targets': ['index.html'],
        }
