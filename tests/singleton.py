class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_loops'):
            orig = super(Singleton, cls)
            cls._loops = orig.__new__(cls, *args, **kwargs)
        return cls._loops