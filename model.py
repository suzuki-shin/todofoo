# -*- coding: utf-8 -*-
from google.appengine.ext import db
# from django.utils import simplejson as json
import logging
import inspect
import json

#
# models
#
class BaseModel(db.Model):
    @classmethod
    def all_by_user(cls, user):
        return cls.all().filter('user =', user).fetch(100)

    @classmethod
    def jsonize(cls, data):
        u"""cls.all()等で取得したデータを渡して、JSONにして返す
        """
        pnames = cls.properties().keys()
        logging.info(pnames)
        d = [dict(zip(pnames, [unicode(a.__getattribute__(p)) for p in pnames])) for a in data]
        logging.info(d)
        return json.dumps(d)

class Task(BaseModel):
    u"""タスク
    """
    is_active  = db.BooleanProperty(default=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    is_done    = db.BooleanProperty(default=False)
    user       = db.UserProperty(required=True)
    name       = db.TextProperty(required=True)
