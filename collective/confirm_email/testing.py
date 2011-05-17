from zope.component import provideUtility
from zope.configuration import xmlconfig
from plone.testing import Layer
from plone.testing import zca
from plone.testing import z2
from Products.MailHost.MailHost import _mungeHeaders
from Products.MailHost.MailHost import MailBase
from Products.MailHost.interfaces import IMailHost
from collective.beaker.testing import BeakerConfigLayer


class MockMailHost(MailBase):
    """A MailHost that collects messages instead of sending them.
    """

    def __init__(self, id):
        self.reset()

    def reset(self):
        self.messages = []

    def _send(self, mfrom, mto, messageText, immediate=False):
        """ Send the message """
        self.messages.append(messageText)

    def send(self, messageText, mto=None, mfrom=None, subject=None,
             encode=None, immediate=False, charset=None, msg_type=None):
        messageText, mto, mfrom = _mungeHeaders(messageText,
                                                mto, mfrom, subject,
                                                charset=charset,
                                                msg_type=msg_type)
        self.messages.append(messageText)


class MyLayer(Layer):
    
    defaultBases = (z2.STARTUP,)
    
    def setUp(self):
        BeakerConfigLayer.setUp()
        
        zca.pushGlobalRegistry()
        self['configurationContext'] = context = zca.stackConfigurationContext(self.get('configurationContext'))
        import collective.confirm_email
        xmlconfig.file('configure.zcml', package=collective.confirm_email, context=context)
        
        from collective.confirm_email.nonce import NonceManager
        from collective.confirm_email.interfaces import INonceManager
        provideUtility(NonceManager(), provides=INonceManager)
        provideUtility(MockMailHost('MailHost'), provides=IMailHost)

    def tearDown(self):
        zca.popGlobalRegistry()
        del self['configurationContext']


FIXTURE = MyLayer()
INTEGRATION_TESTING = z2.IntegrationTesting(bases=(FIXTURE,), name='collective.confirm_email:Integration')
FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(FIXTURE,), name='collective.confirm_email:Functional')
