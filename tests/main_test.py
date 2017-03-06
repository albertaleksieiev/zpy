import unittest

import sys, os
# Setup working dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import doctest
import Zpy.Pipeline, Zpy.Utils, Zpy.Processor
import Zpy.languages.LanguageAnalyzer, Zpy.languages.python.python_lang, Zpy.languages.shell.unix_lang
import Zpy.storage.SuffixTree
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(Zpy.Pipeline))
    tests.addTests(doctest.DocTestSuite(Zpy.Utils))
    tests.addTests(doctest.DocTestSuite(Zpy.Processor))
    tests.addTests(doctest.DocTestSuite(Zpy.Processor))
    tests.addTests(doctest.DocTestSuite(Zpy.languages.LanguageAnalyzer))
    tests.addTests(doctest.DocTestSuite(Zpy.languages.python.python_lang))
    tests.addTests(doctest.DocTestSuite(Zpy.languages.shell.unix_lang))
    tests.addTests(doctest.DocTestSuite(Zpy.storage.SuffixTree))

    return tests

unittest.main()