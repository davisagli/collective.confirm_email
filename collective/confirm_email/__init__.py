from zope.i18nmessageid import MessageFactory
from zExceptions import Redirect
from collective.beaker.interfaces import ISession


# Set up the i18n message factory for our package
_ = MessageFactory('collective.confirm_email')


def confirm_email(self):
    # if the session has been confirmed, do nothing
    session = ISession(self.request)
    if session.get('collective.confirm_email.confirmed'):
        return

    # if it hasn't, redirect to the confirmation page
    url = self.request['URL']
    raise Redirect(url + '/confirm-email')
