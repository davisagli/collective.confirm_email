import time
from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.interface import implements
from collective.confirm_email.interfaces import INonceManager
from uuid import uuid4


class NonceManager(Persistent):
    """ A BTree-based persistent storage of nonces.
    
    For the purposes of this package, a nonce is a temporary mapping of a
    unique identifier to some data.
    
    A nonce manager may be instantiated and inserted into the persistent
    object graph. (Typically, it could be registered as a named local utility.)
    
      >>> from collective.confirm_email.nonce import NonceManager
      >>> nm = NonceManager()
    
    A nonce may be created on demand, and is stored until it is retrieved.
    It is deleted when it is retrieved, so it may only be retrieved once.
    
      >>> uuid = nm.store('foobar')
      >>> nm.retrieve(uuid)
      'foobar'
      >>> nm.retrieve(uuid) # doctest: +ELLIPSIS
      Traceback (most recent call last):
      KeyError: ...
    
    When a nonce is retrieved, a cleanup procedure removes nonces older
    than a defined threshold.
    
      >>> uuid2 = nm.store('foobar2')
      >>> nm.max_age = 0
      >>> time.sleep(1)
      >>> nm.retrieve(uuid2) # doctest: +ELLIPSIS
      Traceback (most recent call last):
      KeyError: ...
    """
    implements(INonceManager)
    
    _nonces = None
    max_age = 10
    
    def __init__(self):
        self._nonces = OOBTree()
    
    def store(self, value):
        # get UUID and timestamp
        uuid = str(uuid4())
        timestamp = int(time.time())
        
        self._nonces[uuid] = (timestamp, value)
        return uuid
    
    def retrieve(self, key):
        self.clean()
        res = self._nonces[key][1]
        del self._nonces[key]
        return res
    
    def clean(self):
        cutoff = int(time.time()) - self.max_age * 86400
        for uuid in self._nonces.keys():
            timestamp = self._nonces[uuid][0]
            if timestamp < cutoff:
                del self._nonces[uuid]
