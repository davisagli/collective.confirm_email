from zExceptions import Redirect


def confirm_email(cls):
    if not callable(cls):
        return cls
    
    __call__ = cls.__call__
    def wrapped_call(self, *args, **kw):
        raise Redirect(self.request['URL'] + '/confirm-email')
        
        __call__(self, *args, **kw)
    cls.__call__ = wrapped_call

    return cls
