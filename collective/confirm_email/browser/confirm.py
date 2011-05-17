from zope.interface import Interface
from z3c.form import form, field


class EmailConfirmationForm(form.Form):
    
    label = u'Confirm Email Address'
    description = (u'Please enter your email address. You will receive an email '
                   u'to confirm your ownership of that address. Please click the '
                   u'link in that email to continue.')

    fields = field.Fields(Interface)

    confirm_code = None
    
    def __call__(self):
        if self.confirm_code:
            assert 0

        # render form
        return super(EmailConfirmationForm, self).__call__()
