from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.confirm_email',
      version=version,
      description="Helper to require email verification to access a Zope 2 browser view",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='verify email',
      author='David Glick, Groundwire',
      author_email='davidglick@groundwire.org',
      url='http://github.com/davisagli/collective.confirm_email',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.beaker',
          'plone.z3cform',
          'Products.MailHost',
          'z3c.form',
          'ZODB3',
          'Zope2',
          'zope.component',
          'zope.configuration',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
          'zope.publisher',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.testing'],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
