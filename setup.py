from setuptools import setup, find_packages
import os, codecs

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),'r', encoding='utf-8').read()

try:
    import pypandoc
    content = read('README.md')
    long_description = pypandoc.convert(content, 'rst', format='md')
except(IOError, ImportError) as e:
    long_description = read('README.md')

setup(
  name = 'zpyshell',
  packages = find_packages(),
  version = '0.1.2.0',

  description = 'Command line shell with script languages, like python',
  long_description=long_description,
  author = 'Albert Aleksieiev',
    include_package_data = True,
  author_email = 'albert.aleksieiev@gmail.com',
  url = 'https://albertaleksieiev.github.io/zpy/',
  download_url = 'https://github.com/albertaleksieiev/zpy/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['python', 'command', 'line','shell','unix','terminal'], # arbitrary keywords
  classifiers = ['Topic :: Software Development :: Interpreters',
                 'Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Terminals',
                 'Environment :: Console'
                 ],
    extras_require = {
        'coloring_console':  ["pygments"],

        'prompt': ["prompt_toolkit"],

        'docs': ["pypandoc"],

        'tables_for_terminal': ["terminaltables"],
    },
    install_requires=[
        "pygments",
        "prompt_toolkit",
        "pypandoc",
        "terminaltables==3.1.0",
    ],
    entry_points={
       'console_scripts': [
           'zpy = Zpy.main:main',
       ],
    }
)
