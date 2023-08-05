# -*- coding: utf-8 -*-
# @Time     : 2020/7/23 9:51 上午
# @Author   : binger

from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.ext.indexable import index_property
from sqlalchemy.types import TypeDecorator, Text
from ..common.flask_mock import json_dumps, json_loads


# XXX replace PseudoJSON and MutableDict with real JSON field
class PseudoJSON(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        return json_dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return value
        return json_loads(value)


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, cls):
            if isinstance(cls, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def remove(self, value):
        list.remove(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


class json_cast_property(index_property):
    """
    A SQLAlchemy index property that is able to cast the
    entity attribute as the specified cast type. Useful
    for JSON and JSONB colums for easier querying/filtering.
    """

    def __init__(self, cast_type, *args, **kwargs):
        super(json_cast_property, self).__init__(*args, **kwargs)
        self.cast_type = cast_type

    def expr(self, model):
        expr = super(json_cast_property, self).expr(model)
        return expr.astext.cast(self.cast_type)
