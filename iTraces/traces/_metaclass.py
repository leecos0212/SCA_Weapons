# -*- coding: utf-8 -*-

class ClassWithMetadatas(type):
    """为曲线的metadata创建实例metadata_key
    matadata格式['key1':'value1','key2':'value2',....]
    """

    def __new__(cls, name, bases, namespace, metadatas_keys):
        res = type.__new__(cls, name, bases, namespace)
        res._metadatas_keys = metadatas_keys
        res._metadatas_properties_set()
        res._is_valid_trace_class = True
        res.__doc__ = bases[0].__doc__
        return res

    def _metadatas_properties_set(cls):
        for k in cls._metadatas_keys:
            setattr(cls, f"{k}", cls._metadata_property_create(metadata_key=k))

    def _metadata_property_create(cls, metadata_key):

        def _(self):
            return self.metadatas[metadata_key]

        return property(fget=_, doc="""Returns f'{metadata_key}' array of values.""")
