from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
_ = MessageFactory('collective.confirm_email')

from .decorator import confirm_email
