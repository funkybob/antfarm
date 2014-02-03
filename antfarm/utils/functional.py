

class buffered_property(object):
    '''Buffer the result of a method on the class instance'''
    def __init__(self, getter, name=None):
        self.name = name or getter.__name__
        self.getter = getter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        instance.__dict__[self.name] = value = self.getter(instance)
        return value

