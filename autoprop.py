"""
Monkeypatching synthesized properties.
"""
try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution('autoprop').version
except Exception:
    __version__ = 'unknown'


class AutoPropDescriptor(object):
    """
    The property descriptor. Stores and looks up the
    value from an attribute. If the value is empty,
    calls the default function declared in the class.
    """
    def __init__(self, default_prop):
        """
        Store the default function and initialize the
        synthesized variable with the same name as the
        default function.
        """
        self.default_prop = default_prop
        self.name = default_prop.__name__
        self.assigned = '_' + self.name

    def __get_assigned__(self, instance):
        """
        Get the value from the synthesized variable.
        """
        return getattr(instance, self.assigned, None)

    def __set_assigned__(self, instance, value):
        """
        Sets the value of the synthesized variable.
        """
        return setattr(instance, self.assigned, value)

    def __get__(self, instance, owner):
        """
        Look up value from the synthesized variable.
        If empty, call the default function to get the
        value
        """
        value = self.__get_assigned__(instance)
        return value or self.default_prop(instance)

    def __set__(self, instance, value):
        """
        Sets the value in the assigned variable.
        """
        self.__set_assigned__(instance, value)

class AutoPropMetaClass(type):

    """
    The meta class responsible for replacing the default
    properties with synthesized ones.
    """

    def __new__(mcs, cname, cbases, cattrs):
        """
        Replace every property that has autoprop attribute set with
        a `AutoPropDescriptor` instance.
        """
        autoprops = {name:member for name, member in cattrs.iteritems()
                        if getattr(member, 'autoprop', False)}
        for name, member in autoprops.iteritems():
            cattrs[name] = AutoPropDescriptor(member)
        return super(AutoPropMetaClass, mcs).__new__(mcs, cname, cbases, cattrs)

class AutoProp(object):
    """
    Base class / Mixin for classes that desire synthesized properties.
    """

    __metaclass__ = AutoPropMetaClass

    @staticmethod
    def default(f):
        """
        Decorator. Simply marks the attributes for the meta class to
        process later.
        """
        f.autoprop = True
        return f