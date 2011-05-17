import doctest
import unittest
from plone.testing import layered
from collective.confirm_email.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('functional.txt'), layer=FUNCTIONAL_TESTING),
        doctest.DocTestSuite(module='collective.confirm_email.nonce'),
    ])
    return suite
