Introduction
============

``collective.confirm_email`` provides a helper to require that the user
confirm their email address before accessing a Zope 2 browser view.

A browser view can require this protection by using the ``confirm_email``
helper when it is called::

  from collective.confirm_email import confirm_email

  class ProtectedView(object):

      def __init__(self, context, request):
          self.context = context
          self.request = request

      def __call__(self):
          confirm_email(self)
          # do stuff here

A beaker session is used to keep track of whether the user's email has
been confirmed.  If the ``collective.confirm_email.confirmed`` key is
not found in the session, the user is redirected to the ``confirm-email``
form which asks them to enter their email address.

Upon entry, a nonce is generated and stored, and an email is sent to the
user including a link back to the ``confirm-email`` view with the nonce
included. When the user clicks the link, the view validates the nonce,
and if it is valid, sets up the beaker session. The email address that
was entered is also stored in the beaker session under the
``collective.confirm_email.email`` key, so it can be used by the original
view::

  from collective.beaker.interfaces import ISession

  session = ISession(self.request)
  email = session['collective.confirm_email.email']

Installation
------------

You must configure ``collective.beaker`` sessions as described in its
documentation.

You must run the ``collective.confirm_email`` default profile, or otherwise
arrange for an ``INonceManager`` to be available.
