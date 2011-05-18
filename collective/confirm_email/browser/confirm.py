import re
from zExceptions import Redirect
from zope.component import getUtility, queryUtility
from zope.interface import Interface, implements
from zope import schema
from zope.publisher.interfaces import IPublishTraverse
from z3c.form import form, field, button
from plone.z3cform import z2
from Products.MailHost.interfaces import IMailHost
from collective.beaker.interfaces import ISession
from collective.confirm_email.interfaces import INonceManager
from collective.confirm_email import _

try:
    from Products.CMFCore.interfaces import ISiteRoot
    HAS_SITE_ROOT = True
except ImportError:
    HAS_SITE_ROOT = False


EMAIL_RE = re.compile("^([0-9a-zA-Z_&.'+-]+!)*[0-9a-zA-Z_&.'+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$")

class InvalidEmailError(schema.ValidationError):
    __doc__ = u'You must enter a valid email address.'

def isEmail(value):
    if EMAIL_RE.match(value):
        return True
    raise InvalidEmailError


class IEmailConfirmation(Interface):
    
    email = schema.ASCIILine(
        title = _(u'Email Address'),
        description = _(u'Please enter your email address.'),
        constraint = isEmail,
        )


class EmailConfirmationForm(form.Form):
    implements(IPublishTraverse)
    
    label = u'Confirm Email Address'
    description = (u'Please enter your email address. You will receive an email '
                   u'to confirm your ownership of that address. Please click the '
                   u'link in that email to continue.')
    
    ignoreContext = True

    fields = field.Fields(IEmailConfirmation)

    def __init__(self, view, request):
        self.context = view.context
        self.request = request

    # the confirm code is passed as an extra path element
    # i.e. /foo/@@confirm-email/[code]
    orig_url = None
    confirm_code = None
    def publishTraverse(self, request, name):
        if self.orig_url is None:
            self.orig_url = request.URL1
        self.confirm_code = name
        return self
    
    def __call__(self):
        """Confirm the code or render the form."""
        
        # make sure we have the form marker interface when testing
        z2.switch_on(self)
        
        if self.confirm_code:
            # confirm/delete nonce
            nonce_store = getUtility(INonceManager)
            try:
                email = nonce_store.retrieve(self.confirm_code)
            except KeyError:
                self.status = _(u'Sorry, your confirmation code is invalid or has expired.')
            else:
                # set up session
                session = ISession(self.request)
                session['collective.confirm_email.confirmed'] = True
                session['collective.confirm_email.email'] = email
                session.save()
            
                # redirect back to target (by removing last 2 parts of path)
                raise Redirect(self.request['URL2'])

        # render form
        return super(EmailConfirmationForm, self).__call__()

    @button.buttonAndHandler(_('Send Confirmation'))
    def handleSend(self, action):
        data, errors = self.widgets.extract()
        if errors:
            self.status = _('There were errors.')
            return

        nonce_store = getUtility(INonceManager)
        nonce = nonce_store.store(data['email'])
        url = '%s/%s' % (self.orig_url or self.request['URL'], nonce)
        
        msg = "Please click this link to continue.\n %s" % url
        mto = data['email']
        mfrom = 'test@example.com'
        if HAS_SITE_ROOT:
            site = queryUtility(ISiteRoot)
            if site is not None:
                mfrom = site.email_from_address
        subject = 'E-mail confirmation'
        mailhost = getUtility(IMailHost)
        mailhost.send(msg, mto, mfrom, subject)
        
        self.status = _(u'Confirmation was sent.')
