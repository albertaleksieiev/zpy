import unittest
import doctest
import ZPy.Pipeline, ZPy.Utils, ZPy.Processor
import ZPy.languages.LanguageAnalyzer, ZPy.languages.python.python_lang, ZPy.languages.shell.unix_lang
import ZPy.storage.SuffixTree
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(ZPy.Pipeline))
    tests.addTests(doctest.DocTestSuite(ZPy.Utils))
    tests.addTests(doctest.DocTestSuite(ZPy.Processor))
    tests.addTests(doctest.DocTestSuite(ZPy.Processor))
    tests.addTests(doctest.DocTestSuite(ZPy.languages.LanguageAnalyzer))
    tests.addTests(doctest.DocTestSuite(ZPy.languages.python.python_lang))
    tests.addTests(doctest.DocTestSuite(ZPy.languages.shell.unix_lang))
    tests.addTests(doctest.DocTestSuite(ZPy.storage.SuffixTree))

    return tests

#unittest.main()