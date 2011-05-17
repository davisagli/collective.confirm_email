from zope.interface import Interface, Attribute


class INonceManager(Interface):
    """A persistent utility that stores nonces.
    
    A nonce is a key-to-value mapping that can be used once.
    """
    
    def store(value):
        """Adds a value to the store and returns the key."""
    
    def retrieve(key, default=None):
        """Returns the value of a nonce and deletes it from the store.
        Also cleans old nonces as a side effect.
        """
    
    def clean():
        """Deletes nonces older than ``max_age`` days that have not been used."""

    max_age = Attribute("""Maximum age of nonces in days. Nonces older than """
                        """this threshold may be removed.  Defaults to 10.""")